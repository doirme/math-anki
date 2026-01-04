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

import concurrent.futures
import os
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
        self._debug_counter = 0  # Counter for debug files

    def _debug_log_prompt(
        self, block: ValidatedBlock, extraction_type: str, prompt: str
    ):
        """Log extraction prompt to file for debugging."""
        import json
        from datetime import datetime
        from pathlib import Path

        # Create debug directory
        debug_dir = Path("./debug_extraction_logs")
        debug_dir.mkdir(exist_ok=True)

        # Increment counter
        self._debug_counter += 1

        # Generate safe filename from block info
        block_name = block.tags[0] if block.tags else "unknown"
        block_name = "".join(c if c.isalnum() else "_" for c in block_name)
        filename = f"{self._debug_counter:03d}_{block.kind}_{block_name}.txt"

        filepath = debug_dir / filename

        # Write log file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 100 + "\n")
            f.write(f"DEBUG EXTRACTION LOG\n")
            f.write("=" * 100 + "\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Block ID: {block.id}\n")
            f.write(f"Block Kind: {block.kind}\n")
            f.write(f"Block Tags: {block.tags}\n")
            f.write(f"Extraction Type: {extraction_type}\n")
            f.write(f"Self-contained: {block.is_self_contained}\n")
            f.write("=" * 100 + "\n\n")

            f.write("BLOCK STATE:\n")
            f.write("-" * 100 + "\n")
            f.write(f"Raw Text ({len(block.raw_text)} chars):\n{block.raw_text}\n\n")
            f.write(
                f"Validated Text ({len(block.validated_text)} chars):\n{block.validated_text}\n\n"
            )
            f.write(f"Normalized Text: {block.normalized_text or 'N/A'}\n\n")
            f.write(
                f"Metadata: {json.dumps(block.metadata, indent=2, ensure_ascii=False)}\n"
            )
            f.write("-" * 100 + "\n\n")

            f.write("PROMPT SENT TO LLM:\n")
            f.write("=" * 100 + "\n")
            f.write(prompt)
            f.write("\n" + "=" * 100 + "\n")

        print(f"🔍 DEBUG: Logged extraction prompt to {filepath}")

    def extract(
        self, linked_blocks: List[LinkedBlock], *, output_language: str = "fr"
    ) -> List[Dict[str, Any]]:
        """
        Extract semantic data from linked blocks in parallel.

        Returns:
            List of extracted semantic objects (definitions, theorems, etc.)
        """
        # DEBUG: Log all blocks BEFORE filtering
        if os.getenv("DEBUG_EXTRACTION", "false").lower() == "true":
            print(f"\n{'='*80}")
            print(f"DEBUG EXTRACTION: Received {len(linked_blocks)} linked blocks")
            print(f"{'='*80}")
            for lb in linked_blocks:
                print(
                    f"  Block {lb.block.id[:8]}: kind={lb.block.kind} (type={type(lb.block.kind).__name__})"
                )
            print(f"{'='*80}\n")

        # Filter blocks to extract (exclude context)
        blocks_to_process = [
            lb for lb in linked_blocks if lb.block.kind != BlockKind.context
        ]

        if not blocks_to_process:
            return []

        extracted = []

        # Determine number of workers (max 10 by default or via env)
        max_workers = int(os.getenv("MAX_EXTRACTION_WORKERS", "10"))

        # Use ThreadPoolExecutor for parallel extraction
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map blocks to processing function
            future_to_block = {
                executor.submit(
                    self._process_single_block, lb, linked_blocks, output_language
                ): lb
                for lb in blocks_to_process
            }

            # Collect results with progress bar
            for future in tqdm(
                concurrent.futures.as_completed(future_to_block),
                total=len(blocks_to_process),
                desc="Extracting semantic data (parallel)",
            ):
                result = future.result()
                if result:
                    extracted.append(result)

        # Sort extracted items to match original order of blocks for consistency
        block_id_to_order = {lb.block.id: i for i, lb in enumerate(linked_blocks)}
        extracted.sort(key=lambda x: block_id_to_order.get(x["block_id"], 999999))

        return extracted

    def _process_single_block(
        self,
        linked_block: LinkedBlock,
        all_blocks: List[LinkedBlock],
        output_language: str,
    ) -> Optional[Dict[str, Any]]:
        """Helper to process a single block for parallel extraction."""
        block = linked_block.block
        context_text = self._get_context_text(linked_block, all_blocks)

        if block.kind == BlockKind.definition:
            result = self._extract_definition(
                block, context_text, output_language=output_language
            )
            if result:
                return {"block_id": block.id, "kind": "definition", "data": result}

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
                return {
                    "block_id": block.id,
                    "kind": "theorem",
                    "data": result,
                }  # TODO: do we want ot force theorem here ?

        elif block.kind == BlockKind.formula:
            result = self._extract_formula(
                block, context_text, output_language=output_language
            )
            if result:
                return {"block_id": block.id, "kind": "formula", "data": result}

        elif block.kind == BlockKind.proof:
            result = self._extract_proof(
                block, context_text, linked_block, output_language=output_language
            )
            if result:
                return {"block_id": block.id, "kind": "proof", "data": result}

        elif block.kind == BlockKind.exercise:
            result = self._extract_exercise(
                block, context_text, output_language=output_language
            )
            if result:
                return {"block_id": block.id, "kind": "exercise", "data": result}

        return None

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
        # 1. Reuse existing metadata if sufficiently complete
        meta = block.metadata or {}
        if block.normalized_text and block.tags:
            # Basic check: if we have normalized text and tags, we might be able to skip
            # In many cases, the chunked extractor already gave us the core info.
            # However, ExtractedDefinition wants a 'term'.
            # We can infer it from normalized_name if present.
            term = (
                block.metadata.get("term")
                or block.normalized_text.split(":")[0].replace("**", "").strip()
            )

            return ExtractedDefinition(
                term=term,
                normalized_term=block.metadata.get("normalized_term") or term,
                statement=block.normalized_text,
                domain_tags=block.tags,
                characteristics=meta.get("characteristics", []),
                is_multiple=meta.get("is_multiple", False),
                definitions=meta.get("definitions", []),
            )

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
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
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
        # 1. Reuse existing metadata if sufficiently complete
        meta = block.metadata or {}

        # Find proof block ID
        proof_block_id = None
        for rel in linked_block.linked_to:
            if rel.get("relation") == "has_proof":
                proof_block_id = rel.get("block_id")

        # OPTIMIZATION DISABLED: Skip LLM call if metadata already exists
        # TODO: Re-enable after validating card quality with the proper check:
        #   if (block.normalized_text and meta.get("hypotheses") and meta.get("conclusion")
        #       and "equivalent_statements" in meta):
        #       # All required fields present, reuse existing metadata
        #       return ExtractedTheorem(...)
        #
        # This optimization saves LLM calls but MUST check for ALL required fields.
        # Without the equivalent_statements check, blocks from old cache would skip
        # extraction and never populate the new field.
        #
        # if block.normalized_text and meta.get("hypotheses") and meta.get("conclusion"):
        #     return ExtractedTheorem(
        #         name=meta.get("name")
        #         or block.normalized_text.split(":")[0].replace("**", "").strip(),
        #         normalized_name=meta.get("normalized_name")
        #         or block.normalized_text.split(":")[0].replace("**", "").strip(),
        #         hypotheses=meta.get("hypotheses"),
        #         conclusion=meta.get("conclusion"),
        #         equivalent_statements=meta.get("equivalent_statements", []),
        #         hypothesis_text="\n".join(meta.get("hypotheses", [])),
        #         conclusion_text=meta.get("conclusion", ""),
        #         domain_tags=block.tags,
        #         characteristics=meta.get("characteristics", []),
        #         has_proof=proof_block_id is not None,
        #         proof_block_id=proof_block_id,
        #     )

        from .language_detector import format_language_instruction

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

- **CRITICAL: JSON Escaping**: In the JSON output, all backslashes in LaTeX MUST be escaped as `\\`.

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

        # DEBUG MODE: Log prompt instead of calling LLM
        if os.getenv("DEBUG_EXTRACTION", "false").lower() == "true":
            self._debug_log_prompt(block, "theorem", prompt)
            # Return mock data in debug mode
            return ExtractedTheorem(
                name="DEBUG_MODE",
                hypotheses=[],
                conclusion="Debug mode active - no LLM call",
                conclusion_text="Debug mode active",
                has_proof=proof_block_id is not None,
                proof_block_id=proof_block_id,
            )

        try:
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
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
        # 1. Reuse existing metadata if sufficiently complete
        if block.normalized_text and block.kind == BlockKind.formula:
            return ExtractedFormula(
                name=block.normalized_text.split(":")[0].replace("**", "").strip()
                if ":" in block.normalized_text
                else None,
                normalized_name=block.metadata.get("normalized_name")
                if block.metadata
                else None,
                statement=block.normalized_text,
                domain_tags=block.tags,
                characteristics=block.metadata.get("characteristics", [])
                if block.metadata
                else [],
            )

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
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
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
        # 1. Reuse existing metadata if sufficiently complete
        meta = block.metadata or {}

        # Find theorem block ID
        theorem_block_id = None
        for rel in linked_block.linked_to:
            if rel.get("relation") == "proves":
                theorem_block_id = rel.get("block_id")

        if meta.get("steps"):
            return ExtractedProof(
                steps=meta.get("steps"),
                uses_definitions=meta.get("uses_definitions", []),
                uses_theorems=meta.get("uses_theorems", []),
                theorem_block_id=theorem_block_id,
            )

        from .language_detector import format_language_instruction

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
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
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
        # 1. Reuse existing metadata if sufficiently complete
        meta = block.metadata or {}

        if meta.get("questions") or meta.get(
            "steps"
        ):  # Steps might contain solution steps
            return ExtractedExercise(
                questions=meta.get("questions")
                or [block.normalized_text or block.validated_text],
                solution_steps=meta.get("steps") or [],
                solved=meta.get("solved", False) or len(meta.get("steps", [])) > 0,
                uses_concepts=meta.get("uses_concepts", []),
            )

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
            response = self.llm.generate(
                prompt=prompt, task_name="extraction", expect_json=True
            )
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
