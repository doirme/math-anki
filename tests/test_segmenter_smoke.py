from core.segmenter import segment


def test_segmenter_headers_smoke():
    md = """
# [Page 1]

Définition (espace métrique)
Un couple (X, d) où d : X×X → R_+ ...

Théorème (Bolzano-Weierstrass)
Toute suite bornée de R^n admet une sous-suite convergente.

Exercice
Montrer que la suite (u_n) définie par ...
"""
    blocks = segment(md)
    types = [b["type"] for b in blocks]
    # On s'attend à voir des blocs correspondant aux en-têtes
    assert any(t.startswith("définition") or t.startswith("definition") for t in types)
    assert any(t.startswith("théor") or t.startswith("theor") for t in types)
    assert any(t.startswith("exercice") or t.startswith("exercise") for t in types)
