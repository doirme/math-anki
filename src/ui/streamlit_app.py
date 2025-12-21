"""
Production Streamlit App for Math-Anki
Complete workflow: PDF → Markdown → Blocks → Validation → Cards → .apkg → Database
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st
from core.cards import Flashcard, make_definition_card, make_theorem_cards
from core.config import settings

# Import core modules
from core.pdf_to_md import pdf_to_markdown
from core.semantic_analyzer import SemanticAnalyzer
from db.session import init_db
from exporters.anki_export import export_apkg

# Import database modules
from ui.db_utils import DatabaseManager

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Database initialization failed: {e}")

# Page configuration
st.set_page_config(
    page_title="Math-Anki Production App",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize session state
def init_session_state():
    """Initialize session state variables if they don't exist"""
    defaults = {
        # Processing state
        "pdf_uploaded": False,
        "pdf_path": None,
        "pdf_filename": None,
        "markdown_text": None,
        "raw_blocks": [],
        "validated_blocks": [],
        "invalid_blocks": [],
        "processing_stage": "idle",  # idle, pdf_to_md, segmentation, validation, done
        "error_message": None,
        # Configuration
        "deck_name": "Maths",
        "output_folder": "./data/cards",
        # Cards
        "cards": [],
        "apkg_path": None,
        # Database
        "document_id": None,
        "saved_to_db": False,
        "duplicates_found": [],
        "db_blocks": [],
        # Settings (initialized from .env)
        "settings": {
            "llm_backend": os.getenv("LLM_BACKEND", "openrouter"),
            "llm_model": os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free"),
            "llm_task_validation_model": os.getenv(
                "LLM_TASK_BLOCK_VALIDATION_MODEL", "mistralai/mistral-7b-instruct:free"
            ),
            "llm_task_extraction_model": os.getenv(
                "LLM_TASK_EXTRACTION_MODEL", "mistralai/mistral-7b-instruct:free"
            ),
            "llm_task_linking_model": os.getenv(
                "LLM_TASK_BLOCK_LINKING_MODEL", "mistralai/mistral-7b-instruct:free"
            ),
            "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", ""),
            "cache_dir": os.getenv(
                "MD_CACHE_DIR", "C:/Users/axelc/Documents/math-anki-cache"
            ),
            "db_url": os.getenv("DB_URL", "sqlite:///./data/math_anki.db"),
        },
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# Sidebar
with st.sidebar:
    st.title("🧮 Math-Anki")
    st.markdown("**Production Pipeline**")
    st.markdown("---")

    # Status indicator
    stage_icons = {
        "idle": "⏸️",
        "pdf_to_md": "📄",
        "segmentation": "✂️",
        "validation": "✅",
        "done": "🎉",
    }

    stage = st.session_state.processing_stage
    st.markdown(
        f"### Status: {stage_icons.get(stage, '❓')} {stage.replace('_', ' ').title()}"
    )

    if st.session_state.pdf_filename:
        st.markdown(f"**File:** {st.session_state.pdf_filename}")

    # Statistics
    if st.session_state.validated_blocks:
        st.markdown("### 📊 Statistics")
        st.metric("Validated Blocks", len(st.session_state.validated_blocks))
        st.metric("Invalid Blocks", len(st.session_state.invalid_blocks))
        st.metric("Cards Generated", len(st.session_state.cards))

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "📤 Upload & Configure",
        "⚙️ Processing",
        "📋 Block Review",
        "✏️ Manual Review",
        "📦 Export",
        "💾 Database",
        "🎴 Generate from DB",
        "⚙️ Settings",
    ]
)

# TAB 1: Upload & Configure
with tab1:
    st.header("Upload PDF & Configure")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload a Math PDF",
            type=["pdf"],
            help="Upload your math course or exercise PDF",
        )

        if uploaded_file:
            # Save uploaded file
            tmp_path = Path("./data/raw") / uploaded_file.name
            tmp_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path.write_bytes(uploaded_file.getvalue())

            st.session_state.pdf_uploaded = True
            st.session_state.pdf_path = str(tmp_path)
            st.session_state.pdf_filename = uploaded_file.name

            st.success(f"✅ Uploaded: {uploaded_file.name}")

    with col2:
        st.subheader("Configuration")

        deck_name = st.text_input(
            "Deck Name", value=st.session_state.deck_name, help="Name of the Anki deck"
        )
        st.session_state.deck_name = deck_name

        output_folder = st.text_input(
            "Output Folder",
            value=st.session_state.output_folder,
            help="Folder where .apkg will be saved",
        )
        st.session_state.output_folder = output_folder

    st.markdown("---")

    # Start processing button
    if st.session_state.pdf_uploaded:
        if st.button("🚀 Start Processing", type="primary", use_container_width=True):
            st.session_state.processing_stage = "pdf_to_md"
            st.rerun()

# TAB 2: Processing
with tab2:
    st.header("Processing Pipeline")

    if st.session_state.processing_stage == "idle":
        st.info("Upload a PDF in the first tab to start processing")

    elif st.session_state.processing_stage == "pdf_to_md":
        st.subheader("📄 Converting PDF to Markdown")

        with st.spinner("Extracting text from PDF..."):
            try:
                md_text = pdf_to_markdown(Path(st.session_state.pdf_path))
                st.session_state.markdown_text = md_text

                # Save markdown
                md_path = (
                    Path("./data/markdown")
                    / f"{Path(st.session_state.pdf_filename).stem}.md"
                )
                md_path.parent.mkdir(parents=True, exist_ok=True)
                md_path.write_text(md_text, encoding="utf-8")

                st.success("✅ PDF converted to Markdown")
                st.text_area(
                    "Markdown Preview",
                    md_text[:2000] + "..." if len(md_text) > 2000 else md_text,
                    height=300,
                )

                # Move to next stage
                st.session_state.processing_stage = "segmentation"
                if st.button("Continue to Segmentation"):
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error converting PDF: {str(e)}")
                st.session_state.error_message = str(e)
                st.session_state.processing_stage = "idle"

    elif st.session_state.processing_stage == "segmentation":
        st.subheader("✂️ Segmenting & Analyzing Blocks")

        with st.spinner("Analyzing semantic blocks..."):
            try:
                analyzer = SemanticAnalyzer()

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Creating blocks...")
                progress_bar.progress(0.3)

                # Run analysis
                result = analyzer.analyze(
                    st.session_state.markdown_text, generate_embeddings=False
                )

                status_text.text("Validating blocks...")
                progress_bar.progress(0.6)

                # Separate validated and invalid blocks
                validated = []
                invalid = []

                for block_data in result.get("blocks", []):
                    if block_data.get("is_self_contained", True) and not block_data.get(
                        "validation_errors"
                    ):
                        validated.append(block_data)
                    else:
                        invalid.append(block_data)

                st.session_state.validated_blocks = validated
                st.session_state.invalid_blocks = invalid

                progress_bar.progress(1.0)
                status_text.text("✅ Analysis complete!")

                st.success(
                    f"Found {len(validated)} validated blocks and {len(invalid)} blocks needing review"
                )

                # Move to next stage
                st.session_state.processing_stage = "done"
                if st.button("View Results"):
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.session_state.error_message = str(e)
                st.session_state.processing_stage = "idle"

    elif st.session_state.processing_stage == "done":
        st.success("🎉 Processing Complete!")
        st.markdown("Navigate to **Block Review** or **Export** tabs to continue")

        # Database save option
        st.markdown("---")
        st.subheader("💾 Save to Database")

        if not st.session_state.saved_to_db:
            st.info(
                "💡 Save validated blocks to database for duplicate detection across multiple sources"
            )

            if st.button(
                "💾 Save to Database with Embeddings",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Saving to database and generating embeddings..."):
                    try:
                        db_manager = DatabaseManager()

                        # Save document
                        doc_id = db_manager.save_document(
                            st.session_state.pdf_path, st.session_state.markdown_text
                        )
                        st.session_state.document_id = doc_id

                        # Save blocks with embeddings
                        progress_text = st.empty()
                        progress_text.text("Generating embeddings...")

                        block_ids = db_manager.save_blocks(
                            st.session_state.validated_blocks,
                            doc_id,
                            generate_embeddings=True,  # ✅ Embeddings enabled for DB
                        )

                        progress_text.text("Checking for duplicates...")

                        # Check for duplicates
                        duplicates = db_manager.find_duplicates(
                            st.session_state.validated_blocks
                        )
                        st.session_state.duplicates_found = duplicates

                        st.session_state.saved_to_db = True

                        st.success(f"✅ Saved {len(block_ids)} blocks to database!")

                        if duplicates:
                            st.warning(
                                f"⚠️ Found {len(duplicates)} potential duplicates. "
                                "Check the Database tab to review."
                            )

                    except Exception as e:
                        st.error(f"❌ Database save failed: {str(e)}")
                        st.exception(e)
        else:
            st.success("✅ Already saved to database")
            if st.session_state.duplicates_found:
                st.info(
                    f"🔍 {len(st.session_state.duplicates_found)} duplicates found - see Database tab"
                )

# TAB 3: Block Review
with tab3:
    st.header("Validated Blocks")

    if not st.session_state.validated_blocks:
        st.info("No validated blocks yet. Process a PDF first.")
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_type = st.selectbox(
                "Filter by Type",
                ["All"]
                + list(
                    set(
                        b.get("kind", "unknown")
                        for b in st.session_state.validated_blocks
                    )
                ),
            )

        with col2:
            st.metric("Total Blocks", len(st.session_state.validated_blocks))

        with col3:
            if st.button("Refresh"):
                st.rerun()

        # Display blocks
        blocks_to_show = st.session_state.validated_blocks
        if filter_type != "All":
            blocks_to_show = [b for b in blocks_to_show if b.get("kind") == filter_type]

        for idx, block in enumerate(blocks_to_show):
            with st.expander(
                f"Block {idx + 1}: {block.get('kind', 'unknown')} - {block.get('tags', [])}"
            ):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("**Raw Text:**")
                    st.text_area(
                        "raw",
                        block.get("validated_text", ""),
                        height=150,
                        key=f"raw_{idx}",
                        label_visibility="collapsed",
                    )

                with col_b:
                    st.markdown("**Normalized Text:**")
                    st.text_area(
                        "norm",
                        block.get("normalized_text", ""),
                        height=150,
                        key=f"norm_{idx}",
                        label_visibility="collapsed",
                    )

                st.markdown(f"**Tags:** {', '.join(block.get('tags', []))}")
                st.markdown(
                    f"**Self-contained:** {'✅' if block.get('is_self_contained') else '❌'}"
                )

# TAB 4: Manual Review
with tab4:
    st.header("Manual Review & Editing")

    if not st.session_state.invalid_blocks:
        st.success("🎉 No blocks need manual review!")
    else:
        st.warning(f"⚠️ {len(st.session_state.invalid_blocks)} blocks need review")

        for idx, block in enumerate(st.session_state.invalid_blocks):
            with st.expander(
                f"Invalid Block {idx + 1}: {block.get('kind', 'unknown')}"
            ):
                st.markdown(
                    f"**Issues:** {', '.join(block.get('missing_context', []))}"
                )

                edited_text = st.text_area(
                    "Edit Block Text",
                    value=block.get("validated_text", ""),
                    height=200,
                    key=f"edit_invalid_{idx}",
                )

                col_x, col_y = st.columns(2)

                with col_x:
                    if st.button("✅ Mark as Valid", key=f"validate_{idx}"):
                        # Move to validated
                        block["validated_text"] = edited_text
                        block["is_self_contained"] = True
                        st.session_state.validated_blocks.append(block)
                        st.session_state.invalid_blocks.pop(idx)
                        st.success("Block validated!")
                        st.rerun()

                with col_y:
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.invalid_blocks.pop(idx)
                        st.rerun()

# TAB 5: Export
with tab5:
    st.header("Export Anki Package")

    if not st.session_state.validated_blocks:
        st.info("No validated blocks to export. Process a PDF first.")
    else:
        col_export1, col_export2 = st.columns([1, 1])

        with col_export1:
            st.subheader("Generate Cards")

            if st.button(
                "🎴 Generate Flashcards", type="primary", use_container_width=True
            ):
                with st.spinner("Generating flashcards..."):
                    cards = []
                    meta = {
                        "deck": st.session_state.deck_name,
                        "doc_id": Path(st.session_state.pdf_filename).stem
                        if st.session_state.pdf_filename
                        else "unknown",
                    }

                    # Generate cards from validated blocks
                    for block in st.session_state.validated_blocks:
                        # This is simplified - you'll need to adapt based on your actual block structure
                        kind = block.get("kind", "")

                        # Convert to expected format
                        if kind == "definition":
                            defi_obj = type(
                                "obj",
                                (object,),
                                {
                                    "name": block.get("tags", ["Definition"])[0]
                                    if block.get("tags")
                                    else "Definition",
                                    "summary": block.get("normalized_text", ""),
                                    "tags": [
                                        type("tag", (object,), {"name": t})()
                                        for t in block.get("tags", [])
                                    ],
                                },
                            )()
                            cards.append(make_definition_card(defi_obj, meta))

                        elif kind == "theorem":
                            # Create mock objects for theorem
                            thm_obj = type(
                                "obj",
                                (object,),
                                {
                                    "name": block.get("tags", ["Theorem"])[0]
                                    if block.get("tags")
                                    else "Theorem",
                                    "hypotheses": type(
                                        "obj", (object,), {"summary": "See block"}
                                    )(),
                                    "conclusion": type(
                                        "obj",
                                        (object,),
                                        {"summary": block.get("normalized_text", "")},
                                    )(),
                                    "summary": block.get("normalized_text", ""),
                                    "tags": [
                                        type("tag", (object,), {"name": t})()
                                        for t in block.get("tags", [])
                                    ],
                                },
                            )()
                            cards.extend(make_theorem_cards(thm_obj, meta))

                    st.session_state.cards = cards
                    st.success(f"✅ Generated {len(cards)} flashcards!")

            # Preview cards
            if st.session_state.cards:
                st.markdown("### Card Preview")
                for i, card in enumerate(st.session_state.cards[:5]):
                    with st.expander(f"Card {i+1}: {card.note_type}"):
                        st.markdown(f"**Front:** {card.front}")
                        st.markdown(f"**Back:** {card.back}")
                        st.code(" ".join(card.tags), language="")

                if len(st.session_state.cards) > 5:
                    st.info(f"... and {len(st.session_state.cards) - 5} more cards")

        with col_export2:
            st.subheader("Export .apkg")

            if st.session_state.cards:
                if st.button(
                    "📦 Export to .apkg", type="primary", use_container_width=True
                ):
                    try:
                        # Create output path
                        output_dir = Path(st.session_state.output_folder)
                        output_dir.mkdir(parents=True, exist_ok=True)

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        apkg_filename = f"{st.session_state.deck_name}_{timestamp}.apkg"
                        apkg_path = output_dir / apkg_filename

                        # Export
                        export_apkg(
                            st.session_state.cards,
                            st.session_state.deck_name,
                            str(apkg_path),
                        )

                        st.session_state.apkg_path = str(apkg_path)
                        st.success(f"✅ Exported to: {apkg_path}")

                        # Download button
                        with open(apkg_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download .apkg",
                                data=f.read(),
                                file_name=apkg_filename,
                                mime="application/octet-stream",
                                use_container_width=True,
                            )

                    except Exception as e:
                        st.error(f"❌ Export failed: {str(e)}")

    # How-to guide
    st.markdown("---")
    st.subheader("📖 How to Import Cards into Anki")

    with st.expander("Step-by-Step Instructions"):
        st.markdown("""
        ### Import Process
        
        1. **Download** the generated `.apkg` file using the button above
        2. **Open Anki** desktop application on your computer
        3. Click **File → Import** from the menu
        4. **Select** the downloaded `.apkg` file
        5. **Confirm** the import settings (deck name, etc.)
        6. Cards will be imported into the specified deck
        
        ### Syncing to Mobile
        
        - Create an AnkiWeb account if you don't have one
        - In Anki desktop: **Tools → Preferences → Network → Sync**
        - On mobile: Sign in with your AnkiWeb account and sync
        
        ### Tips for Effective Learning
        
        - Review your cards regularly for best retention
        - Use Anki's built-in scheduling algorithm to optimize learning
        - You can edit or add cards directly in Anki after import
        - Consider using tags to organize cards by topic or difficulty
        """)


# TAB 6: Database Management
with tab6:
    st.header("💾 Database Management")

    db_manager = DatabaseManager()

    # Overview statistics
    col_db1, col_db2, col_db3 = st.columns(3)

    with col_db1:
        all_blocks = db_manager.get_all_blocks()
        st.metric("Total Blocks in DB", len(all_blocks))

    with col_db2:
        if st.session_state.saved_to_db:
            st.metric("Current Session Saved", "✅ Yes")
        else:
            st.metric("Current Session Saved", "❌ No")

    with col_db3:
        st.metric("Duplicates Found", len(st.session_state.duplicates_found))

    st.markdown("---")

    # Duplicate detection and resolution
    if st.session_state.duplicates_found:
        st.subheader("🔍 Duplicate Detection Results")
        st.warning(
            f"Found {len(st.session_state.duplicates_found)} potential duplicates"
        )

        for idx, (new_block, similar_blocks) in enumerate(
            st.session_state.duplicates_found
        ):
            with st.expander(
                f"Duplicate Group {idx + 1}: {new_block.get('kind', 'unknown')} - {new_block.get('tags', [])}"
            ):
                col_new, col_similar = st.columns(2)

                with col_new:
                    st.markdown("### New Block")
                    st.markdown(f"**Type:** {new_block.get('kind', 'unknown')}")
                    st.markdown(f"**Tags:** {', '.join(new_block.get('tags', []))}")
                    st.text_area(
                        "Content",
                        new_block.get("normalized_text", "")[:300],
                        height=200,
                        key=f"new_{idx}",
                    )

                with col_similar:
                    st.markdown("### Similar Existing Blocks")
                    for sim_idx, sim_block in enumerate(similar_blocks):
                        st.markdown(
                            f"**Block ID {sim_block['id']}** - {sim_block['name']}"
                        )
                        st.text_area(
                            f"Existing {sim_idx +1}",
                            sim_block["summary"][:200],
                            height=100,
                            key=f"sim_{idx}_{sim_idx}",
                        )

                # Resolution actions
                st.markdown("### Resolution Actions")
                col_action1, col_action2, col_action3 = st.columns(3)

                with col_action1:
                    if st.button("✅ Keep Both", key=f"keep_both_{idx}"):
                        st.success("Keeping both blocks as separate entities")
                        # Remove from duplicates list
                        st.session_state.duplicates_found.pop(idx)
                        st.rerun()

                with col_action2:
                    if st.button("🗑️ Discard New", key=f"discard_new_{idx}"):
                        st.info("Discarding new block (keeping existing)")
                        st.session_state.duplicates_found.pop(idx)
                        st.rerun()

                with col_action3:
                    if similar_blocks and st.button("🔀 Merge", key=f"merge_{idx}"):
                        try:
                            # Merge logic - keep first existing, delete others
                            keep_id = similar_blocks[0]["id"]
                            delete_ids = [b["id"] for b in similar_blocks[1:]]
                            db_manager.merge_blocks(keep_id, delete_ids)
                            st.success(f"Merged blocks into ID {keep_id}")
                            st.session_state.duplicates_found.pop(idx)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Merge failed: {e}")

    else:
        if st.session_state.saved_to_db:
            st.success("✅ No duplicates found!")
        else:
            st.info("💡 Process a PDF and save to database to check for duplicates")

    st.markdown("---")

    # Browse all blocks in database
    st.subheader("📚 Browse Database Blocks")

    filter_kind = st.selectbox(
        "Filter by Type",
        ["All"] + ["theorem", "definition", "proof", "example", "exercise", "lemma"],
    )

    if st.button("🔄 Refresh Block List"):
        if filter_kind == "All":
            st.session_state.db_blocks = db_manager.get_all_blocks()
        else:
            st.session_state.db_blocks = db_manager.get_all_blocks(kind=filter_kind)

    if st.session_state.db_blocks:
        st.info(f"Showing {len(st.session_state.db_blocks)} blocks")

        for db_block in st.session_state.db_blocks[:20]:  # Limit to 20 for performance
            with st.expander(
                f"{db_block['kind']} - {db_block['name']} (ID: {db_block['id']})"
            ):
                st.markdown(f"**Tags:** {', '.join(db_block['tags'])}")
                st.markdown(f"**Created:** {db_block['created_at']}")
                st.text_area(
                    "Summary",
                    db_block["summary"][:400],
                    height=150,
                    key=f"db_block_{db_block['id']}",
                )

                if st.button(
                    f"🗑️ Delete Block {db_block['id']}",
                    key=f"delete_db_{db_block['id']}",
                ):
                    try:
                        db_manager.delete_block(db_block["id"])
                        st.success("Block deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Delete failed: {e}")

        if len(st.session_state.db_blocks) > 20:
            st.warning(
                f"... and {len(st.session_state.db_blocks) - 20} more blocks. Refine filter to see more."
            )


# TAB 7: Generate from Database
with tab7:
    st.header("🎴 Generate Anki Cards from Database")

    st.markdown(
        "Create Anki decks from previously processed PDFs without re-uploading."
    )

    db_manager = DatabaseManager()

    # Initialize filter state
    if "filtered_blocks" not in st.session_state:
        st.session_state.filtered_blocks = []
    if "selected_block_ids" not in st.session_state:
        st.session_state.selected_block_ids = []

    # Filters section
    st.subheader("🔍 Filter Blocks")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        # Block type filter
        all_types = [
            "theorem",
            "definition",
            "proof",
            "example",
            "exercise",
            "lemma",
            "corollary",
        ]
        selected_types = st.multiselect(
            "Block Types", all_types, help="Select one or more block types"
        )

        # Tag filter
        all_tags = db_manager.get_all_tags()
        selected_tags = st.multiselect(
            "Tags (must have ALL selected)",
            all_tags,
            help="Blocks must have all selected tags",
        )

    with col_f2:
        # Document/PDF filter
        all_docs = db_manager.get_all_documents()
        doc_options = {f"{d['title']} (ID: {d['id']})": d["id"] for d in all_docs}
        selected_doc_names = st.multiselect(
            "Source PDFs", list(doc_options.keys()), help="Filter by source document"
        )
        selected_doc_ids = [doc_options[name] for name in selected_doc_names]

        # Text search
        search_text = st.text_input(
            "Search Text",
            placeholder="Search in names and summaries...",
            help="Search for specific keywords",
        )

    # Apply filters button
    if st.button("🔍 Apply Filters", type="primary", use_container_width=True):
        with st.spinner("Filtering database..."):
            filtered = db_manager.filter_blocks(
                kinds=selected_types if selected_types else None,
                tags=selected_tags if selected_tags else None,
                document_ids=selected_doc_ids if selected_doc_ids else None,
                search_text=search_text if search_text else None,
            )
            st.session_state.filtered_blocks = filtered
            st.session_state.selected_block_ids = []  # Reset selection

    st.markdown("---")

    # Results section
    if st.session_state.filtered_blocks:
        st.subheader(
            f"📊 Results: {len(st.session_state.filtered_blocks)} blocks found"
        )

        # Select all / Deselect all
        col_sel1, col_sel2, col_sel3 = st.columns(3)

        with col_sel1:
            if st.button("✅ Select All"):
                st.session_state.selected_block_ids = [
                    b["id"] for b in st.session_state.filtered_blocks
                ]
                st.rerun()

        with col_sel2:
            if st.button("❌ Deselect All"):
                st.session_state.selected_block_ids = []
                st.rerun()

        with col_sel3:
            st.metric("Selected", len(st.session_state.selected_block_ids))

        st.markdown("---")

        # Display blocks with checkboxes
        for block in st.session_state.filtered_blocks:
            is_selected = block["id"] in st.session_state.selected_block_ids

            col_check, col_content = st.columns([1, 20])

            with col_check:
                if st.checkbox("", value=is_selected, key=f"select_{block['id']}"):
                    if block["id"] not in st.session_state.selected_block_ids:
                        st.session_state.selected_block_ids.append(block["id"])
                else:
                    if block["id"] in st.session_state.selected_block_ids:
                        st.session_state.selected_block_ids.remove(block["id"])

            with col_content:
                with st.expander(
                    f"{block['kind']} - {block['name']} (ID: {block['id']})"
                ):
                    col_info, col_sources = st.columns(2)

                    with col_info:
                        st.markdown(f"**Tags:** {', '.join(block['tags'])}")
                        st.markdown(f"**Created:** {block['created_at']}")
                        st.text_area(
                            "Summary",
                            block["summary"][:300],
                            height=150,
                            key=f"gen_summary_{block['id']}",
                        )

                    with col_sources:
                        st.markdown("**Source Documents:**")
                        if block.get("sources"):
                            for source in block["sources"]:
                                st.markdown(f"- {source['title']}")
                        else:
                            st.info("No source information available")

                        st.metric("Referenced by", block.get("source_count", 0))

        st.markdown("---")

        # Generation section
        if st.session_state.selected_block_ids:
            st.subheader("🎴 Generate Anki Deck")

            col_gen1, col_gen2 = st.columns(2)

            with col_gen1:
                deck_name_from_db = st.text_input(
                    "Deck Name", value="Maths::FromDB", key="deck_name_from_db"
                )

            with col_gen2:
                output_folder_from_db = st.text_input(
                    "Output Folder", value="./data/cards", key="output_folder_from_db"
                )

            if st.button(
                "🎴 Generate .apkg from Selected Blocks",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner(
                    f"Generating {len(st.session_state.selected_block_ids)} cards..."
                ):
                    try:
                        # Retrieve full block data
                        blocks_to_export = db_manager.get_blocks_by_ids(
                            st.session_state.selected_block_ids
                        )

                        # Generate cards
                        cards = []
                        meta = {"deck": deck_name_from_db, "doc_id": "database_export"}

                        for block in blocks_to_export:
                            kind = block.get("kind", "")

                            # Convert to expected format (same as in Export tab)
                            if kind == "definition":
                                defi_obj = type(
                                    "obj",
                                    (object,),
                                    {
                                        "name": block.get("name", "Definition"),
                                        "summary": block.get("summary", ""),
                                        "tags": [
                                            type("tag", (object,), {"name": t})()
                                            for t in block.get("tags", [])
                                        ],
                                    },
                                )()
                                cards.append(make_definition_card(defi_obj, meta))

                            elif kind == "theorem":
                                thm_obj = type(
                                    "obj",
                                    (object,),
                                    {
                                        "name": block.get("name", "Theorem"),
                                        "hypotheses": type(
                                            "obj", (object,), {"summary": "See block"}
                                        )(),
                                        "conclusion": type(
                                            "obj",
                                            (object,),
                                            {"summary": block.get("summary", "")},
                                        )(),
                                        "summary": block.get("summary", ""),
                                        "tags": [
                                            type("tag", (object,), {"name": t})()
                                            for t in block.get("tags", [])
                                        ],
                                    },
                                )()
                                cards.extend(make_theorem_cards(thm_obj, meta))

                        # Export to .apkg
                        output_dir = Path(output_folder_from_db)
                        output_dir.mkdir(parents=True, exist_ok=True)

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        apkg_filename = (
                            f"{deck_name_from_db.replace('::', '_')}_{timestamp}.apkg"
                        )
                        apkg_path = output_dir / apkg_filename

                        export_apkg(cards, deck_name_from_db, str(apkg_path))

                        st.success(f"✅ Generated {len(cards)} cards!")

                        # Download button
                        with open(apkg_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download .apkg",
                                data=f.read(),
                                file_name=apkg_filename,
                                mime="application/octet-stream",
                                use_container_width=True,
                            )

                    except Exception as e:
                        st.error(f"❌ Card generation failed: {str(e)}")
                        st.exception(e)
        else:
            st.info("💡 Select blocks above to generate cards")

    else:
        st.info("💡 Apply filters above to find blocks in the database")


# TAB 8: Settings
with tab8:
    st.header("Settings & Configuration")

    st.markdown(
        "Configure LLM models, API keys, and directories. Changes are saved to session state."
    )

    with st.form("settings_form"):
        st.subheader("LLM Configuration")

        llm_backend = st.selectbox(
            "LLM Backend",
            ["openrouter", "ollama", "openai"],
            index=["openrouter", "ollama", "openai"].index(
                st.session_state.settings["llm_backend"]
            ),
        )

        col_s1, col_s2 = st.columns(2)

        with col_s1:
            llm_model = st.text_input(
                "Default LLM Model", value=st.session_state.settings["llm_model"]
            )

            validation_model = st.text_input(
                "Validation Model",
                value=st.session_state.settings["llm_task_validation_model"],
            )

        with col_s2:
            extraction_model = st.text_input(
                "Extraction Model",
                value=st.session_state.settings["llm_task_extraction_model"],
            )

            linking_model = st.text_input(
                "Linking Model",
                value=st.session_state.settings["llm_task_linking_model"],
            )

        st.subheader("API Keys")

        openrouter_key = st.text_input(
            "OpenRouter API Key",
            value=st.session_state.settings["openrouter_api_key"],
            type="password",
        )

        st.subheader("Directories")

        cache_dir = st.text_input(
            "Cache Directory", value=st.session_state.settings["cache_dir"]
        )

        db_url = st.text_input(
            "Database URL", value=st.session_state.settings["db_url"]
        )

        submitted = st.form_submit_button("💾 Save Settings", use_container_width=True)

        if submitted:
            st.session_state.settings.update(
                {
                    "llm_backend": llm_backend,
                    "llm_model": llm_model,
                    "llm_task_validation_model": validation_model,
                    "llm_task_extraction_model": extraction_model,
                    "llm_task_linking_model": linking_model,
                    "openrouter_api_key": openrouter_key,
                    "cache_dir": cache_dir,
                    "db_url": db_url,
                }
            )
            st.success("✅ Settings saved to session!")
