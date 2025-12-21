import json
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

# Add src to path so we can import core
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.config import settings
from core.language_detector import detect_language
from core.pdf_to_md import normalize_markdown, pdf_to_markdown
from core.semantic_analyzer import SemanticAnalyzer
from pyinstrument import Profiler

st.set_page_config(
    page_title="Semantic Analysis Debugger", layout="wide", page_icon="🧠"
)

st.title("🧠 Semantic Analysis Pipeline Debugger")

# -------- Sidebar: Configuration --------
st.sidebar.header("⚙️ Configuration")

# Input Source
input_source = st.sidebar.radio(
    "Input Source", ["Upload PDF", "Paste Markdown", "Load Example"], index=1
)

# Pipeline Parameters
st.sidebar.markdown("---")
st.sidebar.subheader("Pipeline Parameters")
context_window = st.sidebar.slider(
    "Context Window", 1, 5, 3, help="Number of blocks to use as context"
)
output_language = st.sidebar.selectbox("Output Language", ["auto", "fr", "en"], index=0)
generate_embeddings = st.sidebar.checkbox("Generate Embeddings", value=False)

# PDF Options
if input_source == "Upload PDF":
    st.sidebar.markdown("---")
    st.sidebar.subheader("PDF Options")
    pdf_method = st.sidebar.selectbox(
        "Conversion Method", ["marker", "mistral_ocr", "docling_modal"], index=0
    )

# -------- Main Content: Input --------
md_text = ""

if input_source == "Upload PDF":
    uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / uploaded.name
            pdf_path.write_bytes(uploaded.read())
            with st.spinner(f"Converting PDF using {pdf_method}..."):
                try:
                    md_text = pdf_to_markdown(
                        pdf_path, prefer=pdf_method, fix_math=False
                    )
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
        "Theorem & Proof (FR)": """# Théorème de Cantor

Le corps $\\mathbb{R}$ n'est pas dénombrable.

## Preuve
On suppose par l'absurde que $\\mathbb{R}$ est dénombrable. On peut alors énumérer ses éléments : $x_1, x_2, \\dots$.
On construit un intervalle fermé $I_1$ ne contenant pas $x_1$. Puis $I_2 \\subset I_1$ ne contenant pas $x_2$, etc.
L'intersection des $I_n$ est non vide (théorème des segments emboîtés), soit $x \\in \\cap I_n$.
Alors $x$ n'est aucun des $x_i$, contradiction.""",
        "Definition (EN)": """# Group Theory

**Definition.** A group is a set $G$ equipped with a binary operation $\\cdot$ such that:
1. Associativity holds.
2. There exists an identity element $e$.
3. Every element has an inverse.

**Example.** The integers $\\mathbb{Z}$ form a group under addition.""",
    }
    selected_example = st.selectbox("Select Example", list(examples.keys()))
    md_text = st.text_area("Content", value=examples[selected_example], height=300)

# -------- Analysis Execution --------
if not md_text:
    st.info("Please provide input content to start the analysis.")
    st.stop()

if st.button("🚀 Run Analysis", type="primary"):
    analyzer = SemanticAnalyzer()

    # Tabs for different phases
    tab1, tab2, tab3, tab4 = st.tabs(
        ["1️⃣ Segmentation & Validation", "2️⃣ Linking", "3️⃣ Extraction", "4️⃣ Indexing"]
    )

    with st.spinner("Running pipeline..."):
        # Detect language
        lang = output_language
        if lang == "auto":
            lang = detect_language(md_text)
        st.caption(f"Processing in language: **{lang}**")

        # Start Profiler
        profiler = Profiler()
        profiler.start()

        # --- Phase 1: Block Creation ---
        validated_blocks = analyzer.block_creator.create_blocks(
            md_text,
            context_window=context_window,
            output_language=lang,
        )

        with tab1:
            st.subheader(f"Phase 1: Found {len(validated_blocks)} Blocks")
            for b in validated_blocks:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{b.kind.value.upper()}**")
                        st.caption(f"ID: `{b.id[:8]}...`")
                        st.caption(
                            f"Type: `{b.kind.value}`"
                        )  # Debug: show the kind value
                        if b.is_self_contained:
                            st.success("✅ Self-contained")
                        else:
                            st.warning(f"⚠️ Missing: {b.missing_context}")

                        # Debug info
                        with st.expander("🔍 Debug Props"):
                            st.json(b.model_dump(exclude={"raw_text"}))
                    with col2:
                        st.markdown(b.validated_text)
                    st.divider()

        # --- Phase 2: Linking ---
        linked_blocks = analyzer.block_linker.link_blocks(
            validated_blocks, output_language=lang
        )

        with tab2:
            st.subheader(f"Phase 2: Linked {len(linked_blocks)} Blocks")
            for lb in linked_blocks:
                if lb.linked_to:
                    st.markdown(
                        f"🔗 **{lb.block.kind.value.title()}** (`{lb.block.id[:8]}`) links to:"
                    )
                    for link in lb.linked_to:
                        st.markdown(
                            f"- `{link['block_id'][:8]}...` via **{link['relation']}**"
                        )
                    st.divider()
                else:
                    st.caption(f"No links for block `{lb.block.id[:8]}`")

        # --- Phase 3: Extraction ---
        extracted = analyzer.extractor.extract(linked_blocks, output_language=lang)

        with tab3:
            st.subheader(f"Phase 3: Extracted {len(extracted)} Items")
            for item in extracted:
                kind = item["kind"]
                data = item["data"]

                with st.expander(
                    f"📄 {kind.title()}: {getattr(data, 'name', 'Unnamed')}",
                    expanded=True,
                ):
                    if hasattr(data, "dict"):
                        st.json(data.model_dump())
                    else:
                        st.json(data)

        # --- Phase 4: Indexing ---
        indexes = []
        for item in extracted:
            index = analyzer.indexer.create_index(item, language=lang)
            indexes.append(index)

        with tab4:
            st.subheader("Phase 4: Search Indexes")
            for idx in indexes:
                st.markdown(f"**{idx.normalized_name or 'Unnamed'}**")
                st.write(f"🏷️ Tags: `{', '.join(idx.domain_tags)}`")
                st.write(f"🔑 Keys: `{', '.join(idx.key_phrases)}`")
                with st.expander("Embedding Text"):
                    st.text(idx.embedding_text)
                st.divider()

        # Stop Profiler and show in terminal
        profiler.stop()
        print("\n" + "=" * 20 + " PIPELINE PROFILE " + "=" * 20)
        profiler.print()
        print("=" * 58 + "\n")
