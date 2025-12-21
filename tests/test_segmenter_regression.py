from core.block_creator import BlockCreator


def test_segmenter_splits_theorem_and_proof_and_flags_toc():
    md = """
# [Page 1]
Table des matières
1 Introduction ........................................ 3
2 Théorèmes classiques ............................... 10
2.1 Théorème de Cantor ............................... 12

# [Page 12]
Théorème de Cantor
Le corps \\mathbb{R} n'est pas dénombrable.

Preuve
On construit une suite de segments emboîtés ...
"""

    creator = BlockCreator()
    blocks = creator._simple_segment(md)

    # On attend : 1 bloc TOC + 1 bloc Théorème + 1 bloc Preuve (au minimum)
    types = [b["type"] for b in blocks]
    # Vérifie que Preuve est séparé
    assert any(t.startswith("théor") or t.startswith("theor") for t in types), types
    assert any(
        t.startswith("preuve") or t.startswith("démonstration") or t.startswith("proof")
        for t in types
    ), types

    # Le premier bloc (table des matières) doit être flaggé is_toc
    toc_blocks = [b for b in blocks if b.get("is_toc")]
    assert len(toc_blocks) >= 1, "Le sommaire devrait être détecté comme TOC"
    # Les blocs Preuve ne doivent pas être flaggés TOC
    proof_blocks = [
        b
        for b in blocks
        if (
            b["type"].startswith("preuve")
            or b["type"].startswith("démonstration")
            or b["type"].startswith("proof")
        )
    ]
    assert all(
        not b.get("is_toc", False) for b in proof_blocks
    ), "Une preuve ne doit pas être marquée TOC"


def test_definition_with_formula_not_split():
    """Test that definitions with embedded formulas are kept as one block."""
    md = """## 1 VOCABULAIRE USUEL

### 1.1 MONOTONIE

Définition (Fonction monotone) Soit $f: E \\longrightarrow \\mathbb{R}$ une fonction.

- On dit que $f$ est croissante si :

$$
\\forall x, y \\in E, \\quad x<y \\quad \\Longrightarrow \\quad f(x) \\leqslant f(y)
$$"""

    creator = BlockCreator()
    blocks = creator._simple_segment(md)

    # Find the definition block
    definition_blocks = [b for b in blocks if b["type"] == "definition"]
    assert len(definition_blocks) >= 1, "Should find at least one definition block"

    # The definition block should contain the formula
    definition_text = definition_blocks[0]["text"]
    assert (
        "\\forall x, y \\in E" in definition_text
    ), "Definition should include the formula"
    assert (
        "croissante" in definition_text
    ), "Definition should include the condition text"

    # Should not have an orphan formula block
    text_blocks = [b for b in blocks if b["type"] == "text"]
    for text_block in text_blocks:
        # No block should be ONLY a formula
        if "$$" in text_block["text"]:
            assert (
                "Définition" in text_block["text"] or len(text_block["text"]) > 100
            ), "Formula blocks should be part of larger semantic blocks, not standalone"


def test_consecutive_theorems_not_merged():
    """Test that a full theorem block doesn't 'eat' the header of the next theorem."""
    md = """Théorème (Injectivité)
Soit f une fonction.
Si f est strictement monotone, f est injective.
Les résultats sont valables.

## Théorème (Opérations)
- (i) Addition : Si f et g sont croissantes...
"""
    creator = BlockCreator()
    # We need to call create_blocks or _initial_segmentation to trigger _merge_headers
    # _simple_segment alone won't show the merge issue
    blocks = creator._initial_segmentation(md)

    # Should have 2 blocks (or 3 if the second theorem body is split from header, but header shouldn't be in block 1)

    # Check Block 1
    block1 = blocks[0]
    assert "Injectivité" in block1["text"]
    assert (
        "Opérations" not in block1["text"]
    ), "Block 1 should not contain the header of Block 2"

    # Check that we have a second block starting with the second theorem
    assert len(blocks) >= 2
    block2 = blocks[1]
    # Block 2 should be the second theorem (header + body if merged, or just header if not)
    assert "Opérations" in block2["text"]


def test_split_on_bold_keywords():
    """Test that we split blocks even if the keyword is bolded (e.g. **Exemple**)."""
    md = """Exemple
Graphiques illustrant...

**Exemple** Pour tous $a, x \\in \\mathbb{R}$ ...

**Définition (Fonction paire/impaire)** On suppose...
"""
    creator = BlockCreator()
    blocks = creator._simple_segment(md)

    # Should be split into 3 blocks
    # 1. Exemple (plain)
    # 2. **Exemple** (bold)
    # 3. **Définition** (bold)

    assert len(blocks) >= 3, f"Expected at least 3 blocks, got {len(blocks)}"

    assert "Graphiques" in blocks[0]["text"]
    assert "**Exemple**" in blocks[1]["text"]
    assert "**Définition" in blocks[2]["text"]

    # Check types
    assert blocks[1]["type"] == "example"
    assert blocks[2]["type"] == "definition"


def test_cantor_theorem_proof_separation():
    """Test that Cantor Theorem and its Proof are separated into two blocks."""
    md = """# Théorème de Cantor

Le corps $\\mathbb{R}$ n'est pas dénombrable.

## Preuve
On suppose par l'absurde que $\\mathbb{R}$ est dénombrable. On peut alors énumérer ses éléments : $x_1, x_2, \\dots$.
On construit un intervalle fermé $I_1$ ne contenant pas $x_1$. Puis $I_2 \\subset I_1$ ne contenant pas $x_2$, etc.
L'intersection des $I_n$ est non vide (théorème des segments emboîtés), soit $x \\in \\cap I_n$.
Alors $x$ n'est aucun des $x_i$, contradiction."""

    creator = BlockCreator()
    # Use _initial_segmentation to check the segmentation including header merging
    blocks = creator._initial_segmentation(md)

    # Output for debugging failure
    print(f"Blocks found: {len(blocks)}")
    for i, b in enumerate(blocks):
        print(f"Block {i} type={b['type']}: {b['text'][:50]}...")

    # Should have at least 2 blocks
    assert len(blocks) >= 2, f"Expected at least 2 blocks, found {len(blocks)}"

    # Block 1: Theorem Statement
    # Should contain "Théorème de Cantor" and "pas dénombrable"
    # Should NOT contain content from the proof like "intervalles fermés"
    block_theorem = blocks[0]
    assert "Théorème de Cantor" in block_theorem["text"]
    assert "pas dénombrable" in block_theorem["text"]
    assert (
        "intervalles fermés" not in block_theorem["text"]
    ), "Theorem block should not contain proof content"
    assert block_theorem["type"] == "theorem"

    # Block 2: Proof
    # Should contain "Preuve" and "intervalles fermés"
    block_proof = blocks[1]
    assert "Preuve" in block_proof["text"] or block_proof["type"] == "proof"
    assert (
        "intervalles fermés" in block_proof["text"]
        or "intervalle fermé" in block_proof["text"]
    )

    # Check types
    assert block_proof["type"] in [
        "proof",
        "text",
    ], f"Expected proof type, got {block_proof['type']}"
