import hashlib
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from db.models import SemanticBlock


@dataclass
class Flashcard:
    deck: str
    note_type: str
    front: str
    back: str
    tags: List[str]

    @property
    def guid(self) -> str:
        return hashlib.sha1(self.front.encode()).hexdigest()[:10]


def _purge_hints_from_conclusion(conclusion: str) -> str:
    """Évite de divulguer des hypothèses dans la conclusion affichée en question."""
    c = conclusion.strip()
    # Supprime préfixes du type "Sous les hypothèses ..., on a ..."
    c = re.sub(r"(?i)^(sous\s+les?\s+hypothèses?.{0,120}?on a\s*[:,]?)", "", c)
    # Compacte espaces et nouvelles lignes
    c = re.sub(r"\s+", " ", c)
    # Tronque si trop long (garde l'idée générale)
    return c[:400]


def make_definition_card(defi: SemanticBlock, meta: Dict[str, Any]) -> Flashcard:
    term = defi.name or "Définition"
    front = f"Rappeler: **{term}**"
    back = defi.summary or ""

    tags = [f"type::definition", f"source::{meta.get('doc_id', 'unknown')}"]
    # Add domain tags
    if defi.tags:
        for tag in defi.tags:
            tags.append(f"domain::{tag.name}")

    return Flashcard(
        deck=meta["deck"], note_type="Basic", front=front, back=back, tags=tags
    )


def make_theorem_cards(thm: SemanticBlock, meta: Dict[str, Any]) -> List[Flashcard]:
    cards = []

    # Access linked hypotheses/conclusion blocks
    # Note: thm.hypotheses is a relationship to a SemanticBlock
    H = thm.hypotheses.summary if thm.hypotheses else "(hypothèses non extraites)"
    C = thm.conclusion.summary if thm.conclusion else (thm.summary or "")
    name = thm.name or "Théorème"

    Cq = _purge_hints_from_conclusion(C)

    base_tags = ["type::theorem", f"name::{name}"]
    if thm.tags:
        for tag in thm.tags:
            base_tags.append(f"domain::{tag.name}")

    # H -> C (question: ne pas révéler H)
    cards.append(
        Flashcard(
            deck=meta["deck"],
            note_type="Basic",
            front=f"Sous quelles hypothèses peut-on conclure : {Cq} ?",
            back=H,
            tags=base_tags,
        )
    )

    # Nom (facette)
    cards.append(
        Flashcard(
            deck=meta["deck"],
            note_type="Basic (and reversed)",
            front=f"Quel est le nom du théorème correspondant à : {Cq} ?",
            back=name,
            tags=base_tags + ["facet::name"],
        )
    )
    return cards
