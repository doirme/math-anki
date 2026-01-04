import os
import sys
from pathlib import Path

# Use a temporary DB for verification
os.environ["DB_URL"] = "sqlite:///./temp_verify_steps.db"

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

    # Mock theorem data that has a proof relation (simulated)
    # In practice make_theorem_cards looks for relations, but we can mock the thm_obj

    mock_steps = [
        "Étape 1: Hypothèse de récurrence",
        "Étape 2: Hérédité",
        "Étape 3: Conclusion",
    ]

    thm_obj = type(
        "obj",
        (object,),
        {
            "name": "Théorème de Test",
            "hypotheses": type("obj", (object,), {"summary": "Soit n un entier"})(),
            "conclusion": type("obj", (object,), {"summary": "P(n) est vrai"})(),
            "summary": "Résumé du théorème",
            "tags": [type("tag", (object,), {"name": "test"})()],
            "proof": type("obj", (object,), {"summary": "Résumé de la preuve"})(),
            "proof_metadata": {"steps": mock_steps},
        },
    )()

    meta_with_steps = {"deck": "TestDeck", "use_steps_for_proofs": True}

    meta_no_steps = {"deck": "TestDeck", "use_steps_for_proofs": False}

    print("Test 1: Generating proof card WITH steps...")
    cards_with = make_theorem_cards(thm_obj, meta_with_steps)
    proof_card_with = next(c for c in cards_with if "facet::proof" in c.tags)

    print(f"  Back content snippet: {proof_card_with.back[:100]}...")
    if "<ol><li>Étape 1" in proof_card_with.back:
        print("  ✅ Success: Steps found in card back as ordered list.")
    else:
        print("  ❌ Failure: Steps not found in card back.")

    print("\nTest 2: Generating proof card WITHOUT steps...")
    cards_no = make_theorem_cards(thm_obj, meta_no_steps)
    proof_card_no = next(c for c in cards_no if "facet::proof" in c.tags)

    print(f"  Back content snippet: {proof_card_no.back[:100]}...")
    if "Résumé de la preuve" in proof_card_no.back and "<ol>" not in proof_card_no.back:
        print("  ✅ Success: Summary used when steps disabled.")
    else:
        print("  ❌ Failure: Summary not correctly used.")

    # Cleanup
    try:
        if os.path.exists("./temp_verify_steps.db"):
            os.remove("./temp_verify_steps.db")
    except:
        pass


if __name__ == "__main__":
    verify()
