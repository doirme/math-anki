import re
from dataclasses import dataclass
from typing import Any, Dict, List


# Mock Classes
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


@dataclass
class Flashcard:
    deck: str
    note_type: str
    front: str
    back: str
    tags: List[str]


# Copied functions from cards.py for testing
def _get_context_prefix(block) -> str:
    """Extraire le contexte (domaines + chemin de titres) pour l'afficher sur le recto."""
    contexts = []
    if block.tags:
        domains = [t.name for t in block.tags]
        contexts.append(", ".join(domains))
    path = None
    if block.sources:
        for src in block.sources:
            if src.text_block and src.text_block.heading_path:
                path = src.text_block.heading_path
                break
    if path:
        parts = [p.strip() for p in path.split(">") if p.strip()]
        if len(parts) > 2:
            path = " > ".join(parts[-2:])
        else:
            path = " > ".join(parts)
        contexts.append(path)
    if not contexts:
        return ""
    return f"<small>[{ ' | '.join(contexts) }]</small><br>"


def _purge_hints_from_conclusion(conclusion: str) -> str:
    c = conclusion.strip()
    c = re.sub(r"(?i)^(sous\s+les?\s+hypothèses?.{0,120}?on a\s*[:,]?)", "", c)
    c = re.sub(r"\s+", " ", c)
    return c[:400]


def make_theorem_cards(thm, meta) -> List[Flashcard]:
    cards = []
    H = (
        thm.hypotheses.summary if thm.hypotheses else "<i>(non spécifiées)</i>"
    ).strip()
    C = (thm.conclusion.summary if thm.conclusion else (thm.summary or "")).strip()
    name = (thm.name or "Théorème").strip()
    context = _get_context_prefix(thm)
    Cq = _purge_hints_from_conclusion(C)
    base_tags = ["type::theorem", f"name::{name}"]

    generic_names = [
        "théorème",
        "proposition",
        "lemme",
        "corollaire",
        "propriété",
        "propriété.",
        "théorème.",
        "définition-proposition",
        "proposition-définition",
    ]
    is_generic = name.lower() in generic_names
    q_type_idx = (thm.id or 0) % 3

    if is_generic:
        cards.append(
            Flashcard(
                deck=meta["deck"],
                note_type="Basic",
                front=f"{context}Sous quelles hypothèses peut-on conclure : <br><br> {Cq} ?",
                back=f"<b>Hypothèses :</b><br>{H}",
                tags=base_tags + ["facet::hypotheses"],
            )
        )
    else:
        if q_type_idx == 0:
            cards.append(
                Flashcard(
                    deck=meta["deck"],
                    note_type="Basic",
                    front=f"{context}Sous quelles hypothèses peut-on conclure : <br><br> {Cq} ?",
                    back=f"<b>Hypothèses :</b><br>{H}",
                    tags=base_tags + ["facet::hypotheses"],
                )
            )
        elif q_type_idx == 1:
            cards.append(
                Flashcard(
                    deck=meta["deck"],
                    note_type="Basic",
                    front=f"{context}Quel est le nom du résultat qui permet de conclure : <br><br> {Cq} ?",
                    back=f"<b>{name}</b>",
                    tags=base_tags + ["facet::name"],
                )
            )
        else:
            cards.append(
                Flashcard(
                    deck=meta["deck"],
                    note_type="Basic",
                    front=f"{context}Énoncer le résultat suivant : <br><b>{name}</b>",
                    back=f"<i>Hypothèses :</i> {H}<br><br><i>Conclusion :</i> {C}",
                    tags=base_tags + ["facet::statement"],
                )
            )
    return cards


# Test Execution
def run_test():
    meta = {"deck": "Math"}

    # 1. Theorem with context and generic name (ID 1 -> Type 1, but forced to Type A because generic)
    thm1 = MockBlock(
        id=1,
        name="Théorème",
        hypotheses=MockBlock(id=0, summary="H1"),
        conclusion=MockBlock(id=0, summary="C1"),
        tags=[MockTag("Algèbre")],
        sources=[MockSourceLink(MockTextBlock("Chapitre 1 > Section 1"))],
    )

    # 2. Famous Theorem (ID 4 -> ID % 3 = 1 -> Name quest)
    thm2 = MockBlock(
        id=4,
        name="Bolzano-Weierstrass",
        hypotheses=MockBlock(id=0, summary="H2"),
        conclusion=MockBlock(id=0, summary="C2"),
        tags=[MockTag("Analyse")],
        sources=[MockSourceLink(MockTextBlock("Espaces Métriques > Compacité"))],
    )

    # 3. Famous Theorem (ID 5 -> ID % 3 = 2 -> Statement quest)
    thm3 = MockBlock(
        id=5,
        name="Cayley-Hamilton",
        hypotheses=MockBlock(id=0, summary="H3"),
        conclusion=MockBlock(id=0, summary="C3"),
        tags=[MockTag("Algèbre")],
        sources=[MockSourceLink(MockTextBlock("Matrices > Endomorphismes"))],
    )

    for t in [thm1, thm2, thm3]:
        print(f"\n--- Testing Block {t.id} ({t.name}) ---")
        cards = make_theorem_cards(t, meta)
        for c in cards:
            print(f"FRONT: {c.front}")
            print(f"BACK: {c.back}")


if __name__ == "__main__":
    run_test()
