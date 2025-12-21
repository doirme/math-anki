import pytest
from core.chunked_extractor import (
    BlockDeduplicator,
    ChunkManager,
    ExtractedBlock,
    TextChunk,
)


def test_chunk_manager_split_simple():
    """Test basic chunking without overflow beyond text length."""
    manager = ChunkManager(chunk_size=100, overlap_size=10)
    text = "A" * 50
    chunks = manager.split_text(text)

    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].start_offset == 0
    assert chunks[0].end_offset == 50
    assert not chunks[0].has_preceding_overlap
    assert not chunks[0].has_following_overlap


def test_chunk_manager_split_with_overlap():
    """Test chunking with overlaps."""
    # Chunk size 50, overlap 10
    manager = ChunkManager(chunk_size=50, overlap_size=10)
    text = "0123456789" * 15  # 150 chars

    chunks = manager.split_text(text)

    # Expected chunks:
    # 0: 0-50 + 10 following overlap = 0-60
    # 1: 50-100 + 10 preceding + 10 following = 40-110
    # 2: 100-150 + 10 preceding = 90-150

    assert len(chunks) == 3

    # Chunk 0
    assert chunks[0].index == 0
    assert chunks[0].start_offset == 0
    assert chunks[0].end_offset == 60
    assert chunks[0].text == text[0:60]
    assert not chunks[0].has_preceding_overlap
    assert chunks[0].has_following_overlap

    # Chunk 1
    assert chunks[1].index == 1
    assert chunks[1].start_offset == 40
    assert chunks[1].end_offset == 110
    assert chunks[1].text == text[40:110]
    assert chunks[1].has_preceding_overlap
    assert chunks[1].has_following_overlap

    # Chunk 2
    assert chunks[2].index == 2
    assert chunks[2].start_offset == 90
    assert chunks[2].end_offset == 150
    assert chunks[2].text == text[90:150]
    assert chunks[2].has_preceding_overlap
    assert not chunks[2].has_following_overlap


def test_deduplicator_exact_overlap():
    """Test deduplication of exact same blocks."""
    deduper = BlockDeduplicator(similarity_threshold=0.9, offset_overlap_threshold=0.7)

    b1 = ExtractedBlock(
        type="theorem",
        normalized_text="Thm 1",
        raw_text="Theorem 1: True",
        start_char_offset=10,
        end_char_offset=50,
        chunk_index=0,
    )

    b2 = ExtractedBlock(
        type="theorem",
        normalized_text="Thm 1",
        raw_text="Theorem 1: True",
        start_char_offset=10,
        end_char_offset=50,
        chunk_index=1,
    )

    deduplicated = deduper.deduplicate([b1, b2])
    assert len(deduplicated) == 1
    assert deduplicated[0] == b1


def test_deduplicator_partial_overlap_semantic():
    """Test deduplication with semantic similarity and offset overlap."""
    deduper = BlockDeduplicator(similarity_threshold=0.8, offset_overlap_threshold=0.5)

    # Block 1 in chunk 0
    b1 = ExtractedBlock(
        type="definition",
        normalized_text="Def of Group",
        raw_text="Definition: A group is...",
        start_char_offset=100,
        end_char_offset=200,
        chunk_index=0,
    )

    # Block 2 in chunk 1 (slightly different but clearly same semantic object)
    b2 = ExtractedBlock(
        type="definition",
        normalized_text="Def of Group",
        raw_text="Definition: A group is a set G...",
        start_char_offset=105,
        end_char_offset=210,
        chunk_index=1,
    )

    deduplicated = deduper.deduplicate([b1, b2])
    assert len(deduplicated) == 1
    # Should keep b2 because it has more raw_text (more context)
    assert deduplicated[0].raw_text == b2.raw_text


def test_deduplicator_no_overlap():
    """Test that distinct blocks are not deduplicated."""
    deduper = BlockDeduplicator()

    b1 = ExtractedBlock(
        type="theorem",
        normalized_text="Thm 1",
        start_char_offset=10,
        end_char_offset=50,
        chunk_index=0,
    )

    b2 = ExtractedBlock(
        type="theorem",
        normalized_text="Thm 2",
        start_char_offset=100,
        end_char_offset=150,
        chunk_index=1,
    )

    deduplicated = deduper.deduplicate([b1, b2])
    assert len(deduplicated) == 2
