import click
from pathlib import Path
from .core.config import settings
from .core.llm_client import LLMClient
from .core.pdf_to_md import pdf_to_markdown
from .core.pdf_to_md import pdf_to_markdown
from .core.cards import make_definition_card, make_theorem_cards
from .core.cards import make_definition_card, make_theorem_cards
from .exporters.anki_export import export_apkg
from .core.math_fix import fix_math_in_markdown, llm_fn_from_settings
from .core.config import settings

@click.group()
def cli():
    pass


@cli.command()
@click.argument('pdf', type=click.Path(exists=True))
@click.option('--out-md', default='./data/markdown/out.md')
@click.option('--prefer', default='marker', help='marker|mistral_ocr|docling_modal')
def ingest(pdf, out_md, prefer):
    """PDF -> Markdown via Marker API (primary), Mistral OCR, or Docling Modal."""
    md = pdf_to_markdown(Path(pdf), prefer=prefer)
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_md).write_text(md, encoding="utf-8")
    click.echo(f"Markdown écrit dans {out_md}")


@cli.command()
@click.option('--md', default='./data/markdown/out.md')
@click.option('--deck', default='Maths')
@click.option('--out-json', default='./data/cards/cards.json')
def build(md, deck, out_json):
    """Segmente le markdown et génère des cartes."""
    md_text = Path(md).read_text(encoding="utf-8")
    cards = []
    
    # New semantic analyzer
    from .core.semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(md_text, generate_embeddings=False)
    
    # Convert extracted data to flashcards
    from .core.cards import make_definition_card, make_theorem_cards
    meta = {"deck": deck, "doc_id": Path(md).stem}
    
    for item in result["extracted"]:
        kind = item["kind"]
        data = item["data"]
        
        if kind == "definition":
            # Handle multiple definitions
            if data.get("is_multiple") and data.get("definitions"):
                for def_item in data["definitions"]:
                    defi = {"term": def_item.get("term"), "statement": def_item.get("statement")}
                    cards.append(make_definition_card(defi, meta))
            else:
                defi = {"term": data.get("term"), "statement": data.get("statement")}
                cards.append(make_definition_card(defi, meta))
        
        elif kind == "theorem":
            thm = {
                "name": data.get("name"),
                "hypotheses": data.get("hypotheses", []),
                "conclusion": data.get("conclusion", ""),
                "has_proof": data.get("has_proof", False),
            }
            cards.extend(make_theorem_cards(thm, meta))
    
    import json
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(out_json).write_text(json.dumps([c.__dict__ for c in cards], ensure_ascii=False, indent=2), encoding="utf-8")
    click.echo(f"Cartes générées: {out_json}")


@cli.command()
@click.option('--in-json', default='./data/cards/cards.json')
@click.option('--out', default='./data/cards/Deck.apkg')
@click.option('--deck', default='Maths')
def export(in_json, out, deck):
    """Exporte les cartes en .apkg (Anki)."""
    import json
    from .core.cards import Flashcard
    raw = json.loads(Path(in_json).read_text(encoding="utf-8"))
    cards = [Flashcard(**r) for r in raw]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    export_apkg(cards, deck, out)
    click.echo(f"Écrit: {out}")


@cli.command()
@click.argument("md_in", type=click.Path(exists=True))
@click.option("--out", "-o", default=None, help="Chemin du Markdown corrigé")
@click.option("--use-llm/--no-llm", default=None, help="Forcer l'usage du LLM (override .env)")
def fixmath(md_in, out, use_llm):
    """Passe de réparation LaTeX sur un fichier Markdown."""
    text = Path(md_in).read_text(encoding="utf-8")
    if use_llm is None:
        do_llm = settings.fixmath_use_llm
    else:
        do_llm = use_llm
    llm = llm_fn_from_settings() if do_llm else None
    fixed, nmod, natt = fix_math_in_markdown(text, llm=llm)
    click.echo(f"Modifiés: {nmod}, Besoin-attention: {natt}")
    if out:
        Path(out).write_text(fixed, encoding="utf-8")
        click.echo(f"Écrit: {out}")
    else:
        # affiche les 400 premiers chars
        click.echo(fixed[:400])


if __name__ == '__main__':
    cli()
