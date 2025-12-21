"""
Phase 1: Smart Block Creation with Chunked LLM Extraction

Creates semantic blocks from markdown using chunked batch processing and LLM extraction.
"""

from typing import List

from .chunked_extractor import ChunkedBlockExtractor, ExtractedBlock
from .constants import BLOCK_TYPE_KEYWORDS
from .semantic_schemas import BlockKind, ValidatedBlock


class BlockCreator:
    """Creates and validates semantic blocks from markdown using chunked extraction."""

    def __init__(self):
        self.extractor = ChunkedBlockExtractor()

    def create_blocks(
        self, md_text: str, *, context_window: int = 3, output_language: str = "fr"
    ) -> List[ValidatedBlock]:
        """
        Create validated blocks from markdown using chunked LLM extraction.

        Args:
            md_text: Markdown text
            context_window: (Deprecated/Unused in chunked mode)
            output_language: Target output language ("fr", "en", "auto")

        Returns:
            List of validated blocks
        """
        # 1. Extract blocks using chunked extractor
        extracted_blocks = self.extractor.extract_blocks(
            md_text, output_language=output_language
        )

        # 2. Convert to ValidatedBlock objects
        validated_blocks = []
        for idx, extracted in enumerate(extracted_blocks):
            validated = self._to_validated_block(extracted, idx)
            validated_blocks.append(validated)

        # 3. Add preceding/following references (for linking compatibility)
        validated_blocks = self._add_block_references(validated_blocks)

        return validated_blocks

    def _to_validated_block(
        self, extracted: ExtractedBlock, index: int
    ) -> ValidatedBlock:
        """Convert ExtractedBlock to ValidatedBlock."""
        # Infer kind
        kind = self._infer_block_kind(extracted.type)

        # Generate stable ID
        block_id = extracted.generate_hash()

        # Create ValidatedBlock
        return ValidatedBlock(
            id=block_id,
            kind=kind,
            raw_text=extracted.raw_text,
            validated_text=extracted.raw_text,  # Use raw text as base
            normalized_text=extracted.normalized_text,
            page=0,  # TODO: Map char offsets to pages if possible?
            start_line=0,  # TODO: Map char offsets to lines
            end_line=0,
            is_self_contained=True,  # Extractor only returns self-contained blocks
            tags=extracted.tags,
            validation_errors=[],
            metadata=extracted.metadata or {},
        )

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
        # Prioritize exact match
        if type_lower in type_to_kind:
            return type_to_kind[type_lower]

        # Fallback loop
        for block_type, keywords in BLOCK_TYPE_KEYWORDS.items():
            if block_type in type_to_kind and (
                type_lower == block_type or type_lower in keywords
            ):
                return type_to_kind[block_type]

        return BlockKind.unknown

    def _is_proof_type(self, type_str: str) -> bool:
        """Check if type is a proof."""
        return self._infer_block_kind(type_str) in [
            BlockKind.proof,
            BlockKind.demonstration,
        ]
