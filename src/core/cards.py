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


def _get_context_prefix(block: Any) -> str:
    """Extraire le contexte (domaines + document + page + chemin) pour l'afficher sur le recto."""
    contexts = []

    # 1. Domaines (tags)
    tags = []
    if hasattr(block, "tags") and block.tags:
        tags = block.tags
    elif isinstance(block, dict) and block.get("tags"):
        tags = block["tags"]

    if tags:
        # tags can be list of Tag objects or list of strings
        domains = []
        for t in tags:
            if hasattr(t, "name"):
                domains.append(t.name)
            else:
                domains.append(str(t))
        if domains:
            contexts.append(", ".join(domains))

    # 2. Source (Document & Page)
    sources = []
    if hasattr(block, "sources") and block.sources:
        sources = block.sources
    elif isinstance(block, dict) and block.get("sources"):
        sources = block["sources"]
    doc_title = None
    page_num = None
    path = None

    if sources:
        for src in sources:
            # Handle ORM objects (SemanticSourceLink)
            if hasattr(src, "text_block") and src.text_block:
                if (
                    not doc_title
                    and hasattr(src.text_block, "document")
                    and src.text_block.document
                ):
                    doc_title = src.text_block.document.title
                if page_num is None and hasattr(src.text_block, "page_number"):
                    page_num = src.text_block.page_number
                if not path and hasattr(src.text_block, "heading_path"):
                    path = src.text_block.heading_path
            # Handle dictionaries (from get_blocks_by_ids)
            elif isinstance(src, dict):
                if not doc_title:
                    doc_title = src.get("title")
                if page_num is None:
                    page_num = src.get("page")
                if not path:
                    path = src.get("path") or src.get("heading_path")

                if doc_title and page_num is not None and path:
                    break

    # Fallback for page if it's directly on the block (like in ValidatedBlock/Pydantic)
    if page_num is None:
        if hasattr(block, "page"):
            page_num = block.page
        elif isinstance(block, dict) and "page" in block:
            page_num = block["page"]

    if doc_title:
        contexts.append(f"Doc: {doc_title}")

    if page_num is not None and page_num > 0:
        contexts.append(f"p. {page_num}")

    # 3. Hiérarchie (heading_path)
    if path:
        # On simplifie le chemin s'il est trop long (ex: "Chap1 > Sec2 > Sub3" -> "Sec2 > Sub3")
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
    # This is crucial if name is just "Définition" or a generic tag
    bold_match = re.search(r"^\s*\**([^*:]+)\**\s*[:\-]*\s*", summary)
    if bold_match:
        extracted_term = bold_match.group(1).strip()

        # Get list of tag names for comparison
        tag_names = [t.name.lower() for t in getattr(defi, "tags", [])]

        # Override if name is generic OR just a tag (suggesting it was a fallback)
        is_generic = name.lower() in ["définition", "definition"]
        is_tag_fallback = name.lower() in tag_names

        if (is_generic or is_tag_fallback) and len(extracted_term) > 2:
            name = extracted_term
            # Remove it from summary to avoid duplication in Back
            summary = re.sub(r"^\s*\**[^*:]+\**\s*[:\-]*\s*", "", summary).strip()
        elif name.lower() != "définition" and (
            extracted_term.lower() in name.lower()
            or name.lower() in extracted_term.lower()
        ):
            # Name and summary-prefix match (e.g. Name="Archimédien", Prefix="Corps archimédien")
            # Prefer the extracted one as it might be more complete
            if len(extracted_term) > len(name):
                name = extracted_term
            # Remove prefix from summary
            summary = re.sub(r"^\s*\**[^*:]+\**\s*[:\-]*\s*", "", summary).strip()

    front = f"{_get_context_prefix(defi)}Rappeler la définition de : <br><b>{name}</b>"
    back = summary

    tags = ["type::definition", f"source::{meta.get('doc_id', 'unknown')}"]
    defi_tags = getattr(defi, "tags", [])
    if defi_tags:
        for tag in defi_tags:
            tags.append(f"domain::{tag.name}")

    return Flashcard(
        deck=meta["deck"], note_type="Basic", front=front, back=back, tags=tags
    )


def make_theorem_cards(thm: SemanticBlock, meta: Dict[str, Any]) -> List[Flashcard]:
    cards = []

    # Access linked hypotheses/conclusion blocks
    H = (
        thm.hypotheses.summary if thm.hypotheses else "<i>(non spécifiées)</i>"
    ).strip()
    C = (thm.conclusion.summary if thm.conclusion else (thm.summary or "")).strip()

    # Handle equivalent statements (i <=> ii <=> iii)
    equivs = getattr(thm, "equivalent_statements", [])
    if equivs and isinstance(equivs, list) and len(equivs) > 0:
        # Format as a list for the conclusion
        # If the conclusion is just "They are equivalent", we replace it with the properties
        items_html = "".join([f"<li>{s}</li>" for s in equivs])
        C = f"Les propositions suivantes sont équivalentes :<ul>{items_html}</ul>"

    name = (thm.name or "Théorème").strip()

    context = _get_context_prefix(thm)
    Cq = _purge_hints_from_conclusion(C)

    base_tags = ["type::theorem", f"name::{name}"]
    thm_tags = getattr(thm, "tags", [])
    if thm_tags:
        for tag in thm_tags:
            base_tags.append(f"domain::{tag.name}")

    # --- SÉLECTION DE LA QUESTION (Sémantique / Identification) ---
    # Pour chaque théorème, on ne génère qu'UNE SEULE question de ce type
    # pour éviter la redondance, en alternant selon l'ID.

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

    # Choix du type de question basé sur l'ID (déterministe)
    # On utilise getattr car les objets de session Streamlit n'ont pas d'ID
    q_type_idx = (getattr(thm, "id", 0) or 0) % 3

    if is_generic:
        # Toujours TYPE A pour les noms génériques (Hypothèses)
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
        # Pour les noms célèbres, on varie :
        # 0: Hypothèses, 1: Nom via Conclusion, 2: Énoncé via Nom
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

    # --- CARTE DÉMONSTRATION (Si elle existe) ---
    proof_text = None
    if hasattr(thm, "proof") and thm.proof:
        proof_text = thm.proof.summary
    else:
        # Chercher dans les relations si un bloc "proves" celui-ci
        if hasattr(thm, "relations_to"):
            for rel in thm.relations_to:
                if rel.predicate == "proves" or rel.predicate == "has_proof":
                    proof_text = rel.subject.summary
                    break

    if proof_text:
        # User preference: use steps instead of summary if available
        if meta.get("use_steps_for_proofs") and hasattr(thm, "proof_metadata"):
            steps = thm.proof_metadata.get("steps")
            if steps and isinstance(steps, list):
                steps_html = "".join([f"<li>{s}</li>" for s in steps])
                proof_text = f"<ol>{steps_html}</ol>"

        cards.append(
            Flashcard(
                deck=meta["deck"],
                note_type="Basic",
                front=f"{context}<b>Démontrer le résultat suivant ({name}) :</b><br><br><i>Hypothèses :</i> {H}<br><br><i>Conclusion :</i> {C}",
                back=f"<b>Démonstration :</b><br>{proof_text}",
                tags=base_tags + ["facet::proof"],
            )
        )

    return cards
