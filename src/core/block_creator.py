"""
Phase 1: Smart Block Creation with LLM Validation

Creates semantic blocks from markdown, validates self-containedness,
and merges/attaches context as needed.
"""

from __future__ import annotations

import hashlib
import re
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

from .json_utils import extract_json_obj
from .llm_config import get_llm_task_manager
from .semantic_schemas import BlockKind, RawBlock, SelfContainedCheck, ValidatedBlock

# Block type keywords for segmentation
BLOCK_TYPE_KEYWORDS = {
    "toc": ["table des matières", "contents"],
    "definition": ["definition", "définition"],
    "theorem": ["theorem", "théorème"],
    "proof": ["proof", "démonstration", "preuve"],
    "example": ["example", "exemple", "examples", "exemples"],
    "exercise": ["exercise", "exercice", "exercises", "exercices"],
    "lemma": ["lemma", "lemme"],
    "corollary": ["corollary", "corollaire"],
    "proposition": ["proposition"],
    "remark": ["remark", "remarque"],
    "formula": ["formule", "formules", "formula", "formulas", "equations", "equation"],
}


class BlockCreator:
    """Creates and validates semantic blocks from markdown."""

    def __init__(self):
        self.llm = get_llm_task_manager()
        # Pre-calculate keywords for performance
        self._all_keywords = [
            kw
            for btype, keywords in BLOCK_TYPE_KEYWORDS.items()
            if btype != "toc"
            for kw in keywords
        ]
        self._kw_pattern = "|".join(set(re.escape(k) for k in self._all_keywords))
        # Add capitalized versions
        self._kw_pattern += "|" + "|".join(
            set(re.escape(k.capitalize()) for k in self._all_keywords)
        )

    def create_blocks(
        self, md_text: str, *, context_window: int = 3, output_language: str = "fr"
    ) -> List[ValidatedBlock]:
        """
        Create validated blocks from markdown.

        Args:
            md_text: Markdown text
            context_window: Number of preceding/following blocks to consider

        Returns:
            List of validated blocks
        """
        # 1. Initial regex segmentation
        raw_blocks = self._initial_segmentation(md_text)

        # 2. Convert to RawBlock objects
        raw_block_objs = [
            self._to_raw_block(rb, idx) for idx, rb in enumerate(raw_blocks)
        ]

        # 3. Validate and merge blocks
        validated = self._validate_and_merge(
            raw_block_objs,
            context_window=context_window,
            output_language=output_language,
        )

        # 4. Add preceding/following references
        validated = self._add_block_references(validated)

        return validated

    def _initial_segmentation(self, md_text: str) -> List[Dict]:
        """Use simple internal segmentation and merge headers."""
        # Preprocess to ensure headers are separated
        preprocessed_text = self._preprocess_text(md_text)
        raw_blocks = self._simple_segment(preprocessed_text)
        return self._merge_headers(raw_blocks)

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text to ensure robust segmentation.

        1. Ensure all headers (#, ##, etc.) are preceded by empty lines.
        2. Ensure all semantic keywords (Definition, Theorem, etc.) are on their own lines.
        """
        processed = text

        # 1. Handle Headers (#, ##, ###)
        # Rule A: Ensure lines containing a header marker are preceded by double newlines
        # We match a non-newline character followed by a newline, then a line containing a header marker.
        processed = re.sub(
            r"([^\n])\n(?=[ \t]*[^#\n]*(?:#{1,6}\s|###))", r"\1\n\n", processed
        )

        # Rule B: Ensure inline header markers (preceded by a period and space) are preceded by double newlines
        # This handles "Some content. ### New Section" but avoids "EXPONENTIELLE ### Définition"
        processed = re.sub(r"(\.)[ \t]+(?=#{1,6}\s|###)", r"\1\n\n", processed)

        # 2. Handle Semantic Keywords
        # Collect all keywords
        all_keywords = []
        for btype, keywords in BLOCK_TYPE_KEYWORDS.items():
            if btype == "toc":
                continue
            all_keywords.extend(keywords)

        # Create a regex pattern for these keywords
        escaped_kws = [re.escape(k) for k in all_keywords]
        escaped_kws.extend([re.escape(k.capitalize()) for k in all_keywords])
        kw_pattern = "|".join(set(escaped_kws))

        # Pattern for Bold keywords: (**)(Keyword)
        # We exclude * and # and space from the preceding character to avoid splitting ** into *\n\n* or separating from headers
        bold_start_pattern = rf"(\*\*)({kw_pattern})"
        processed = re.sub(
            r"([^\*\#\n\ ])\s*" + bold_start_pattern,
            r"\1\n\n\2\3",
            processed,
            flags=re.IGNORECASE,
        )

        # Pattern for "Keyword (" or "Keyword :"
        # We use negative lookbehind (?<!\*\*) to ensure we don't match if preceded by **
        # We also exclude * and # and space from the preceding character to be safe
        context_pattern = rf"(?<!\*\*)(\b)({kw_pattern})(\s*)([(:])"
        processed = re.sub(
            r"([^\*\#\n\ ])\s*" + context_pattern,
            r"\1\n\n\3\4\5",
            processed,
            flags=re.IGNORECASE,
        )

        return processed

    def _merge_headers(self, blocks: List[Dict]) -> List[Dict]:
        """
        Heuristically merge headers/titles with subsequent content.
        """
        if not blocks:
            return []

        merged = []
        i = 0
        while i < len(blocks):
            current = blocks[i]

            # Check if we can merge with next
            if i + 1 < len(blocks):
                next_block = blocks[i + 1]

                is_title_type = current["type"] in [
                    "header",
                    "theorem",
                    "definition",
                    "proof",
                    "example",
                    "exercise",
                    "lemma",
                    "corollary",
                    "proposition",
                    "remark",
                ]

                # If current is just a title/header and next is the content
                if is_title_type:
                    # Check if current block is actually a title (short) or already a full block
                    is_short = (
                        len(current["text"]) < 200 and current["text"].count("\n") < 3
                    )

                    # Merge logic:
                    # 1. Headers ALWAYS merge with next (unless next is also a header)
                    # 2. Semantic blocks (Theorem, etc.) merge if:
                    #    - Next block is 'text' or 'header'
                    #    - OR Next block has the SAME type (e.g., "## Preuve" -> "Proof content")
                    if current["type"] == "header":
                        should_merge = next_block["type"] not in [
                            "header",
                            "theorem",
                            "definition",
                            "lemma",
                            "corollary",
                            "proposition",
                        ]
                    else:
                        # For semantic types like 'proof', 'theorem', etc.
                        should_merge = is_short and (
                            next_block["type"] in ["text", "header"]
                            or next_block["type"] == current["type"]
                        )

                    if not should_merge:
                        # Don't merge
                        merged.append(current)
                        i += 1
                        continue

                    # Merge logic
                    # We assume the next block belongs to this title
                    current["text"] = f"{current['text']}\n\n{next_block['text']}"
                    # Preserve line range: start from current, end at next
                    current["end_line"] = next_block.get(
                        "end_line", current.get("end_line", 0)
                    )

                    # Use the more specific type: if current is "header", use next block's type if it's not "text"
                    if current["type"] == "header" and next_block["type"] != "text":
                        current["type"] = next_block["type"]

                    # Keep the specific type of the current block
                    i += 2
                    merged.append(current)
                    continue

            merged.append(current)
            i += 1

        return merged

    def _simple_segment(self, text: str) -> List[Dict]:
        """
        Simple segmentation by double newlines and headers.
        """
        blocks = []
        current_lines = []
        current_start_line = 0

        def flush_block(line_idx: int):
            if not current_lines:
                return

            full_text = "\n".join(current_lines).strip()
            if not full_text:
                current_lines.clear()
                return

            # Detect type using keyword dictionary
            block_type = "text"
            lower_text = full_text.lower()
            is_toc = False

            # 1. Check if the block STARTS with a keyword (highest priority)
            # We strip common markdown/title markers first
            stripped_start = full_text.lstrip("*_# \t\n").lower()

            found_start_kw = False
            for btype, keywords in BLOCK_TYPE_KEYWORDS.items():
                if any(stripped_start.startswith(kw) for kw in keywords):
                    block_type = btype
                    if btype == "toc":
                        is_toc = True
                    found_start_kw = True
                    break

            # 2. If no starting keyword, check for keyword anywhere in the text (lower priority)
            # ONLY for short blocks to avoid misidentifying long descriptive paragraphs
            if not found_start_kw and len(full_text) < 100:
                for btype, keywords in BLOCK_TYPE_KEYWORDS.items():
                    if any(kw in lower_text for kw in keywords):
                        block_type = btype
                        if btype == "toc":
                            is_toc = True
                        break

            # If no keyword found and it's a header, mark as header
            if block_type == "text" and (
                lower_text.startswith("#") or "###" in lower_text
            ):
                block_type = "header"

            blocks.append(
                {
                    "type": block_type,
                    "text": full_text,
                    "page": 0,
                    "is_toc": is_toc,
                    "start_line": current_start_line,
                    "end_line": line_idx - 1,  # Last line before flush
                }
            )
            current_lines.clear()

        lines = text.split("\n")
        empty_line_count = 0

        for line_idx, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                # Count consecutive empty lines
                empty_line_count += 1
                # Only flush on double empty lines (real paragraph break)
                if empty_line_count >= 2:
                    flush_block(line_idx)
                    current_start_line = line_idx + 1
                    empty_line_count = 0
                continue

            # Reset empty line counter when we hit content
            empty_line_count = 0

            # Check if this line should start a new block
            # 1. It's a header
            if stripped.startswith("#") or "###" in stripped:
                flush_block(line_idx)
                current_start_line = line_idx
                current_lines.append(line)
                flush_block(line_idx + 1)  # Headers are single lines usually
                current_start_line = line_idx + 1
                continue

            # 2. It's a keyword start (Theorem, etc)
            cleaned_line = stripped.lstrip("*_# ").lower()
            is_keyword = any(cleaned_line.startswith(kw) for kw in self._all_keywords)

            if is_keyword and current_lines:
                flush_block(line_idx)
                current_start_line = line_idx

            current_lines.append(line)

        flush_block(len(lines))
        return blocks

    def _to_raw_block(self, block_dict: Dict, index: int) -> RawBlock:
        """Convert dict block to RawBlock."""
        return RawBlock(
            type=block_dict.get("type", "unknown"),
            text=block_dict.get("text", ""),
            page=block_dict.get("page", 0),
            is_toc=block_dict.get("is_toc", False),
            start_line=block_dict.get("start_line", 0),
            end_line=block_dict.get("end_line", 0),
        )

    def _validate_and_merge(
        self,
        raw_blocks: List[RawBlock],
        *,
        context_window: int = 3,
        output_language: str = "fr",
    ) -> List[ValidatedBlock]:
        """
        Validate blocks and merge if needed.
        """
        validated: List[ValidatedBlock] = []
        skip_indices = set()

        from .config import settings

        batch_size = settings.llm_batch_size if settings.fixmath_use_llm else 1

        # Prepare all blocks and their contexts first
        blocks_to_process = []
        for idx, raw_block in enumerate(raw_blocks):
            if raw_block.is_toc and not self._is_proof_type(raw_block.type):
                continue

            preceding = self._get_preceding_blocks(raw_blocks, idx, context_window)
            following = self._get_following_blocks(raw_blocks, idx, context_window)
            blocks_to_process.append(
                {
                    "idx": idx,
                    "block": raw_block,
                    "preceding": preceding,
                    "following": following,
                }
            )

        # Process in batches
        all_results = []
        pbar = tqdm(total=len(blocks_to_process), desc="Validating blocks")
        for i in range(0, len(blocks_to_process), batch_size):
            batch = blocks_to_process[i : i + batch_size]
            batch_blocks = [b["block"] for b in batch]
            batch_preceding = [b["preceding"] for b in batch]
            batch_following = [b["following"] for b in batch]

            batch_results = self._check_self_contained_batch(
                batch_blocks,
                batch_preceding,
                batch_following,
                output_language=output_language,
            )

            for b_info, result in zip(batch, batch_results):
                all_results.append((b_info, result))
            pbar.update(len(batch))
        pbar.close()

        # Final loop to handle merges and creation
        for b_info, check_result in all_results:
            idx = b_info["idx"]
            if idx in skip_indices:
                continue

            raw_block = b_info["block"]
            preceding = b_info["preceding"]
            following = b_info["following"]

            # Determine block kind
            kind = self._infer_block_kind(raw_block.type)
            validation_errors = []
            if len(raw_block.text) > 1500 and kind != BlockKind.proof:
                kind = BlockKind.manual_review
                validation_errors.append(
                    f"Block too long ({len(raw_block.text)} chars)."
                )

            # If not self-contained, try to merge
            if not check_result.is_self_contained:
                merged_block, merged_indices = self._try_merge(
                    raw_block,
                    raw_blocks,
                    idx,
                    check_result,
                    preceding=preceding,
                    following=following,
                )
                if merged_block:
                    raw_block = merged_block
                    skip_indices.update(merged_indices)
                    # Re-check after merge
                    check_result = self._check_self_contained(
                        raw_block,
                        preceding=preceding,
                        following=following,
                        output_language=output_language,
                    )

            # Create validated block
            block_id = self._generate_block_id(raw_block, idx)
            validated_block = ValidatedBlock(
                id=block_id,
                kind=kind,
                raw_text=raw_block.text,
                validated_text=raw_block.text,
                page=raw_block.page,
                start_line=raw_block.start_line,
                end_line=raw_block.end_line,
                is_self_contained=check_result.is_self_contained,
                missing_context=check_result.missing,
                validation_errors=validation_errors,
                normalized_text=check_result.normalized_text,
                tags=check_result.tags,
            )

            validated.append(validated_block)

        # Second pass: Populate preceding and following blocks
        for i, block in enumerate(validated):
            # Preceding
            start_p = max(0, i - context_window)
            block.preceding_blocks = [b.id for b in validated[start_p:i]]

            # Following
            end_f = min(len(validated), i + 1 + context_window)
            block.following_blocks = [b.id for b in validated[i + 1 : end_f]]

        return validated

    def _check_self_contained_batch(
        self,
        blocks: List[RawBlock],
        preceding_list: List[List[RawBlock]],
        following_list: List[List[RawBlock]],
        *,
        output_language: str = "fr",
    ) -> List[SelfContainedCheck]:
        """Check multiple blocks in a single LLM request."""
        from .language_detector import format_language_instruction

        if not blocks:
            return []

        lang_instruction = format_language_instruction(output_language)

        # Build the batched prompt
        blocks_content = []
        for i, block in enumerate(blocks):
            pre_text = "\n\n".join(b.text for b in preceding_list[i])
            foll_text = "\n\n".join(b.text for b in following_list[i])

            blocks_content.append(
                f"### TARGET BLOCK {i}\n<<<< BLOCK START >>>>\n{block.text}\n<<<< BLOCK END >>>>\n\nPRECEDING CONTEXT:\n{pre_text[:500] or 'None'}\n\nFOLLOWING CONTEXT:\n{foll_text[:500] or 'None'}\n"
            )

        all_blocks_text = "\n\n---\n\n".join(blocks_content)

        prompt = f"""Analyze if each of the following {len(blocks)} mathematical blocks is self-contained and provide a normalized version for each.

### CONTEXTUAL INFORMATION
A block is self-contained if:
- for definition blocks, definitions used are present in the block
- for theorem blocks, theorems mentioned are stated in the block
- for proof blocks, theorems mentioned  are not necessarily stated can just be referenced
- If it's a proof, it is self-contained if the theorem being proved is in the PRECEDING CONTEXT.
- **IMPORTANT**: Theorem and Proof should remain in SEPARATE blocks.
- It contains actual content, NOT just a title.

### NORMALIZATION RULES
- **Strict Scope**: ONLY normalize the content found within the TARGET BLOCK.
- **No Context Contamination**: Do NOT include information from PRECEDING/FOLLOWING context.
- **Theorems**: Include Name, Hypotheses, and Conclusion. No proof steps.
- **Proofs**: do not repeat the result statement, only the proof steps.
- **Synthetic & Structured**: Use bullet points.

### INPUT DATA
{all_blocks_text}

{lang_instruction}

Respond in strict JSON as a LIST of objects:
[
  {{
    "block_index": 0,
    "is_self_contained": true|false,
    "missing": [...],
    "needs_preceding": true|false,
    "needs_following": true|false,
    "suggest_merge_with": [],
    "normalized_text": "...",
    "tags": [...]
  }},
  ...
]"""

        try:
            response = self.llm.generate(
                "block_validation",
                prompt,
                display_name="batch_validation",
                expect_json=True,
            )
            data_list = extract_json_obj(response)
            if not isinstance(data_list, list):
                raise ValueError("Expected a list of results")

            # Map back to original order and handle missing indices
            results_map = {
                item["block_index"]: item for item in data_list if "block_index" in item
            }
            final_results = []
            for i in range(len(blocks)):
                if i in results_map:
                    data = results_map[i]
                    # FIX: Coerce types for Pydantic (int -> str)
                    if "suggested_merge_with" in data and isinstance(
                        data["suggested_merge_with"], list
                    ):
                        data["suggested_merge_with"] = [
                            str(x) for x in data["suggested_merge_with"]
                        ]
                    if "missing" in data and isinstance(data["missing"], list):
                        data["missing"] = [str(x) for x in data["missing"]]

                    final_results.append(SelfContainedCheck(**data))
                else:
                    # Fallback for this specific block if missing from LLM response
                    final_results.append(
                        SelfContainedCheck(
                            is_self_contained=True,
                            missing=[],
                            normalized_text=blocks[i].text,
                        )
                    )
            return final_results

        except Exception as e:
            print(
                f"WARNING: Batched LLM validation failed: {e}. Falling back to individual checks."
            )
            # Fallback: process individually
            return [
                self._check_self_contained(b, p, f, output_language=output_language)
                for b, p, f in zip(blocks, preceding_list, following_list)
            ]

    def _check_self_contained(
        self,
        block: RawBlock,
        preceding: List[RawBlock],
        following: List[RawBlock],
        *,
        output_language: str = "fr",
    ) -> SelfContainedCheck:
        """Check if block is self-contained using LLM."""
        from .language_detector import format_language_instruction

        preceding_text = "\n\n".join(b.text for b in preceding)
        following_text = "\n\n".join(b.text for b in following)
        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Analyze if the TARGET BLOCK is self-contained and provide a normalized, synthetic version.

### CONTEXTUAL INFORMATION
A block is self-contained if:
- All definitions used are present in the block
- All theorems mentioned are stated in the block
- If it's a proof, it is self-contained if it references the theorem being proved.
- **IMPORTANT**: Theorem and Proof should remain in SEPARATE blocks for Anki card creation. Do NOT suggest merging a Theorem with its Proof/Démonstration.
- It contains actual content, NOT just a title (e.g., "Proof", "Theorem X" alone is NOT self-contained)

### NORMALIZATION RULES
If the block is self-contained, provide a `normalized_text` version:
- **Strict Scope**: ONLY normalize the content found within the TARGET BLOCK.
- **No Context Contamination**: Do NOT include information, proofs, or steps found in the PRECEDING or FOLLOWING context if they are not in the TARGET BLOCK.
- **Theorems**: Include Name, Hypotheses, and Conclusion. Do NOT include proof steps or assumptions used for proof-by-contradiction (e.g., if the theorem says "A is true", do not list "Assume A is false" as a hypothesis).
- **Synthetic**: Eliminate unnecessary explanations or filler text.
- **Structured**: Use bullet points or line breaks for reasoning steps.
- **Tagged**: Identify names of properties/theorems/formulas at the beginning.

### INPUT DATA
<<<< TARGET BLOCK START >>>>
{block.text}
<<<< TARGET BLOCK END >>>>

PRECEDING CONTEXT:
{preceding_text[:1000] or "None"}

FOLLOWING CONTEXT:
{following_text[:1000] or "None"}

{lang_instruction}

Respond in strict JSON:
{{
  "is_self_contained": true|false,
  "missing": ["definition of X", "theorem Y", "content missing", ...],
  "needs_preceding": true|false,
  "needs_following": true|false,
  "suggested_merge_with": [],
  "normalized_text": "Synthetic and structured version of ONLY the TARGET BLOCK",
  "tags": ["property name", "theorem name", "formula name"]
}}"""

        try:
            response = self.llm.generate("block_validation", prompt, expect_json=True)
            data = extract_json_obj(response)
            return SelfContainedCheck(**data)
        except Exception as e:
            print(
                f"WARNING: LLM block validation failed: {e}. Falling back to self-contained=True."
            )
            # Fallback: assume self-contained if check fails
            return SelfContainedCheck(
                is_self_contained=True,
                missing=[],
                needs_preceding=False,
                needs_following=False,
                suggested_merge_with=[],
            )

    def _try_merge(
        self,
        block: RawBlock,
        all_blocks: List[RawBlock],
        current_idx: int,
        check_result: SelfContainedCheck,
        *,
        preceding: List[RawBlock],
        following: List[RawBlock],
    ) -> Tuple[Optional[RawBlock], List[int]]:
        """
        Try to merge block with preceding/following blocks.
        """
        merged_indices = []
        merged_text = block.text

        # Try merging with preceding blocks
        if check_result.needs_preceding and preceding:
            # Merge with last preceding block
            last_preceding = preceding[-1]

            # Safeguard: Don't merge a Proof with a Theorem unless one is very short
            is_cross_merge = (
                self._is_proof_type(block.type)
                and "theor" in last_preceding.type.lower()
            ) or (
                self._is_proof_type(last_preceding.type)
                and "theor" in block.type.lower()
            )
            if (
                is_cross_merge
                and len(block.text) > 200
                and len(last_preceding.text) > 200
            ):
                pass  # Don't merge
            else:
                merged_text = f"{last_preceding.text}\n\n{merged_text}"
                # Find index of last_preceding in all_blocks
                for i, b in enumerate(all_blocks):
                    if b.text == last_preceding.text and i < current_idx:
                        merged_indices.append(i)
                        break

        # Try merging with following blocks
        if check_result.needs_following and following:
            # Merge with first following block
            first_following = following[0]

            # Safeguard: Don't merge a Theorem with a Proof unless one is very short
            is_cross_merge = (
                self._is_proof_type(block.type)
                and "theor" in first_following.type.lower()
            ) or (
                self._is_proof_type(first_following.type)
                and "theor" in block.type.lower()
            )
            if (
                is_cross_merge
                and len(block.text) > 200
                and len(first_following.text) > 200
            ):
                pass  # Don't merge
            else:
                merged_text = f"{merged_text}\n\n{first_following.text}"
                # Find index of first_following in all_blocks
                for i, b in enumerate(all_blocks):
                    if b.text == first_following.text and i > current_idx:
                        merged_indices.append(i)
                        break

        if merged_indices:
            merged_block = RawBlock(
                type=block.type,
                text=merged_text,
                page=block.page,
                is_toc=False,
                start_line=block.start_line,
                end_line=block.end_line,
            )
            return merged_block, merged_indices

        return None, []

    def _get_preceding_blocks(
        self, blocks: List[RawBlock], idx: int, window: int
    ) -> List[RawBlock]:
        """Get preceding blocks within window."""
        start = max(0, idx - window)
        return blocks[start:idx]

    def _get_following_blocks(
        self, blocks: List[RawBlock], idx: int, window: int
    ) -> List[RawBlock]:
        """Get following blocks within window."""
        end = min(len(blocks), idx + 1 + window)
        return blocks[idx + 1 : end]

    def _add_block_references(
        self, blocks: List[ValidatedBlock]
    ) -> List[ValidatedBlock]:
        """Add preceding/following block ID references."""
        for idx, block in enumerate(blocks):
            # Preceding
            if idx > 0:
                block.preceding_blocks = [blocks[idx - 1].id]
            # Following
            if idx < len(blocks) - 1:
                block.following_blocks = [blocks[idx + 1].id]

        return blocks

    def _infer_block_kind(self, type_str: str) -> BlockKind:
        """Infer BlockKind from type string."""
        type_lower = type_str.lower()

        # Direct mapping from BLOCK_TYPE_KEYWORDS keys to BlockKind
        type_to_kind = {
            "definition": BlockKind.definition,
            "theorem": BlockKind.theorem,
            "proposition": BlockKind.proposition,
            "lemma": BlockKind.lemma,
            "corollary": BlockKind.corollary,
            "exercise": BlockKind.exercise,
            "proof": BlockKind.proof,
            "example": BlockKind.example,
            "remark": BlockKind.remark,
            "formula": BlockKind.formula,
        }

        # Check if type_str matches any key in BLOCK_TYPE_KEYWORDS
        for block_type, keywords in BLOCK_TYPE_KEYWORDS.items():
            if block_type in type_to_kind and type_lower == block_type:
                return type_to_kind[block_type]
            # Also check if type_str matches any of the keywords
            for keyword in keywords:
                if keyword in type_lower:
                    if block_type in type_to_kind:
                        return type_to_kind[block_type]

        return BlockKind.unknown

    def _is_proof_type(self, type_str: str) -> bool:
        """Check if type is a proof."""
        type_lower = type_str.lower()
        return any(
            x in type_lower
            for x in ["démonstration", "demonstration", "proof", "preuve"]
        )

    def _generate_block_id(self, block: RawBlock, index: int) -> str:
        """Generate unique block ID."""
        # Use hash of first 100 chars + index for uniqueness
        text_hash = hashlib.sha256(block.text[:100].encode()).hexdigest()[:8]
        return f"block_{index}_{text_hash}"
