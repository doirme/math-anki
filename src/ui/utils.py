"""
Utility functions for Streamlit UI
Helper functions for display formatting and user interactions
"""

from pathlib import Path
from typing import Any, Dict, List

import streamlit as st


def format_block_display(block: Dict[str, Any]) -> str:
    """Format a semantic block for display"""
    kind = block.get("kind", "unknown")
    tags = block.get("tags", [])
    tags_str = ", ".join(tags) if tags else "No tags"

    return f"**Type:** {kind.title()} | **Tags:** {tags_str}"


def show_error_message(message: str, details: str = None):
    """Display a user-friendly error message"""
    st.error(f"❌ {message}")
    if details:
        with st.expander("Error Details"):
            st.code(details)


def show_success_message(message: str):
    """Display a success message"""
    st.success(f"✅ {message}")


def show_info_message(message: str):
    """Display an info message"""
    st.info(f"ℹ️ {message}")


def get_block_type_icon(block_type: str) -> str:
    """Get emoji icon for block type"""
    icons = {
        "theorem": "📐",
        "definition": "📖",
        "proof": "🔍",
        "example": "💡",
        "exercise": "✏️",
        "lemma": "📏",
        "corollary": "📊",
        "proposition": "📝",
        "remark": "💭",
        "unknown": "❓",
    }
    return icons.get(block_type.lower(), "❓")


def format_card_preview(card) -> str:
    """Format a flashcard for preview display"""
    return f"""
**Note Type:** {card.note_type}
**Front:** {card.front[:100]}{'...' if len(card.front) > 100 else ''}
**Back:** {card.back[:100]}{'...' if len(card.back) > 100 else ''}
**Tags:** {' | '.join(card.tags)}
    """.strip()


def ensure_directory(path: str) -> Path:
    """Ensure directory exists and return Path object"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def count_blocks_by_type(blocks: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count blocks grouped by type"""
    counts = {}
    for block in blocks:
        block_type = block.get("kind", "unknown")
        counts[block_type] = counts.get(block_type, 0) + 1
    return counts


def display_block_stats(blocks: List[Dict[str, Any]]):
    """Display statistics about blocks in a nice format"""
    if not blocks:
        st.warning("No blocks to display")
        return

    type_counts = count_blocks_by_type(blocks)

    st.markdown("### Block Statistics")
    cols = st.columns(min(len(type_counts), 4))

    for idx, (block_type, count) in enumerate(type_counts.items()):
        col_idx = idx % 4
        with cols[col_idx]:
            icon = get_block_type_icon(block_type)
            st.metric(f"{icon} {block_type.title()}", count)


def create_download_link(file_path: str, link_text: str = "Download"):
    """Create a download link for a file"""
    if not Path(file_path).exists():
        return None

    with open(file_path, "rb") as f:
        data = f.read()

    filename = Path(file_path).name

    return st.download_button(
        label=link_text, data=data, file_name=filename, mime="application/octet-stream"
    )
