import json
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

# Add src to path so we can import core
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.chunked_extractor import (
    BlockDeduplicator,
    ChunkedBlockExtractor,
    ChunkManager,
    ExtractedBlock,
)
from core.config import settings
from core.language_detector import detect_language
from core.pdf_to_md import normalize_markdown, pdf_to_markdown
from core.semantic_analyzer import SemanticAnalyzer

st.set_page_config(
    page_title="Chunked Strategy Debugger", layout="wide", page_icon="🧩"
)

st.title("🧩 Chunked Strategy Debugger")
st.markdown(
    "Inspect how the document is chunked, how LLM extracts blocks, and how deduplication works."
)

# -------- Sidebar: Configuration --------
st.sidebar.header("⚙️ Configuration")

# Input Source
input_source = st.sidebar.radio(
    "Input Source", ["Upload PDF", "Paste Markdown", "Load Example"], index=1
)

# Strategy Parameters
st.sidebar.markdown("---")
st.sidebar.subheader("Strategy Parameters")
chunk_size = st.sidebar.number_input(
    "Chunk Size (chars)", value=settings.chunk_size_chars, step=1000
)
overlap_size = st.sidebar.number_input(
    "Overlap Size (chars)", value=settings.chunk_overlap_chars, step=500
)
sim_threshold = st.sidebar.slider(
    "Similarity Threshold", 0.1, 1.0, settings.dedupe_similarity_threshold
)
overlap_threshold = st.sidebar.slider(
    "Offset Overlap Threshold", 0.1, 1.0, settings.dedupe_offset_overlap_threshold
)

output_language = st.sidebar.selectbox("Output Language", ["auto", "fr", "en"], index=0)

# -------- Main Content: Input --------
md_text = ""

if input_source == "Upload PDF":
    uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / uploaded.name
            pdf_path.write_bytes(uploaded.read())
            with st.spinner("Converting PDF..."):
                try:
                    md_text = pdf_to_markdown(pdf_path, prefer="marker", fix_math=False)
                    md_text = normalize_markdown(md_text or "")
                    st.success(f"Conversion successful! ({len(md_text)} chars)")
                except Exception as e:
                    st.error(f"Conversion failed: {e}")

elif input_source == "Paste Markdown":
    md_text = st.text_area(
        "Paste Markdown Content", height=300, placeholder="# Title\n\nTheorem 1..."
    )

elif input_source == "Load Example":
    examples = {
        "Long Document (Mocked)": "### Chapter 1\n\nDefinition 1: A set is...\n\n"
        + "Lorem ipsum... " * 500
        + "\n\nTheorem 1: The set of... is infinite.\n\n"
        + "More text... " * 500,
    }
    selected_example = st.selectbox("Select Example", list(examples.keys()))
    md_text = st.text_area("Content", value=examples[selected_example], height=300)

if not md_text:
    st.info("Please provide input content to start the analysis.")
    st.stop()

if st.button("🚀 Run Chunked Analysis", type="primary"):
    # Initialize components with sidebar overrides
    manager = ChunkManager(chunk_size=chunk_size, overlap_size=overlap_size)
    deduper = BlockDeduplicator(
        similarity_threshold=sim_threshold, offset_overlap_threshold=overlap_threshold
    )
    extractor = (
        ChunkedBlockExtractor()
    )  # Note: uses global settings but we can call its methods

    # Override settings for the duration of this run if needed (global settings can't be easily overridden per call without refactoring)
    # But for now, we'll use the components directly

    st.markdown("---")

    # Tabs
    tab_chunks, tab_raw, tab_dedupe, tab_final = st.tabs(
        [
            "📄 1. Chunks",
            "🤖 2. Raw Extraction",
            "✂️ 3. Deduplication",
            "📦 4. Final Blocks",
        ]
    )

    with st.spinner("Processing chunks..."):
        # 1. Chunking
        chunks = manager.split_text(md_text)

        with tab_chunks:
            st.subheader(f"Split into {len(chunks)} Chunks")
            for c in chunks:
                with st.expander(
                    f"Chunk {c.index} | Global: {c.start_offset}:{c.end_offset} | Len: {len(c.text)}"
                ):
                    st.code(c.text, language="markdown")
                    st.caption(
                        f"Preceding Overlap: {c.has_preceding_overlap} | Following Overlap: {c.has_following_overlap}"
                    )

        # 2. Raw Extraction (One by one)
        all_raw_blocks = []

        with tab_raw:
            st.subheader("LLM Extraction results per chunk")
            lang = output_language
            if lang == "auto":
                lang = detect_language(md_text)

            for c in chunks:
                with st.status(f"Processing Chunk {c.index}...", expanded=False):
                    try:
                        chunk_blocks = extractor._process_chunk(c, output_language=lang)
                        all_raw_blocks.extend(chunk_blocks)

                        st.write(f"Found {len(chunk_blocks)} blocks.")
                        for rb in chunk_blocks:
                            st.write(f"- [{rb.type.upper()}] {rb.normalized_name}")
                            with st.expander("Show Details"):
                                st.json(rb.__dict__)
                    except Exception as e:
                        st.error(f"Error in chunk {c.index}: {e}")

        # 3. Deduplication Visualizer
        with tab_dedupe:
            st.subheader("Merging Overlapping Blocks")

            # We want to show which blocks were identified as duplicates
            # Since the deduplicator just returns the final list, we'll wrap it or look at its logic

            sorted_blocks = sorted(all_raw_blocks, key=lambda b: b.start_char_offset)
            to_keep = []
            removed = []
            matches = []  # List of (kept_idx, removed_idx, reason)

            skip_indices = set()
            for i, block1 in enumerate(sorted_blocks):
                if i in skip_indices:
                    continue

                is_duplicate = False
                for j in range(i + 1, len(sorted_blocks)):
                    if j in skip_indices:
                        continue

                    block2 = sorted_blocks[j]

                    # Same logic as deduper
                    if abs(block1.chunk_index - block2.chunk_index) <= 1:
                        if deduper._offsets_overlap(block1, block2):
                            if deduper._are_semantically_similar(block1, block2):
                                # Duplicate found!
                                if len(block2.raw_text) > len(block1.raw_text):
                                    matches.append(
                                        (
                                            j,
                                            i,
                                            "Semantic + Offset overlap (b2 is longer)",
                                        )
                                    )
                                    is_duplicate = True
                                    skip_indices.add(i)
                                    removed.append(block1)
                                    break
                                else:
                                    matches.append(
                                        (
                                            i,
                                            j,
                                            "Semantic + Offset overlap (b1 is longer)",
                                        )
                                    )
                                    skip_indices.add(j)
                                    removed.append(block2)

                if not is_duplicate:
                    to_keep.append(block1)

            st.write(
                f"Total Raw: {len(all_raw_blocks)} | Deduplicated: {len(to_keep)} | Removed: {len(removed)}"
            )

            if matches:
                st.markdown("### Match Details")
                for kept_idx, rem_idx, reason in matches:
                    k = sorted_blocks[kept_idx]
                    r = sorted_blocks[rem_idx]
                    with st.expander(
                        f"Match: {k.normalized_name} (Chunk {k.chunk_index}) and {r.normalized_name} (Chunk {r.chunk_index})"
                    ):
                        st.write(f"**Reason:** {reason}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.info("**KEPT**")
                            st.write(k.raw_text)
                        with c2:
                            st.error("**REMOVED**")
                            st.write(r.raw_text)
            else:
                st.info("No duplicates found during merge.")

        # 4. Final Blocks
        with tab_final:
            st.subheader("Final Validated Blocks")
            # Convert to ValidatedBlocks for preview
            creator = SemanticAnalyzer().block_creator
            final_validated = [
                creator._to_validated_block(b, idx) for idx, b in enumerate(to_keep)
            ]

            for b in final_validated:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{b.kind.value.upper()}**")
                        st.caption(f"ID: `{b.id[:8]}...`")
                        st.caption(f"Tags: `{', '.join(b.tags)}`")
                    with col2:
                        st.markdown(b.normalized_text or b.raw_text)
                    st.divider()
