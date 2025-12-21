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

    def __post_init__(self):
        """Standardize content for Anki: Markdown -> HTML, then LaTeX -> MathJax."""
        # 1. Sanitize tags
        self.tags = [_sanitize_tag(t) for t in self.tags]

        # 2. Convert Markdown to HTML (Anki expects HTML)
        self.front = _md_to_html(self.front)
        self.back = _md_to_html(self.back)

        # 3. Convert standard Math delimiters to Anki MathJax
        # Doing this AFTER HTML prevents backslash escaping
        self.front = _convert_to_anki_latex(self.front)
        self.back = _convert_to_anki_latex(self.back)

    @property
    def guid(self) -> str:
        import hashlib

        return hashlib.sha1(self.front.encode()).hexdigest()[:10]


def _sanitize_tag(tag: str) -> str:
    """Anki tags cannot contain spaces. Replace with underscores and clean other chars."""
    if not tag:
        return "untagged"
    # Replace spaces and special chars used as separators in our logic
    t = tag.replace(" ", "_").replace("::", "__").replace(":", "_")
    # Remove any other non-alphanumeric except underscore and dash
    t = re.sub(r"[^\w\-_]", "", t)
    return t


def _convert_to_anki_latex(text: str) -> str:
    """
    Convert $...$ to \\(...\\) and $$...$$ to \\[...\\] for Anki MathJax compatibility.
    """
    if not text:
        return ""

    # 1. Convert block math: $$ ... $$ -> \[ ... \]
    # Using double backslashes in Python string to ensure literal \ in output
    text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)

    # 2. Convert inline math: $ ... $ -> \( ... \)
    text = re.sub(r"(?<!\\)\$(?!\$)(.*?)(?<!\\)\$", r"\\(\1\\)", text)

    return text


def _md_to_html(text: str) -> str:
    """Convert Markdown to HTML for Anki."""
    if not text:
        return ""

    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark", {"breaks": True, "html": True})

    # We want to preserve our \[ \] and \( \) markers from being escaped
    # But MarkdownIt might try to escape backslashes.
    # A simple way is to render and then fix if needed, but modern markdown-it
    # is usually fine if we don't use strict mode.
    html = md.render(text).strip()

    # Remove surrounding <p> if it's a single line to keep it clean in Anki preview
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]

    return html


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
    name = (defi.name or "Définition").strip()
    summary = (defi.summary or "").strip()

    # Aggressive cleaning: find the first bold or header that matches the term
    # or any generic block type indicator at the very beginning

    # 1. Remove generic prefixes at start
    summary = re.sub(
        r"(?i)^(définition|théorème|lemme|proposition|remarque|exemple)\s*[:\-]*\s*",
        "",
        summary,
    )

    # 2. Extract specific term if present in bold at the start: **Term**
    # This is crucial if name is just "Définition"
    bold_match = re.search(r"^\s*\**([^*:]+)\**\s*[:\-]*\s*", summary)
    if bold_match:
        extracted_term = bold_match.group(1).strip()

        # If the extracted term is more useful than the current name
        if name.lower() == "définition" and len(extracted_term) > 2:
            name = extracted_term
            # Remove it from summary to avoid duplication in Back
            summary = re.sub(r"^\s*\**[^*:]+\**\s*[:\-]*\s*", "", summary).strip()
        elif name.lower() != "définition" and (
            extracted_term.lower() in name.lower()
            or name.lower() in extracted_term.lower()
        ):
            # Name and summary-prefix match, remove prefix from summary
            summary = re.sub(r"^\s*\**[^*:]+\**\s*[:\-]*\s*", "", summary).strip()

    front = f"Rappeler la définition de : <br><b>{name}</b>"
    back = summary

    tags = ["type::definition", f"source::{meta.get('doc_id', 'unknown')}"]
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
