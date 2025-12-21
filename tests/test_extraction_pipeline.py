import json
import unittest
from unittest.mock import patch

from core.block_creator import BlockCreator
from core.block_linker import BlockLinker
from core.enums import BlockKind
from core.semantic_extractor import SemanticExtractor
from core.semantic_schemas import LinkedBlock


class TestExtractionPipeline(unittest.TestCase):
    def setUp(self):
        self.block_creator = BlockCreator()
        self.block_linker = BlockLinker()
        self.semantic_extractor = SemanticExtractor()

    @patch("core.llm_client.LLMClient.generate")
    def test_full_pipeline_flow(self, mock_generate):
        """Test the full flow from raw text to semantic objects with mocked LLM."""

        # 1. Mock ChunkedBlockExtractor response
        # This simulates the first step: extracting blocks from a markdown chunk
        chunk_extraction_response = {
            "blocks": {
                "block_001": {
                    "type": "definition",
                    "normalized_name": "Group",
                    "tags": ["algebra"],
                    "raw_text": "A group (G, *) is a set G with an operation *.",
                    "normalized_text": "Definition: A group (G, *) is a set G with an operation *.",
                    "start_char_offset": 0,
                    "end_char_offset": 50,
                    "term": "Group",
                    "characteristics": ["algebraic structure"],
                },
                "block_002": {
                    "type": "theorem",
                    "normalized_name": "Uniqueness of identity",
                    "tags": ["algebra"],
                    "raw_text": "The identity element of a group is unique.",
                    "normalized_text": "Theorem: The identity element of a group is unique.",
                    "start_char_offset": 60,
                    "end_char_offset": 100,
                    "hypotheses": ["G is a group"],
                    "conclusion": "The identity element is unique",
                },
            }
        }

        # 2. Mock SemanticExtractor responses (if needed)
        # In our optimized version, it might skip LLM calls if metadata is complete.
        # But let's provide a response just in case for complex extraction.
        semantic_response_def = {
            "term": "Group",
            "normalized_term": "Group",
            "statement": "A group (G, *) is a set G with an operation *.",
            "domain_tags": ["algebra"],
            "characteristics": ["algebraic structure"],
            "is_multiple": False,
            "definitions": [],
        }

        # Configure mock_generate side effects
        mock_generate.side_effect = [
            json.dumps(chunk_extraction_response),  # For ChunkedBlockExtractor
            json.dumps({"relationships": []}),  # For BlockLinker (if it calls LLM)
            json.dumps(
                semantic_response_def
            ),  # For SemanticExtractor (if it calls LLM for def)
        ]

        # --- EXECUTION ---

        # Step 1: Create blocks
        text = "A group (G, *) is a set G with an operation *. \n\n The identity element of a group is unique."
        validated_blocks = self.block_creator.create_blocks(text)

        # Verify Step 1
        self.assertEqual(len(validated_blocks), 2)
        self.assertEqual(validated_blocks[0].kind, BlockKind.definition)
        self.assertEqual(validated_blocks[0].metadata["term"], "Group")
        self.assertEqual(validated_blocks[1].kind, BlockKind.theorem)
        self.assertEqual(
            validated_blocks[1].metadata["conclusion"], "The identity element is unique"
        )

        # Step 2: Link blocks
        linked_blocks = self.block_linker.link_blocks(validated_blocks)

        # Verify Step 2
        self.assertEqual(len(linked_blocks), 2)
        self.assertTrue(isinstance(linked_blocks[0], LinkedBlock))

        # Step 3: Semantic Extraction
        semantic_data = self.semantic_extractor.extract(linked_blocks)

        # Verify Step 3
        self.assertEqual(len(semantic_data), 2)

        # Check first extracted item (Definition)
        def_item = next(item for item in semantic_data if item["kind"] == "definition")
        self.assertEqual(def_item["data"].term, "Group")
        self.assertIn("algebra", def_item["data"].domain_tags)

        # Check second extracted item (Theorem)
        thm_item = next(item for item in semantic_data if item["kind"] == "theorem")
        self.assertEqual(thm_item["data"].normalized_name, "Uniqueness of identity")
        self.assertEqual(thm_item["data"].conclusion, "The identity element is unique")

        print("\nPipeline test passed successfully!")


if __name__ == "__main__":
    unittest.main()
