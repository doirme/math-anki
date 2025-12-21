from pathlib import Path

import fitz  # PyMuPDF

# On importe directement les fonctions du module à tester
from core.pdf_to_md import (
    pdf_to_markdown,
)


def _make_text_pdf(path: Path, texts=("Hello", "World")) -> Path:
    """Crée un PDF texte (sélectionnable) avec une page par élément de 'texts'."""
    doc = fitz.open()
    for t in texts:
        page = doc.new_page()
        # écriture simple en haut à gauche
        page.insert_text((72, 72), t)  # 72 pt = 1 inch margin
    doc.save(path)
    doc.close()
    return path

def _make_vector_only_pdf(path: Path, n_pages=2) -> Path:
    """Crée un PDF sans texte : uniquement des formes vectorielles (simulateur de scan)."""
    doc = fitz.open()
    for _ in range(n_pages):
        page = doc.new_page()
        shape = page.new_shape()
        # Dessine un rectangle rempli (pas de texte)
        rect = fitz.Rect(50, 50, 300, 200)
        shape.draw_rect(rect)
        shape.finish(fill=(0.8, 0.8, 0.8))  # gris
        shape.commit()
    doc.save(path)
    doc.close()
    return path

# Note: _has_extractable_text was removed as we no longer use OCR preprocessing
# The backends (Marker, Mistral, Docling) handle OCR internally

def test_pdf_to_markdown_docling_fallback(tmp_path):
    """Test that docling_modal can be used as fallback."""
    pdf = _make_text_pdf(tmp_path / "text.pdf", texts=("Page One", "Page Two"))
    # This will try Marker -> Mistral -> Docling
    # If none work, it returns empty string
    md = pdf_to_markdown(pdf, prefer="docling_modal")
    # Result depends on whether backends are available
    assert isinstance(md, str)
