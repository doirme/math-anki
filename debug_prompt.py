"""
Debug : Génère le prompt d'extraction pour le bloc 10 SANS l'envoyer au LLM
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from core.language_detector import format_language_instruction
from core.semantic_schemas import BlockKind, ValidatedBlock

# === SIMULER LE BLOC 10 ===
block = ValidatedBlock(
    id="block_10_sim",
    kind=BlockKind.proposition,
    raw_text="""#### 1.2.2 Proposition Soit $\{a_n; b_n\}$ une suite décroissante de segments de $\mathbb{K}$ , telle que $(H) \lim_{n \to +\infty} b_n - a_n = 0$ . Il est équivalent de dire que 1. l'ensemble $\{a_n \mid n \in \mathbb{N}\}$ possède une borne supérieure; 2. il existe $c$ dans $\mathbb{K}$ tel que : $\bigcap_{n \in \mathbb{N}} [a_n; b_n] = \{c\}$ .""",
    validated_text="""Soit $\{a_n; b_n\}$ une suite décroissante de segments de $\mathbb{K}$ , telle que $(H) \lim_{n \to +\infty} b_n - a_n = 0$ . Il est équivalent de dire que 1. l'ensemble $\{a_n \mid n \in \mathbb{N}\}$ possède une borne supérieure; 2. il existe $c$ dans $\mathbb{K}$ tel que : $\bigcap_{n \in \mathbb{N}} [a_n; b_n] = \{c\}$ .""",
    normalized_text="Proposition sur les intervalles emboîtés",
    page=5,
    start_line=10,
    end_line=15,
    tags=["analyse", "suites"],
    is_self_contained=True,
)

# Contexte (simulé)
context_text = "Chapitre sur les suites et les corps ordonnés..."

# Bloc de preuve lié (simulé)
proof_block_id = "3470750d59c0"

# === CONSTRUIRE LE PROMPT EXACT ===
output_language = "fr"
lang_instruction = format_language_instruction(output_language)

prompt = f"""Extract the theorem from this mathematical block.

### INPUT DATA
<<<< TARGET BLOCK START >>>>
Block (Original):
{block.validated_text}

Block (Normalized - can be misleading prioritize original Block):
{block.normalized_text or "N/A"}
<<<< TARGET BLOCK END >>>>

CONTEXT (for reference only):
{context_text[:1000] or "None"}

Rules:
- **Strict Scope**: ONLY extract content found within the TARGET BLOCK. Do NOT include information from the CONTEXT.
- **IMPORTANT - Examples Are NOT Theorems**: Do NOT tag EXAMPLES as theorems. 
  * If the block starts with "Example:", "Exemple :", "For instance", "Illustration", or similar, it is an EXAMPLE, not a theorem.
  * Examples typically show concrete instances, specific calculations, or particular cases illustrating a concept.
  * Examples may reference a theorem but are not themselves theorems.
- Identify the theorem name, which often appears:
  * In parentheses after the keyword: "Théorème(Operations on monotone functions)"
  * As a header: "# Theorem Name" or "### Name"
  * In bold: "**Theorem Name**"
- **CRITICAL - Normalized Name Language**: Extract the normalized name **in ENGLISH ONLY** (e.g., "Cayley-Hamilton", "Cantor", "Pythagoras").
  * This ensures consistency for duplicate detection across all documents, regardless of their original language.
  * Translate theorem names to English: "Théorème de Cantor" → "Cantor", "Opérations monotones" → "Monotone operations"
- Clearly separate hypotheses from conclusion.
- **CRITICAL**: The `hypothesis_text` and `conclusion_text` MUST NOT contain the theorem name, title, or "Théorème" keyword. They should only contain the mathematical statement. 
They should not contain void statement either - should make sense on their own.
- Extract the mathematical domain (e.g., "analyse réelle", "théorie des groupes"). **ALWAYS provide at least one tag.**
- Extract key characteristics (e.g., "monotone", "continu", "fini")
- **EQUIVALENCE THEOREMS**: If the theorem states that several properties are equivalent:
  * **Detection patterns**: "The following are equivalent:", "TFA:", "P if and only if Q", "Il est équivalent de dire que", numbered lists (1. ... 2. ...)
  * Extract each distinct property/statement into the `equivalent_statements` list.
  * In `conclusion`, use a self contained descriptive summary.
  * Ensure `equivalent_statements` contains the actual math statements, not just "(i), (ii)".

Examples:
1. "Théorème(Opérations sur les fonctions monotones)" → name: "Opérations sur les fonctions monotones", normalized_name: "Monotone functions operations"
2. "### Théorème de Pythagore" → name: "Théorème de Pythagore", normalized_name: "Pythagoras"
3. "**Fundamental Theorem of Calculus**" → name: "Fundamental Theorem of Calculus", normalized_name: "Fundamental theorem of calculus"
4. "Il est équivalent de dire que 1. A est vrai 2. B est vrai" → 
   conclusion: "A si et seulement si B", 
   equivalent_statements: ["A est vrai", "B est vrai"]

- **CRITICAL: JSON Escaping**: In the JSON output, all backslashes in LaTeX MUST be escaped as `\\\\`.

{lang_instruction}

Respond in strict JSON:
{{
  "name": "theorem name" | null,
  "normalized_name": "normalized name" | null,
  "hypotheses": ["hypothesis 1", "hypothesis 2"],
  "hypothesis_text": "complete hypothesis text",
  "conclusion": "conclusion statement",
  "equivalent_statements": ["statement 1", "statement 2"] | [],
  "conclusion_text": "complete conclusion text",
  "has_proof": true|false,
  "domain_tags": ["domain1", "domain2"],
  "characteristics": ["characteristic1", "characteristic2"]
}}"""

# === AFFICHER LE PROMPT ===
print("=" * 100)
print("PROMPT D'EXTRACTION POUR LE BLOC 10")
print("=" * 100)
print(prompt)
print("=" * 100)
print("\n📊 STATISTIQUES :")
print(f"   - Longueur du prompt : {len(prompt)} caractères")
print(f"   - Bloc validé : {len(block.validated_text)} caractères")
print(f"   - Contexte : {len(context_text)} caractères")
print("\n🔍 POINTS À VÉRIFIER :")
print(
    "   1. Le texte du bloc contient-il 'Il est équivalent de dire que' ? ",
    "✅ OUI" if "Il est équivalent de dire que" in block.validated_text else "❌ NON",
)
print(
    "   2. Le prompt mentionne-t-il les listes numérotées (1. ... 2. ...) ? ",
    "✅ OUI" if "numbered lists (1. ... 2. ...)" in prompt else "❌ NON",
)
print(
    "   3. Le prompt contient-il un exemple concret ? ",
    "✅ OUI" if "Il est équivalent de dire que 1. A est vrai" in prompt else "❌ NON",
)
print("\n💡 ATTENDU du LLM :")
print("   {")
print('     "equivalent_statements": [')
print('       "l\'ensemble {a_n | n ∈ ℕ} possède une borne supérieure",')
print('       "il existe c dans K tel que : ⋂ [a_n; b_n] = {c}"')
print("     ]")
print("   }")
