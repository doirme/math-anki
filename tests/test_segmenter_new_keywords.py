import pytest

from src.core.block_creator import BlockCreator


def test_plural_keywords():
    creator = BlockCreator()
    text = """
Some intro text.

Examples
Here are some examples:
1. Example A
2. Example B

Exemples
Voici des exemples:
1. Exemple A
2. Exemple B
"""
    blocks = creator._simple_segment(text)
    
    # Filter out empty blocks if any
    blocks = [b for b in blocks if b["text"].strip()]
    
    # Expected:
    # 1. Intro text
    # 2. Examples block
    # 3. Exemples block
    
    assert len(blocks) >= 3
    
    # Check types
    types = [b["type"] for b in blocks]
    assert "example" in types
    
    # Find the blocks
    examples_block = next(b for b in blocks if "Examples" in b["text"])
    exemples_block = next(b for b in blocks if "Exemples" in b["text"])
    
    assert examples_block["type"] == "example"
    assert exemples_block["type"] == "example"

def test_embedded_header_segmentation():
    creator = BlockCreator()
    text = """
Previous content.

EXPONENTIELLE ### Définition-théorème (Fonction logarithme)
La fonction logarithme est définie comme...

Next content.
"""
    blocks = creator._simple_segment(text)
    blocks = [b for b in blocks if b["text"].strip()]
    
    # Should split at "EXPONENTIELLE..."
    # And "EXPONENTIELLE..." should be identified as definition because it contains "Définition"
    
    header_block = next(b for b in blocks if "EXPONENTIELLE" in b["text"])
    assert header_block["type"] == "definition"
    
    # Verify it was split from "Previous content"
    assert "Previous content" not in header_block["text"]
