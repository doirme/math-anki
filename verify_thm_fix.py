import os
import sys
from pathlib import Path

# Use a temporary DB for verification to avoid locks
os.environ["DB_URL"] = "sqlite:///./temp_verify_thm.db"

# Add src to sys.path
sys.path.append(str(Path(__file__).parent / "src"))

from core.cards import make_theorem_cards
from db.models import SemanticBlock
from db.session import get_db_session, init_db
from ui.db_utils import DatabaseManager


def verify():
    print("Initializing DB...")
    init_db()

    db_manager = DatabaseManager()

    # Simulate extraction results for a theorem
    mock_thm_data = {
        "kind": "theorem",
        "name": "Théorème de la borne supérieure",
        "tags": ["analyse", "bornes"],
        "validated_text": "Théorème de la borne supérieure: ...",
        "normalized_text": "Théorème de la borne supérieure: ...",
        "page": 1,
        "metadata": {
            "name": "Théorème de la borne supérieure",
            "hypotheses": ["E est une partie non vide de R", "E est majorée"],
            "conclusion": "E admet une borne supérieure.",
        },
    }

    # 1. Test save_blocks (should create sub-blocks)
    print("Test 1: Saving theorem block to DB...")
    with get_db_session() as session:
        # Create a mock doc first
        from datetime import datetime

        from db.models import Document

        doc = Document(
            title="test_thm", source_path="test.pdf", created_at=datetime.utcnow()
        )
        session.add(doc)
        session.flush()
        doc_id = doc.id

    block_ids = db_manager.save_blocks([mock_thm_data], doc_id)
    block_id = block_ids[0]

    # 2. Verify retrieval
    print("Test 2: Retrieving block and checking sub-block data...")
    retrieved_blocks = db_manager.get_blocks_by_ids([block_id])
    b = retrieved_blocks[0]

    print(f"  Retrieved Name: {b.get('name')}")
    print(f"  Hypotheses Text: {b.get('hypotheses_text')}")
    print(f"  Conclusion Text: {b.get('conclusion_text')}")

    if b.get("hypotheses_text") and "majorée" in b.get("hypotheses_text"):
        print("  ✅ Success: Hypotheses retrieved correctly.")
    else:
        print("  ❌ Failure: Hypotheses missing or incorrect.")

    if b.get("conclusion_text") == "E admet une borne supérieure.":
        print("  ✅ Success: Conclusion retrieved correctly.")
    else:
        print("  ❌ Failure: Conclusion missing or incorrect.")

    # 3. Test card generation (simulate streamlit logic)
    print("Test 3: Simulating card generation...")
    meta = {"deck": "Math", "doc_id": "test"}
    # Construct thm_obj like in streamlit_app.py
    thm_obj = type(
        "obj",
        (object,),
        {
            "name": b.get("name", "Theorem"),
            "hypotheses": type(
                "obj",
                (object,),
                {"summary": b.get("hypotheses_text") or "See block"},
            )(),
            "conclusion": type(
                "obj",
                (object,),
                {"summary": b.get("conclusion_text") or b.get("summary", "")},
            )(),
            "summary": b.get("summary", ""),
            "tags": [type("tag", (object,), {"name": t})() for t in b.get("tags", [])],
            "id": b.get("id", 0),
        },
    )()

    cards = make_theorem_cards(thm_obj, meta)
    for c in cards:
        print(
            f"  Card Type: {c.note_type} | Facet: {'hypotheses' if 'facet::hypotheses' in c.tags else 'other'}"
        )
        if "See block" in c.back:
            print(f"  ❌ Failure: Card back contains 'See block'!")
        elif "E est majorée" in c.back:
            print(f"  ✅ Success: Card back contains actual hypotheses.")

    # Cleanup
    try:
        if os.path.exists("./temp_verify_thm.db"):
            os.remove("./temp_verify_thm.db")
    except:
        pass


if __name__ == "__main__":
    verify()
