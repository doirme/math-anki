"""
Constants for the core module.
"""

from typing import Dict, List

# Block type keywords for segmentation and identification
BLOCK_TYPE_KEYWORDS: Dict[str, List[str]] = {
    "toc": ["table des matières", "contents"],
    "definition": ["definition", "définition"],
    "theorem": ["theorem", "théorème"],
    "proof": ["proof", "démonstration", "preuve"],
    "example": ["example", "exemple", "examples", "exemples"],
    "exercise": ["exercise", "exercice", "exercises", "exercices"],
    "lemma": ["lemma", "lemme"],
    "corollary": ["corollary", "corollaire"],
    "proposition": ["proposition"],
    "remark": ["remark", "remarque"],
    "formula": ["formule", "formules", "formula", "formulas", "equations", "equation"],
}
