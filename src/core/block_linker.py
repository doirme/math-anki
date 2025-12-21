"""
Block Linking: Detect relationships between blocks.

Links theorems to proofs, definitions to usages, and attaches context blocks.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from tqdm import tqdm

from .enums import BlockKind
from .enums import RelationPredicate as BlockRelation
from .json_utils import extract_json_obj
from .llm_config import get_llm_task_manager
from .semantic_schemas import LinkedBlock, ValidatedBlock


class BlockLinker:
    """Detects and establishes relationships between blocks."""

    def __init__(self):
        self.llm = get_llm_task_manager()

    def link_blocks(
        self, blocks: List[ValidatedBlock], *, output_language: str = "fr"
    ) -> List[LinkedBlock]:
        """
        Detect relationships between blocks.

        Returns:
            List of linked blocks with relationships established
        """
        linked = []

        for block in tqdm(blocks, desc="Linking blocks"):
            # Detect relationships
            relationships = self._detect_relationships(block, blocks, output_language)

            # Attach context blocks
            context_blocks = self._find_context_blocks(block, blocks)

            linked_block = LinkedBlock(
                block=block,
                linked_to=relationships,
                context_blocks=context_blocks,
            )
            linked.append(linked_block)

        return linked

    def _detect_relationships(
        self,
        block: ValidatedBlock,
        all_blocks: List[ValidatedBlock],
        output_language: str = "fr",
    ) -> List[Dict]:
        """
        Detect relationships for a block.

        Returns:
            List of {block_id, relation, confidence} dicts
        """
        relationships = []

        # Quick heuristics first
        if block.kind == BlockKind.proof:
            # Find theorem this proof belongs to
            theorem = self._find_related_theorem(block, all_blocks)
            if theorem:
                relationships.append(
                    {
                        "block_id": theorem.id,
                        "relation": BlockRelation.proves.value,
                        "confidence": 0.9,
                    }
                )

        elif block.kind in (
            BlockKind.theorem,
            BlockKind.proposition,
            BlockKind.lemma,
            BlockKind.formula,
        ):
            # Find proof for this theorem
            proof = self._find_related_proof(block, all_blocks)
            if proof:
                relationships.append(
                    {
                        "block_id": proof.id,
                        "relation": BlockRelation.has_proof.value,
                        "confidence": 0.9,
                    }
                )

        # Use LLM for more complex relationships OR as fallback if heuristics failed
        # If we found no relationships yet, specifically check following blocks with LLM
        if not relationships and block.following_blocks:
            llm_relationships = self._detect_llm_relationships(
                block,
                all_blocks,
                output_language=output_language,
                force_candidates=True,  # Force checking following blocks
            )
            relationships.extend(llm_relationships)
        else:
            # Normal LLM check for additional relationships
            llm_relationships = self._detect_llm_relationships(
                block, all_blocks, output_language=output_language
            )
            relationships.extend(llm_relationships)

        return relationships

    def _find_related_theorem(
        self,
        proof_block: ValidatedBlock,
        all_blocks: List[ValidatedBlock],
    ) -> Optional[ValidatedBlock]:
        """Find theorem that this proof belongs to."""
        # Look in preceding blocks
        for preceding_id in proof_block.preceding_blocks:
            preceding = self._find_block_by_id(preceding_id, all_blocks)
            if preceding and preceding.kind in (
                BlockKind.theorem,
                BlockKind.proposition,
                BlockKind.lemma,
                BlockKind.formula,
            ):
                return preceding
                # Check if proof mentions this theorem
                # if self._mentions_block(proof_block.validated_text, preceding.validated_text):
                #     return preceding

        # Look in following blocks (less common)
        for following_id in proof_block.following_blocks:
            following = self._find_block_by_id(following_id, all_blocks)
            if following and following.kind in (
                BlockKind.theorem,
                BlockKind.proposition,
                BlockKind.lemma,
                BlockKind.formula,
            ):
                if self._mentions_block(
                    proof_block.validated_text, following.validated_text
                ):
                    return following

        return None

    def _find_related_proof(
        self,
        theorem_block: ValidatedBlock,
        all_blocks: List[ValidatedBlock],
    ) -> Optional[ValidatedBlock]:
        """Find proof for this theorem."""
        # Look in following blocks
        for following_id in theorem_block.following_blocks:
            following = self._find_block_by_id(following_id, all_blocks)
            if following and following.kind == BlockKind.proof:
                # Check if proof mentions this theorem
                # if self._mentions_block(following.validated_text, theorem_block.validated_text):
                return following

        return None

    def _detect_llm_relationships(
        self,
        block: ValidatedBlock,
        all_blocks: List[ValidatedBlock],
        *,
        output_language: str = "fr",
        force_candidates: bool = False,
    ) -> List[Dict]:
        """Use LLM to detect relationships."""
        from .language_detector import format_language_instruction

        lang_instruction = format_language_instruction(output_language)
        # Get candidate blocks (preceding + following + same page)
        candidates = []

        if force_candidates:
            # When heuristics failed, specifically check following blocks
            for following_id in block.following_blocks:
                candidate = self._find_block_by_id(following_id, all_blocks)
                if candidate:
                    candidates.append(candidate)
        else:
            # Normal case: check both preceding and following
            for candidate_id in block.preceding_blocks + block.following_blocks:
                candidate = self._find_block_by_id(candidate_id, all_blocks)
                if candidate:
                    candidates.append(candidate)

        if not candidates:
            return []

        candidates_text = "\n\n".join(
            [
                f"[Block {c.id} - {c.kind.value}]: {c.validated_text[:200]}"
                for c in candidates[:5]  # Limit to 5 candidates
            ]
        )

        prompt = f"""Analyze the relationships between this mathematical block and candidate blocks.

Block to analyze:
[Block {block.id} - {block.kind.value}]
{block.validated_text[:500]}

Candidate blocks:
{candidates_text}

Detect possible relationships:
- "has_proof": this block has a proof in another block
- "proves": this block proves a theorem in another block
- "uses_definition": this block uses a definition from another block
- "uses_theorem": this block uses a theorem from another block
- "generalizes": this block generalizes another block
- "specializes": this block specializes another block

{lang_instruction}

Respond in strict JSON:
{{
  "relationships": [
    {{"block_id": "...", "relation": "uses_definition", "confidence": 0.8, "reason": "..."}},
    ...
  ]
}}"""

        try:
            response = self.llm.generate(
                prompt=prompt, task_name="block_linking", expect_json=True
            )
            data = extract_json_obj(response)
            return data.get("relationships", [])
        except Exception:
            return []

    def _find_context_blocks(
        self,
        block: ValidatedBlock,
        all_blocks: List[ValidatedBlock],
    ) -> List[str]:
        """
        Find context blocks (non-semantic) that should be attached to this block.

        Context blocks are explanations, examples, remarks that aren't semantic targets.
        """
        context_ids = []

        # Look for context blocks nearby
        for preceding_id in block.preceding_blocks:
            preceding = self._find_block_by_id(preceding_id, all_blocks)
            if preceding and preceding.kind == BlockKind.context:
                context_ids.append(preceding_id)

        for following_id in block.following_blocks:
            following = self._find_block_by_id(following_id, all_blocks)
            if following and following.kind == BlockKind.context:
                context_ids.append(following_id)

        return context_ids

    def _find_block_by_id(
        self, block_id: str, all_blocks: List[ValidatedBlock]
    ) -> Optional[ValidatedBlock]:
        """Find block by ID."""
        for block in all_blocks:
            if block.id == block_id:
                return block
        return None

    def _mentions_block(self, text: str, other_text: str) -> bool:
        """Check if text mentions concepts from other_text."""
        # Simple heuristic: check for common phrases
        other_first_100 = other_text[:100].lower()
        # Look for theorem names, definitions mentioned
        # This is a simple heuristic; LLM does better
        return len(other_first_100) > 20 and any(
            word in text.lower()
            for word in other_first_100.split()[:5]
            if len(word) > 4
        )
