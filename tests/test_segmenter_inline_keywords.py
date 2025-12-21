import pytest

from src.core.block_creator import BlockCreator


def test_inline_bold_keyword_splitting():
    creator = BlockCreator()
    # Simulate the massive block scenario where keywords are stuck to previous text
    text = """
Here is some intro text. **Définition (Fonction paire)**
Let f be a function...
End of definition. **Théorème (Propriété)**
If f is even then...
"""
    # Expected:
    # 1. "Here is some intro text."
    # 2. "**Définition (Fonction paire)**\nLet f be a function...\nEnd of definition."
    # 3. "**Théorème (Propriété)**\nIf f is even then..."
    
    blocks = creator._initial_segmentation(text)
    
    print("DEBUG: Blocks found:")
    for b in blocks:
        print(f"Type: {b['type']}, Text: {repr(b['text'])}")

    # Check types
    types = [b["type"] for b in blocks]
    assert "definition" in types
    assert "theorem" in types
    
    # Check content separation
    def_block = next(b for b in blocks if b["type"] == "definition")
    assert "**Définition" in def_block["text"]
    assert "intro text" not in def_block["text"]
    
    theo_block = next(b for b in blocks if b["type"] == "theorem")
    assert "**Théorème" in theo_block["text"]
    assert "End of definition" not in theo_block["text"]

def test_inline_header_splitting():
    creator = BlockCreator()
    text = """
Some content. ### New Section
Section content.
"""
    blocks = creator._initial_segmentation(text)
    
    # Should split at ###
    header_block = next((b for b in blocks if b["type"] == "header"), None)
    assert header_block is not None
    assert "### New Section" in header_block["text"]
    assert "Some content" not in header_block["text"]

def test_inline_keyword_with_parenthesis():
    creator = BlockCreator()
    # Case: "EXPONENTIELLE ### Définition (Fonction...)"
    # This is tricky because it has both ### and Définition
    # But let's test a simpler case without ### first
    
    text = """
Previous text. Définition (Fonction logarithme)
Logarithm is defined as...
"""
    blocks = creator._initial_segmentation(text)
    
    def_block = next((b for b in blocks if b["type"] == "definition"), None)
    assert def_block is not None
    assert "Définition (Fonction logarithme)" in def_block["text"]
    assert "Previous text" not in def_block["text"]
