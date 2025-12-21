import pytest

from src.core.block_creator import BlockCreator


def test_preprocess_adds_newlines():
    creator = BlockCreator()
    text = """
Some content.
# Header 1
More content.
## Header 2
Even more content.
EXPONENTIELLE ### Définition
"""
    # Expected behavior:
    # "Some content." -> "\n\n" -> "# Header 1"
    # "More content." -> "\n\n" -> "## Header 2"
    # "Even more content." -> "\n\n" -> "EXPONENTIELLE ### Définition"
    
    processed = creator._preprocess_text(text)
    
    # Check for double newlines before headers
    assert "Some content.\n\n\n# Header 1" in processed or "Some content.\n\n# Header 1" in processed
    assert "More content.\n\n\n## Header 2" in processed or "More content.\n\n## Header 2" in processed
    assert "Even more content.\n\n\nEXPONENTIELLE ### Définition" in processed or "Even more content.\n\nEXPONENTIELLE ### Définition" in processed

def test_preprocess_idempotent():
    creator = BlockCreator()
    text = """
Some content.

# Header 1
"""
    processed = creator._preprocess_text(text)
    # Should not add extra newlines if already present (or at least not excessive)
    # My implementation adds them if previous line is not empty.
    # If previous line IS empty, it does nothing.
    
    assert processed.strip() == text.strip()
