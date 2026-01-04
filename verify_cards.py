from dataclasses import dataclass
from typing import List, Optional

from src.core.cards import make_definition_card, make_theorem_cards


# Mock objects for testing
@dataclass
class MockTag:
    name: str


@dataclass
class MockTextBlock:
    heading_path: str


@dataclass
class MockSourceLink:
    text_block: MockTextBlock


@dataclass
class MockBlock:
    id: int
    name: str = None
    summary: str = None
    hypotheses: "MockBlock" = None
    conclusion: "MockBlock" = None
    tags: List[MockTag] = None
    sources: List[MockSourceLink] = None


def test_cards():
    meta = {"deck": "Math", "doc_id": "test_doc"}

    # 1. Theorem with generic name
    thm_generic = MockBlock(
        id=1,
        name="Théorème",
        summary="Soit f continue...",
        hypotheses=MockBlock(id=2, summary="f est continue sur [a, b]"),
        conclusion=MockBlock(id=3, summary="f est bornée"),
        tags=[MockTag("Analyse")],
        sources=[MockSourceLink(MockTextBlock("Chapitre 1 > Continuité"))],
    )

    print("--- GENERIC THEOREM ---")
    cards = make_theorem_cards(thm_generic, meta)
    for i, c in enumerate(cards):
        print(f"Card {i} Front:\n{c.front}")
        print(f"Card {i} Back:\n{c.back}\n")

    # 2. Famous Theorem (ID % 3 == 1 -> Name quest)
    thm_famous = MockBlock(
        id=4,  # 4 % 3 = 1
        name="Théorème de Bolzano-Weierstrass",
        summary="Toute suite bornée...",
        hypotheses=MockBlock(id=5, summary="(u_n) est une suite bornée de R^n"),
        conclusion=MockBlock(id=6, summary="(u_n) admet une sous-suite convergente"),
        tags=[MockTag("Topologie")],
        sources=[
            MockSourceLink(MockTextBlock("Espaces Vectoriels Normés > Compacité"))
        ],
    )

    print("--- FAMOUS THEOREM (ID % 3 == 1) ---")
    cards = make_theorem_cards(thm_famous, meta)
    for i, c in enumerate(cards):
        print(f"Card {i} Front:\n{c.front}")
        print(f"Card {i} Back:\n{c.back}\n")

    # 3. Famous Theorem (ID % 3 == 2 -> Statement quest)
    thm_famous_2 = MockBlock(
        id=5,  # 5 % 3 = 2
        name="Théorème de Cayley-Hamilton",
        summary="chi_A(A) = 0",
        hypotheses=MockBlock(id=8, summary="A est une matrice carrée"),
        conclusion=MockBlock(id=9, summary="Le polynôme caractéristique de A annule A"),
        tags=[MockTag("Algèbre")],
        sources=[MockSourceLink(MockTextBlock("Réduction des endomorphismes"))],
    )

    print("--- FAMOUS THEOREM (ID % 3 == 2) ---")
    cards = make_theorem_cards(thm_famous_2, meta)
    for i, c in enumerate(cards):
        print(f"Card {i} Front:\n{c.front}")
        print(f"Card {i} Back:\n{c.back}\n")


if __name__ == "__main__":
    test_cards()
