import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent / "src"))

from core.cards import make_theorem_cards


def verify():
    print("Test: Generating cards for an equivalence theorem...")

    # Mock an equivalence theorem with equivalent_statements
    equivs_list = [
        "$\\mathbb{K}$ est archimédien",
        "$\\bigcap_{n \\in \\mathbb{N}} [a_n; b_n]$ contient un unique élément",
        "$\\forall \\epsilon > 0, \\exists N, \\forall n \\geq N: b_n - a_n < \\epsilon$",
    ]

    thm_obj = type(
        "obj",
        (object,),
        {
            "name": "Théorème des intervalles emboîtés",
            "hypotheses": type(
                "obj",
                (object,),
                {
                    "summary": "$\\{a_n; b_n\\}$ est une suite décroissante de segments de $\\mathbb{K}$"
                },
            )(),
            "conclusion": type(
                "obj",
                (object,),
                {"summary": "Les propositions suivantes sont équivalentes"},
            )(),
            "summary": "Théorème classique d'analyse",
            "tags": [type("tag", (object,), {"name": "analyse"})()],
            "equivalent_statements": equivs_list,
        },
    )()

    meta = {"deck": "TestDeck", "use_steps_for_proofs": False}

    print("\nGenerating cards...")
    cards = make_theorem_cards(thm_obj, meta)

    print(f"\n✅ Generated {len(cards)} card(s)")

    for i, card in enumerate(cards, 1):
        print(f"\n--- Card {i} ---")
        print(f"Front snippet: {card.front[:100]}...")
        print(f"Back snippet: {card.back[:150]}...")

        # Check if equivalent statements appear in the back
        if "<ul><li>" in card.back and "archimédien" in card.back:
            print("  ✅ Equivalent statements detected in card back!")
        else:
            print(f"  ⚠️  Full back: {card.back}")


if __name__ == "__main__":
    verify()
