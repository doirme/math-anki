import os
import sys
from pathlib import Path

# Use a temporary DB for verification
os.environ["DB_URL"] = "sqlite:///./temp_verify_meta.db"

# Add src to sys.path
sys.path.append(str(Path(__file__).parent / "src"))

from db.models import SemanticBlock
from db.session import get_db_session, init_db
from ui.db_utils import DatabaseManager


def verify():
    print("Initializing DB...")
    init_db()

    db_manager = DatabaseManager()

    # Mock data with rich metadata
    mock_data = {
        "kind": "proof",
        "name": "Preuve de l'irrationnalité de sqrt(2)",
        "tags": ["arithmétique"],
        "validated_text": "Supposons p/q = sqrt(2)...",
        "normalized_text": "Supposons p/q = sqrt(2)...",
        "page": 2,
        "metadata": {
            "steps": [
                "Supposons par l'absurde que sqrt(2) = p/q",
                "Alors 2q^2 = p^2",
                "Donc p^2 est pair, donc p est pair",
                "...",
            ],
            "uses_theorems": ["Lemme d'Euclide"],
        },
    }

    print("Test 1: Saving block with metadata...")
    with get_db_session() as session:
        from datetime import datetime

        from db.models import Document

        doc = Document(
            title="test_meta", source_path="test_meta.pdf", created_at=datetime.utcnow()
        )
        session.add(doc)
        session.flush()
        doc_id = doc.id

    block_ids = db_manager.save_blocks([mock_data], doc_id)
    block_id = block_ids[0]

    print("Test 2: Retrieving block and checking metadata...")
    retrieved = db_manager.get_blocks_by_ids([block_id])[0]

    print(f"  Retrieved Kind: {retrieved.get('kind')}")
    print(f"  Metadata Type: {type(retrieved.get('metadata'))}")

    if retrieved.get("metadata") and "steps" in retrieved.get("metadata"):
        print("  ✅ Success: Metadata steps found.")
        print(f"  First Step: {retrieved['metadata']['steps'][0]}")
    else:
        print("  ❌ Failure: Metadata missing or 'steps' key not found.")
        print(f"  Full retrieved dict keys: {retrieved.keys()}")

    # Cleanup
    try:
        if os.path.exists("./temp_verify_meta.db"):
            os.remove("./temp_verify_meta.db")
    except:
        pass


if __name__ == "__main__":
    verify()
