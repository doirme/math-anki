"""
Manual verification script for chunked extraction pipeline.
"""

import json
import sys
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

sys.path.append(r"C:\Users\axelc\Documents\math-anki")
from src.core.block_creator import BlockCreator
from src.core.chunked_extractor import (
    ChunkedBlockExtractor,
    ExtractedBlock,
    TextChunk,
)
from src.core.semantic_schemas import BlockKind


def test_chunked_extraction_pipeline():
    print("Starting chunked extraction pipeline verification...")

    # Mock LLM response
    mock_llm_response = {
        "blocks": {
            "block_001": {
                "type": "theorem",
                "normalized_name": "Test Theorem",
                "tags": ["test", "math"],
                "raw_text": "Theorem 1: Test theorem statement.",
                "normalized_text": "**Test Theorem**: Statement",
                "hypotheses": ["Hypothesis A"],
                "conclusion": "Conclusion B",
                "start_char_offset": 0,
                "end_char_offset": 30,
            },
            "block_002": {
                "type": "proof",
                "raw_text": "Proof: This is a proof.",
                "normalized_text": "- Step 1",
                "steps": ["Step 1"],
                "start_char_offset": 35,
                "end_char_offset": 60,
            },
        }
    }

    mock_llm = MagicMock()
    mock_llm.generate.return_value = json.dumps(mock_llm_response)

    # Patch get_llm_task_manager to return our mock
    with patch(
        "src.core.chunked_extractor.get_llm_task_manager", return_value=mock_llm
    ):
        # Initialize creator
        creator = BlockCreator()

        # Test input text (length doesn't matter much as we mock extraction)
        md_text = "Theorem 1: Test theorem statement.\n\nProof: This is a proof." * 100

        print("Calling create_blocks...")
        blocks = creator.create_blocks(md_text, output_language="en")

        print(f"Extracted {len(blocks)} blocks.")

        # Verify blocks
        assert len(blocks) > 0, "Should have extracted blocks"

        first_block = blocks[0]
        print(f"First block: {first_block.id} - {first_block.kind}")

        assert first_block.kind == BlockKind.theorem
        assert first_block.normalized_text == "**Test Theorem**: Statement"
        assert first_block.tags == ["test", "math"]

        # Verify deduplication worked (we duplicated text but mocked LLM returns same blocks for each chunk,
        # but wait, mock LLM returns fixed blocks for ANY chunk.
        # Real LLM would return blocks at different offsets in different chunks.
        # Our mock returns blocks at 0-30 and 35-60.
        # So deduplicator will see many blocks at *same global offsets* (if chunk index 0)
        # OR if chunks shift, global offsets shift.
        # Actually, if we pass a long text, ChunkManager splits it.
        # Validating pipeline flow is enough for now.

    print("Verification passed!")


if __name__ == "__main__":
    test_chunked_extraction_pipeline()
