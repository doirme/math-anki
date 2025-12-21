"""
Phase 2: Enhanced Semantic Extraction

Extracts structured data from validated blocks:
- Check self-containedness with context
- Complete/trim blocks if needed
- Split multiple items
- Isolate key parts (name, hypothesis, conclusion)
- Extract domain tags
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from tqdm import tqdm

from .json_utils import extract_json_obj
from .llm_config import get_llm_task_manager
from .semantic_schemas import (
    BlockKind,
    ExtractedDefinition,
    ExtractedExercise,
    ExtractedFormula,
    ExtractedProof,
    ExtractedTheorem,
    LinkedBlock,
    ValidatedBlock,
)


class SemanticExtractor:
    """Extracts structured semantic data from linked blocks."""

    def __init__(self):
        self.llm = get_llm_task_manager()

    def extract(
        self, linked_blocks: List[LinkedBlock], *, output_language: str = "fr"
    ) -> List[Dict[str, Any]]:
        """
        Extract semantic data from linked blocks.

        Returns:
            List of extracted semantic objects (definitions, theorems, etc.)
        """
        extracted = []

        for linked_block in tqdm(linked_blocks, desc="Extracting semantic data"):
            block = linked_block.block

            # Only extract from semantic target blocks (not context)
            if block.kind == BlockKind.context:
                continue

            # Get context from linked blocks
            context_text = self._get_context_text(linked_block, linked_blocks)

            # Extract based on block kind
            if block.kind == BlockKind.definition:
                result = self._extract_definition(
                    block, context_text, output_language=output_language
                )
                if result:
                    extracted.append(
                        {
                            "block_id": block.id,
                            "kind": "definition",
                            "data": result,
                        }
                    )

            elif block.kind in (
                BlockKind.theorem,
                BlockKind.proposition,
                BlockKind.lemma,
                BlockKind.corollary,
            ):
                result = self._extract_theorem(
                    block, context_text, linked_block, output_language=output_language
                )
                if result:
                    extracted.append(
                        {
                            "block_id": block.id,
                            "kind": "theorem",
                            "data": result,
                        }
                    )

            elif block.kind == BlockKind.formula:
                result = self._extract_formula(
                    block, context_text, output_language=output_language
                )
                if result:
                    extracted.append(
                        {
                            "block_id": block.id,
                            "kind": "formula",
                            "data": result,
                        }
                    )

            elif block.kind == BlockKind.proof:
                result = self._extract_proof(
                    block, context_text, linked_block, output_language=output_language
                )
                if result:
                    extracted.append(
                        {
                            "block_id": block.id,
                            "kind": "proof",
                            "data": result,
                        }
                    )

            elif block.kind == BlockKind.exercise:
                result = self._extract_exercise(
                    block, context_text, output_language=output_language
                )
                if result:
                    extracted.append(
                        {
                            "block_id": block.id,
                            "kind": "exercise",
                            "data": result,
                        }
                    )

        return extracted

    def _get_context_text(
        self, linked_block: LinkedBlock, all_blocks: List[LinkedBlock]
    ) -> str:
        """Get context text from preceding/following and attached context blocks."""
        context_parts = []

        # Preceding blocks
        for preceding_id in linked_block.block.preceding_blocks:
            preceding = self._find_linked_block(preceding_id, all_blocks)
            if preceding:
                context_parts.append(preceding.block.validated_text[:500])

        # Following blocks
        for following_id in linked_block.block.following_blocks:
            following = self._find_linked_block(following_id, all_blocks)
            if following:
                context_parts.append(following.block.validated_text[:500])

        # Attached context blocks
        for context_id in linked_block.context_blocks:
            context = self._find_linked_block(context_id, all_blocks)
            if context:
                context_parts.append(context.block.validated_text[:500])

        return "\n\n".join(context_parts)

    def _extract_definition(
        self,
        block: ValidatedBlock,
        context_text: str,
        *,
        output_language: str = "fr",
    ) -> Optional[ExtractedDefinition]:
        """Extract definition with splitting support."""
        from .language_detector import format_language_instruction

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Extract the definition(s) from this mathematical block.

### INPUT DATA
<<<< TARGET BLOCK START >>>>
Block (Original):
{block.validated_text}

Block (Normalized):
{block.normalized_text or "N/A"}
<<<< TARGET BLOCK END >>>>

CONTEXT (for reference only):
{context_text[:1000] or "None"}

Rules:
- **Strict Scope**: ONLY extract content found within the TARGET BLOCK. Do NOT include information from the CONTEXT.
- **CRITICAL: Statement Cleaning**: The `statement` field MUST contain ONLY the mathematical definition. 
  * REMOVE titles (e.g., "# Group Theory")
  * REMOVE keywords (e.g., "**Definition.**", "Définition :")
  * REMOVE introductory filler text.
- **CRITICAL: Term Identification**: Identify the main term being defined (e.g., "Group", "Compact set").
- **CRITICAL: Domain Tags**: Extract the mathematical domain (e.g., "analyse réelle", "algèbre linéaire"). **ALWAYS provide at least one tag.**
- If multiple definitions in the block, set `is_multiple: true` and populate the `definitions` list.
- Extract key characteristics (e.g., "fini", "ordre premier", "compact")
- **CRITICAL: JSON Escaping**: In the JSON output, all backslashes in LaTeX (e.g., `\cdot`, `\mathbb`) MUST be escaped as `\\` (e.g., `\\cdot`, `\\mathbb`).

{lang_instruction}

Respond in strict JSON:
{{
  "term": "main term" | null,
  "normalized_term": "normalized term" | null,
  "statement": "complete statement",
  "domain_tags": ["domain1", "domain2"],
  "characteristics": ["characteristic1", "characteristic2"],
  "is_multiple": true|false,
  "definitions": [
    {{"term": "...", "statement": "..."}},
    ...
  ]
}}"""

        try:
            response = self.llm.generate("extraction", prompt, expect_json=True)
            data = extract_json_obj(response)
            return ExtractedDefinition(**data)
        except Exception as e:
            print(f"WARNING: LLM definition extraction failed: {e}")
            # Fallback
            return ExtractedDefinition(
                term=None,
                statement=block.validated_text,
                is_multiple=False,
            )

    def _extract_theorem(
        self,
        block: ValidatedBlock,
        context_text: str,
        linked_block: LinkedBlock,
        *,
        output_language: str = "fr",
    ) -> Optional[ExtractedTheorem]:
        """Extract theorem with hypothesis/conclusion isolation."""
        from .language_detector import format_language_instruction

        # Find proof block ID
        proof_block_id = None
        for rel in linked_block.linked_to:
            if rel.get("relation") == "has_proof":
                proof_block_id = rel.get("block_id")

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Extract the theorem from this mathematical block.

### INPUT DATA
<<<< TARGET BLOCK START >>>>
Block (Original):
{block.validated_text}

Block (Normalized):
{block.normalized_text or "N/A"}
<<<< TARGET BLOCK END >>>>

CONTEXT (for reference only):
{context_text[:1000] or "None"}

Rules:
- **Strict Scope**: ONLY extract content found within the TARGET BLOCK. Do NOT include information from the CONTEXT.
- **IMPORTANT - Examples Are NOT Theorems**: Do NOT tag EXAMPLES as theorems. 
  * If the block starts with \"Example:\", \"Exemple :\", \"For instance\", \"Illustration\", or similar, it is an EXAMPLE, not a theorem.
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
- Extract the mathematical domain (e.g., "analyse réelle", "théorie des groupes"). **ALWAYS provide at least one tag.**
- Extract key characteristics (e.g., "monotone", "continu", "fini")

Examples:
1. "Théorème(Opérations sur les fonctions monotones)" → name: "Opérations sur les fonctions monotones", normalized_name: "Monotone functions operations"
2. "### Théorème de Pythagore" → name: "Théorème de Pythagore", normalized_name: "Pythagoras"
3. "**Fundamental Theorem of Calculus**" → name: "Fundamental Theorem of Calculus", normalized_name: "Fundamental theorem of calculus"

- **CRITICAL: JSON Escaping**: In the JSON output, all backslashes in LaTeX MUST be escaped as `\\`.

{lang_instruction}

Respond in strict JSON:
{{
  "name": "theorem name" | null,
  "normalized_name": "normalized name" | null,
  "hypotheses": ["hypothesis 1", "hypothesis 2"],
  "hypothesis_text": "complete hypothesis text",
  "conclusion": "conclusion",
  "conclusion_text": "complete conclusion text",
  "has_proof": true|false,
  "domain_tags": ["domain1", "domain2"],
  "characteristics": ["characteristic1", "characteristic2"]
}}"""

        try:
            response = self.llm.generate("extraction", prompt, expect_json=True)
            data = extract_json_obj(response)
            data["proof_block_id"] = proof_block_id
            return ExtractedTheorem(**data)
        except Exception as e:
            print(f"WARNING: LLM theorem extraction failed: {e}")
            # Fallback
            return ExtractedTheorem(
                name=None,
                hypotheses=[],
                conclusion=block.validated_text,
                conclusion_text=block.validated_text,
                has_proof=proof_block_id is not None,
            )

    def _extract_formula(
        self,
        block: ValidatedBlock,
        context_text: str,
        *,
        output_language: str = "fr",
    ) -> Optional[ExtractedFormula]:
        """Extract formula structure."""
        from .language_detector import format_language_instruction

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Extract the mathematical formula from this block.
        
### INPUT DATA
<<<< TARGET BLOCK START >>>>
Block (Original):
{block.validated_text}

Block (Normalized):
{block.normalized_text or "N/A"}
<<<< TARGET BLOCK END >>>>

CONTEXT (for reference only):
{context_text[:1000] or "None"}

Rules:
- **Strict Scope**: ONLY extract content found within the TARGET BLOCK. Do NOT include information from the CONTEXT.
- **CRITICAL: Statement Cleaning**: The `statement` field MUST contain ONLY the LaTeX formula/equation.
  * REMOVE titles (e.g., "### Binôme de Newton")
  * REMOVE keywords (e.g., "**Formule :**")
  * REMOVE descriptive text that is not part of the formula itself.
- **CRITICAL: Name Identification**: Identify the name of the formula (e.g., "Binôme de Newton", "Dérivée de ln").
- **CRITICAL: Domain Tags**: Extract the mathematical domain (e.g., "analyse", "probabilités"). **ALWAYS provide at least one tag.**
- Extract key characteristics (e.g., "identité", "inégalité", "approximation")
- **CRITICAL: JSON Escaping**: In the JSON output, all backslashes in LaTeX MUST be escaped as `\\`.

{lang_instruction}

Respond in strict JSON:
{{
  "name": "formula name" | null,
  "normalized_name": "normalized name" | null,
  "statement": "LaTeX formula",
  "domain_tags": ["domain1", "domain2"],
  "characteristics": ["characteristic1", "characteristic2"]
}}"""

        try:
            response = self.llm.generate("extraction", prompt, expect_json=True)
            data = extract_json_obj(response)
            return ExtractedFormula(**data)
        except Exception as e:
            print(f"WARNING: LLM formula extraction failed: {e}")
            return ExtractedFormula(
                name=None,
                statement=block.validated_text,
            )

    def _extract_proof(
        self,
        block: ValidatedBlock,
        context_text: str,
        linked_block: LinkedBlock,
        *,
        output_language: str = "fr",
    ) -> Optional[ExtractedProof]:
        """Extract proof structure."""
        from .language_detector import format_language_instruction

        # Find theorem block ID
        theorem_block_id = None
        for rel in linked_block.linked_to:
            if rel.get("relation") == "proves":
                theorem_block_id = rel.get("block_id")

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Extract the structure of this proof.

Block:
{block.validated_text}

Context (may be empty):
{context_text[:1000]}

Rules:
- Identify the main steps of the proof
- Identify definitions used (mentioned in the text)
- Identify theorems used (mentioned in the text)

{lang_instruction}

Respond in strict JSON:
{{
  "steps": ["step 1", "step 2", ...],
  "uses_definitions": ["definition X", "definition Y"],
  "uses_theorems": ["theorem A", "theorem B"]
}}"""

        try:
            response = self.llm.generate("extraction", prompt, expect_json=True)
            data = extract_json_obj(response)
            data["theorem_block_id"] = theorem_block_id
            return ExtractedProof(**data)
        except Exception as e:
            print(f"WARNING: LLM proof extraction failed: {e}")
            return ExtractedProof(
                steps=[],
                uses_definitions=[],
                uses_theorems=[],
                theorem_block_id=theorem_block_id,
            )

    def _extract_exercise(
        self,
        block: ValidatedBlock,
        context_text: str,
        *,
        output_language: str = "fr",
    ) -> Optional[ExtractedExercise]:
        """Extract exercise structure."""
        from .language_detector import format_language_instruction

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Extract the structure of this exercise.

Block:
{block.validated_text}

Context (may be empty):
{context_text[:1000]}

Rules:
- Identify the questions
- Identify solution steps (if present)
- Indicate if the exercise is solved

{lang_instruction}

Respond in strict JSON:
{{
  "questions": ["question 1", "question 2"],
  "solution_steps": ["step 1", "step 2"],
  "solved": true|false,
  "uses_concepts": ["concept1", "concept2"]
}}"""

        try:
            response = self.llm.generate("extraction", prompt, expect_json=True)
            data = extract_json_obj(response)
            return ExtractedExercise(**data)
        except Exception as e:
            print(f"WARNING: LLM exercise extraction failed: {e}")
            return ExtractedExercise(
                questions=[block.validated_text],
                solution_steps=[],
                solved=False,
                uses_concepts=[],
            )

    def _find_linked_block(
        self, block_id: str, all_blocks: List[LinkedBlock]
    ) -> Optional[LinkedBlock]:
        """Find linked block by block ID."""
        for linked_block in all_blocks:
            if linked_block.block.id == block_id:
                return linked_block
        return None
