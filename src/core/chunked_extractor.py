"""
Chunked Batch Extraction Module

Handles splitting markdown into overlapping chunks and extracting semantic blocks
via LLM batch processing.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tqdm import tqdm

from .config import settings
from .constants import BLOCK_TYPE_KEYWORDS
from .json_utils import extract_json_obj
from .language_detector import format_language_instruction
from .llm_config import get_llm_task_manager


@dataclass
class TextChunk:
    """Represents a chunk of text with overlap context."""

    index: int  # Chunk number (0-indexed)
    text: str  # Full chunk text (including overlaps)
    start_offset: int  # Starting character position in original document
    end_offset: int  # Ending character position in original document
    has_preceding_overlap: (
        bool  # True if this chunk has preceding context from prev chunk
    )
    has_following_overlap: (
        bool  # True if this chunk has following context from next chunk
    )


class ChunkManager:
    """Manages text chunking with overlapping windows."""

    def __init__(
        self,
        chunk_size: int = settings.chunk_size_chars,
        overlap_size: int = settings.chunk_overlap_chars,
    ):
        """
        Initialize ChunkManager.

        Args:
            chunk_size: Size of each chunk in characters
            overlap_size: Size of overlap before/after in characters
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def split_text(self, text: str) -> List[TextChunk]:
        """
        Split text into overlapping chunks.

        Strategy:
        - First chunk: 0 to chunk_size (no preceding overlap)
        - Middle chunks: includes overlap_size before and after
        - Last chunk: includes overlap_size before (no following overlap)

        Args:
            text: Full markdown text

        Returns:
            List of TextChunk objects
        """
        total_length = len(text)
        chunks = []

        if total_length <= self.chunk_size:
            # Text fits in one chunk
            chunks.append(
                TextChunk(
                    index=0,
                    text=text,
                    start_offset=0,
                    end_offset=total_length,
                    has_preceding_overlap=False,
                    has_following_overlap=False,
                )
            )
            return chunks

        # Calculate chunk boundaries
        current_pos = 0
        chunk_index = 0

        while current_pos < total_length:
            # Determine chunk boundaries
            chunk_start = max(0, current_pos - self.overlap_size)
            chunk_end = min(total_length, current_pos + self.chunk_size)

            # Extract chunk text
            chunk_text = text[chunk_start:chunk_end]

            # Determine if this is the last chunk
            is_last_chunk = chunk_end >= total_length

            # Add following overlap if not last chunk
            if not is_last_chunk:
                overlap_end = min(total_length, chunk_end + self.overlap_size)
                chunk_text = text[chunk_start:overlap_end]
                actual_end = overlap_end
            else:
                actual_end = chunk_end

            chunks.append(
                TextChunk(
                    index=chunk_index,
                    text=chunk_text,
                    start_offset=chunk_start,
                    end_offset=actual_end,
                    has_preceding_overlap=(chunk_start > 0),
                    has_following_overlap=(not is_last_chunk),
                )
            )

            # Move to next chunk (skip by chunk_size, not accounting for overlap)
            current_pos += self.chunk_size
            chunk_index += 1

        return chunks

    def global_offset(self, chunk: TextChunk, local_offset: int) -> int:
        """
        Convert local character offset within chunk to global offset in document.

        Args:
            chunk: The TextChunk
            local_offset: Character position within chunk.text

        Returns:
            Global character position in original document
        """
        return chunk.start_offset + local_offset


@dataclass
class ExtractedBlock:
    """Represents a block extracted from a chunk."""

    # Block identification
    type: str  # Maps to BLOCK_TYPE_KEYWORDS
    normalized_name: Optional[str] = None
    tags: List[str] = None

    # Content
    raw_text: str = ""
    normalized_text: str = ""

    # Position in original document
    start_char_offset: int = 0
    end_char_offset: int = 0
    chunk_index: int = 0

    # Extra semantic data (optional)
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize mutable defaults."""
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}

    def generate_hash(self) -> str:
        """Generate content hash for this block."""
        content = (
            f"{self.normalized_text}|{self.start_char_offset}|{self.end_char_offset}"
        )
        return hashlib.md5(content.encode()).hexdigest()[:12]


class BlockDeduplicator:
    """Handles deduplication of blocks from overlapping chunks."""

    def __init__(
        self,
        similarity_threshold: float = settings.dedupe_similarity_threshold,
        offset_overlap_threshold: float = settings.dedupe_offset_overlap_threshold,
    ):
        """
        Initialize BlockDeduplicator.

        Args:
            similarity_threshold: Embedding similarity threshold (0-1)
            offset_overlap_threshold: Character offset overlap ratio (0-1)
        """
        self.similarity_threshold = similarity_threshold
        self.offset_overlap_threshold = offset_overlap_threshold

    def deduplicate(self, blocks: List[ExtractedBlock]) -> List[ExtractedBlock]:
        """
        Deduplicate blocks from overlapping chunks.

        Strategy:
        1. Group blocks by chunk pairs that might overlap
        2. For each pair of blocks from adjacent chunks:
           a. Check if character offsets overlap significantly
           b. Check if normalized text is semantically similar (embedding)
        3. If both checks pass, keep the block with more complete context

        Args:
            blocks: List of all extracted blocks from all chunks

        Returns:
            Deduplicated list of blocks
        """
        if not blocks:
            return []

        # Sort by start offset for easier processing
        sorted_blocks = sorted(blocks, key=lambda b: b.start_char_offset)

        # Track which blocks to keep
        to_keep = []
        skip_indices = set()

        for i, block1 in enumerate(sorted_blocks):
            if i in skip_indices:
                continue

            # Check for duplicates in subsequent blocks
            is_duplicate = False
            for j in range(i + 1, len(sorted_blocks)):
                if j in skip_indices:
                    continue

                block2 = sorted_blocks[j]

                # Blocks should be from adjacent or nearby chunks to be duplicates
                if abs(block1.chunk_index - block2.chunk_index) > 1:
                    # Too far apart, stop checking
                    if block2.start_char_offset > block1.end_char_offset + 1000:
                        break
                    continue

                # Check if offsets overlap
                if self._offsets_overlap(block1, block2):
                    # Check semantic similarity
                    if self._are_semantically_similar(block1, block2):
                        # Found duplicate - keep the one with more context
                        if len(block2.raw_text) > len(block1.raw_text):
                            # Keep block2, skip block1
                            is_duplicate = True
                            skip_indices.add(i)
                            break
                        else:
                            # Keep block1, skip block2
                            skip_indices.add(j)

            if not is_duplicate:
                to_keep.append(block1)

        return to_keep

    def _offsets_overlap(self, block1: ExtractedBlock, block2: ExtractedBlock) -> bool:
        """
        Check if two blocks have overlapping character offsets.

        Args:
            block1: First block
            block2: Second block

        Returns:
            True if offsets overlap significantly
        """
        # Calculate overlap
        overlap_start = max(block1.start_char_offset, block2.start_char_offset)
        overlap_end = min(block1.end_char_offset, block2.end_char_offset)
        overlap_length = max(0, overlap_end - overlap_start)

        # Calculate lengths
        len1 = block1.end_char_offset - block1.start_char_offset
        len2 = block2.end_char_offset - block2.start_char_offset

        # Check if overlap is significant (relative to shorter block)
        min_length = min(len1, len2)
        if min_length == 0:
            return False

        overlap_ratio = overlap_length / min_length
        return overlap_ratio >= self.offset_overlap_threshold

    def _are_semantically_similar(
        self, block1: ExtractedBlock, block2: ExtractedBlock
    ) -> bool:
        """
        Check if two blocks are semantically similar.

        For now, use simple text comparison. Can be enhanced with embeddings later.

        Args:
            block1: First block
            block2: Second block

        Returns:
            True if blocks are semantically similar
        """
        # Simple approach: compare normalized text similarity
        text1 = block1.normalized_text.lower().strip()
        text2 = block2.normalized_text.lower().strip()

        # If texts are very similar, they're likely duplicates
        if text1 == text2:
            return True

        # Calculate character-level similarity (Jaccard on words)
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return False

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        similarity = intersection / union if union > 0 else 0
        return similarity >= self.similarity_threshold


class ChunkedBlockExtractor:
    """
    Main orchestrator for chunked batch extraction.
    """

    def __init__(self):
        self.chunk_manager = ChunkManager()
        self.deduplicator = BlockDeduplicator()
        self.llm = get_llm_task_manager()

    def extract_blocks(
        self, md_text: str, *, output_language: str = "fr"
    ) -> List[ExtractedBlock]:
        """
        Extract blocks from markdown text using chunked processing.

        Args:
            md_text: Markdown content
            output_language: Target output language ("fr", "en", "auto")

        Returns:
            List of unique extracted blocks
        """
        if not md_text.strip():
            return []

        # 1. Split text into chunks
        chunks = self.chunk_manager.split_text(md_text)
        print(f"INFO: Split text into {len(chunks)} chunks.")

        # 2. Process each chunk
        all_blocks = []
        for chunk in tqdm(chunks, desc="Processing chunks"):
            chunk_blocks = self._process_chunk(chunk, output_language)
            all_blocks.extend(chunk_blocks)

        # 3. Deduplicate
        unique_blocks = self.deduplicator.deduplicate(all_blocks)

        return unique_blocks

    def _process_chunk(
        self, chunk: TextChunk, output_language: str
    ) -> List[ExtractedBlock]:
        """
        Process a single chunk with LLM.

        Args:
            chunk: TextChunk to process
            output_language: Output language

        Returns:
            List of ExtractedBlock from this chunk
        """
        lang_instruction = format_language_instruction(output_language)

        # Build category list string
        categories_str = ""
        for btype, keywords in BLOCK_TYPE_KEYWORDS.items():
            if btype == "toc":
                continue
            categories_str += f"- **{btype}** ({'/'.join(keywords[:2])})\n"

        prompt = f"""You are analyzing a CHUNK of a mathematical document to extract self-contained semantic blocks. 

CRITICAL: Extract ONLY blocks where the raw_text contains the COMPLETE statement, proof, or definition.
Do NOT extract title-only blocks or incomplete fragments.

### BLOCK CATEGORIES
Extract blocks from these categories (mapped to BLOCK_TYPE_KEYWORDS):
{categories_str}

### SELF-CONTAINEDNESS RULES
A block is self-contained if:
- **Definitions**: The term AND its complete statement are both in raw_text
- **Theorems/Propositions/Lemmas**: Name (if any), ALL hypotheses, and the conclusion are present in raw_text
- **Proofs**: All proof steps are in raw_text (the theorem being proved may be in preceding context)
- **Examples/Exercises**: The complete question and solution/approach are in raw_text
- **NOT self-contained**: Title-only blocks (e.g., "Theorem 5.2" without statement), incomplete fragments

### NORMALIZATION RULES
For each block, provide a `normalized_text` version:

**All block types**:
- **Strict Scope**: Normalize ONLY content in raw_text, do NOT add external context
- **Synthetic**: Remove filler text, explanations, redundancy
- **Structured**: Use bullet points and clear formatting

**Theorems/Propositions/Lemmas**:
- Format: **Name** (if any): [Hypotheses] -> [Conclusion]
- Hypotheses as bullet points
- Do NOT include proof steps
- Do NOT include proof-by-contradiction assumptions as hypotheses

**Proofs**:
- List each reasoning step as a bullet point
- Do NOT repeat the theorem statement
- Keep only the proof logic

**Definitions**:
- Format: **Term**: [Clear statement]
- If multiple definitions in one block, list each separately

**Examples/Exercises**:
- Question(s) as bullet points
- Solution steps as numbered/bulleted list

### TAGGING
Extract:
- **normalized_name**: Standard English name (e.g., "Cauchy-Schwarz Inequality", "Definition of Topology")
  - For unnamed items, use descriptive name based on content
- **tags**: Domain tags (e.g., ["topology", "metric spaces", "continuity"])

### TASK
For each self-contained semantic block found in the chunk:

1. **type**: One of the block categories above
2. **normalized_name**: English name or descriptive title
3. **tags**: Domain/topic tags (2-5 tags)
4. **raw_text**: Exact text from chunk (preserve LaTeX, line breaks)
5. **normalized_text**: Cleaned, structured version following rules above
6. **steps**: (proofs/exercises only) List of proof/solution steps
7. **hypotheses**: (theorems/propositions only) List of hypotheses
8. **conclusion**: (theorems/propositions only) The conclusion statement
9. **start_char_offset**: Starting character position in chunk (0-indexed)
10. **end_char_offset**: Ending character position in chunk

### OVERLAP HANDLING
This chunk may overlap with adjacent chunks. Extract ALL self-contained blocks you find, even if partially in overlap regions. The deduplication will be handled later.

### NOISE HANDLING
- **Ignore Table of Contents**: Do NOT extract entries from tables of contents or indices.
- **Ignore Page Headers/Footers**: Do NOT extract page numbers, document titles, or author names found at the top/bottom of pages.

### JSON & LaTeX RULES
- **Strict JSON**: Respond with ONLY valid JSON.
- **LaTeX Escaping**: In JSON string values, YOU MUST DOUBLE THE BACKSLASHES for LaTeX. Example: `"raw_text": "\\\\pi"` (not `\\pi`).

### INPUT CHUNK
{chunk.text}

{lang_instruction}

### RESPONSE FORMAT
Respond with ONLY valid JSON (no markdown fences, no commentary):
{{
  "blocks": {{
    "001": {{
      "type": "theorem",
      "normalized_name": "Pythagorean Theorem",
      "tags": ["geometry", "triangles"],
      "raw_text": "...",
      "normalized_text": "**Pythagorean Theorem**:\\n- Hypothesis: Right triangle with legs a, b and hypotenuse c\\n- Conclusion: a² + b² = c²",
      "hypotheses": ["Right triangle with legs a, b and hypotenuse c"],
      "conclusion": "a² + b² = c²",
      "start_char_offset": 1234,
      "end_char_offset": 2345
    }},
    "002": {{ ... }}
  }}
}}"""

        try:
            print(
                f"INFO: Requesting extraction for chunk {chunk.index} ({len(chunk.text)} chars)..."
            )
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
            print(f"INFO: Received response for chunk {chunk.index}.")

            data = extract_json_obj(response)
            if not data or "blocks" not in data:
                print(
                    f"WARNING: Chunk {chunk.index} response has no 'blocks' key or is empty."
                )
                if not data:
                    print(f"DEBUG: Raw response: {response[:500]}...")
                return []

            blocks_dict = data["blocks"]
            extracted = []
            for block_id, block_data in blocks_dict.items():
                try:
                    # Convert local offsets to global
                    local_start = block_data.get("start_char_offset", 0)
                    local_end = block_data.get("end_char_offset", 0)

                    # Validate offsets within chunk length
                    local_start = max(0, min(local_start, len(chunk.text)))
                    local_end = max(0, min(local_end, len(chunk.text)))

                    block = ExtractedBlock(
                        type=block_data.get("type", "unknown").lower(),
                        normalized_name=block_data.get("normalized_name"),
                        tags=block_data.get("tags", []),
                        raw_text=block_data.get("raw_text", ""),
                        normalized_text=block_data.get("normalized_text", ""),
                        start_char_offset=self.chunk_manager.global_offset(
                            chunk, local_start
                        ),
                        end_char_offset=self.chunk_manager.global_offset(
                            chunk, local_end
                        ),
                        chunk_index=chunk.index,
                        metadata={
                            k: v
                            for k, v in block_data.items()
                            if k
                            not in [
                                "type",
                                "tags",
                                "raw_text",
                                "normalized_text",
                                "start_char_offset",
                                "end_char_offset",
                            ]
                        },
                    )
                    extracted.append(block)
                    print(
                        f"INFO: Extracted block: [{block.type}] {block.normalized_name}"
                    )
                except Exception as e:
                    print(f"ERROR: Failed to parse block {block_id}: {e}")
                    continue

            print(f"INFO: Chunk {chunk.index} yielded {len(extracted)} blocks.")
            return extracted

        except Exception as e:
            import traceback

            print(f"ERROR: Chunk {chunk.index} processing failed: {e}")
            traceback.print_exc()
            return []
