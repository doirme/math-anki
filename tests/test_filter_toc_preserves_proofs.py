from core.segmenter import segment


def test_toc_filtered_but_proofs_kept():
    md = """
# [Page 2]
Sommaire
1 Préliminaires ................................... 3

# [Page 12]
Théorème (Cantor)
Le corps \\mathbb{R} n'est pas dénombrable.

Preuve
On procède par segments emboîtés ...

# [Page 200]
Démonstration
Autre preuve indépendante ...
"""
    blocks = segment(md)
    # Simule le filtrage côté orchestration
    kept = []
    for b in blocks:
        t = b["type"].lower()
        is_proof = t.startswith("démonstration") or t.startswith("proof") or t.startswith("preuve")
        if b.get("is_toc") and not is_proof:
            continue
        kept.append(b)
    # On s'attend à avoir au moins 1 théorème et 2 preuves conservées
    types = [b["type"] for b in kept]
    assert any(t.startswith("théor") or t.startswith("theor") for t in types)
    assert sum(1 for t in types if (t.startswith("preuve") or t.startswith("démonstration") or t.startswith("proof"))) >= 2
