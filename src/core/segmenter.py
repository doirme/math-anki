"""
Compatibility wrapper for segmentation.
This module is kept for backward compatibility with tests and UI.
New code should use BlockCreator directly.
"""

from .block_creator import BlockCreator


def segment(md_text: str):
    """
    Legacy segment function.
    Uses BlockCreator._initial_segmentation to provide the same behavior as before.
    """
    creator = BlockCreator()
    return creator._initial_segmentation(md_text)
