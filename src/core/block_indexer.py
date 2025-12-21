"""
Phase 3: Block Indexing for Database

Creates indexes for database comparison:
- Normalized names
- Domain tags
- Embeddings (sentence-transformers)
- Key characteristics
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from .json_utils import extract_json_obj
from .llm_config import get_llm_task_manager
from .semantic_schemas import (
    ExtractedDefinition,
    ExtractedExercise,
    ExtractedProof,
    ExtractedTheorem,
    SemanticBlockIndex,
)

# sentence-transformers is lazy-loaded in BlockIndexer.embedding_model property


class BlockIndexer:
    """Creates database indexes for semantic blocks."""

    def __init__(self, embedding_model: Optional[str] = None):
        self.llm = get_llm_task_manager()
        self._embedding_model_instance = None
        self._embedding_model_name = (
            embedding_model
            or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self._tried_loading = False

    @property
    def embedding_model(self):
        """Lazy load the embedding model only when needed."""
        if self._embedding_model_instance is None and not self._tried_loading:
            self._tried_loading = True
            try:
                from sentence_transformers import SentenceTransformer

                print(
                    f"DEBUG: Loading embedding model {self._embedding_model_name} (this may take a few seconds)..."
                )
                self._embedding_model_instance = SentenceTransformer(
                    self._embedding_model_name
                )
            except Exception as e:
                print(f"WARNING: Failed to load embedding model: {e}")
        return self._embedding_model_instance

    def create_index(
        self,
        extracted_data: Dict[str, Any],
        *,
        language: str = "fr",
    ) -> SemanticBlockIndex:
        """
        Create index for extracted semantic data.

        Args:
            extracted_data: Dict with "kind" and "data" keys

        Returns:
            SemanticBlockIndex for database comparison
        """
        kind = extracted_data["kind"]
        data = extracted_data["data"]

        if kind == "definition":
            return self._index_definition(data, language=language)
        elif kind == "theorem":
            return self._index_theorem(data, language=language)
        elif kind == "proof":
            return self._index_proof(data, language=language)
        elif kind == "exercise":
            return self._index_exercise(data, language=language)
        else:
            # Fallback
            return SemanticBlockIndex(
                normalized_name=None,
                domain_tags=[],
                characteristics=[],
                embedding_text="",
                key_phrases=[],
            )

    def _index_definition(
        self, definition: ExtractedDefinition, *, language: str = "fr"
    ) -> SemanticBlockIndex:
        """Create index for definition."""
        # Use LLM for normalization if not already done
        normalized = definition.normalized_term
        if not normalized and definition.term:
            normalized = self._normalize_name(
                definition.term, "definition", output_language=language
            )

        # Build embedding text
        embedding_parts = []
        if normalized:
            embedding_parts.append(normalized)
        if definition.term:
            embedding_parts.append(definition.term)
        embedding_parts.append(definition.statement[:200])
        embedding_text = " | ".join(embedding_parts)

        # Extract key phrases
        key_phrases = self._extract_key_phrases(definition.statement)

        # Add language tag
        domain_tags = definition.domain_tags.copy()
        if language not in domain_tags:
            domain_tags.append(f"lang:{language}")

        return SemanticBlockIndex(
            normalized_name=normalized,
            domain_tags=domain_tags,
            characteristics=definition.characteristics,
            embedding_text=embedding_text,
            key_phrases=key_phrases,
        )

    def _index_theorem(
        self, theorem: ExtractedTheorem, *, language: str = "fr"
    ) -> SemanticBlockIndex:
        """Create index for theorem."""
        # Normalize name
        normalized = theorem.normalized_name
        if not normalized and theorem.name:
            normalized = self._normalize_name(
                theorem.name, "theorem", output_language=language
            )

        # Build embedding text
        embedding_parts = []
        if normalized:
            embedding_parts.append(normalized)
        if theorem.name:
            embedding_parts.append(theorem.name)
        if theorem.hypothesis_text:
            embedding_parts.append(theorem.hypothesis_text[:100])
        embedding_parts.append(theorem.conclusion_text[:200])
        embedding_text = " | ".join(embedding_parts)

        # Extract key phrases
        key_phrases = self._extract_key_phrases(theorem.conclusion_text)
        if theorem.hypothesis_text:
            key_phrases.extend(self._extract_key_phrases(theorem.hypothesis_text))

        # Add language tag
        domain_tags = theorem.domain_tags.copy()
        if language not in domain_tags:
            domain_tags.append(f"lang:{language}")

        return SemanticBlockIndex(
            normalized_name=normalized,
            domain_tags=domain_tags,
            characteristics=theorem.characteristics,
            embedding_text=embedding_text,
            key_phrases=key_phrases,
        )

    def _index_proof(
        self, proof: ExtractedProof, *, language: str = "fr"
    ) -> SemanticBlockIndex:
        """Create index for proof."""
        # Proofs are indexed by their theorem
        # This is mainly for reference
        proof_text = " | ".join(proof.steps[:3])  # First 3 steps

        # Add language tag
        domain_tags = [f"lang:{language}"]

        return SemanticBlockIndex(
            normalized_name=None,  # Proofs don't have names
            domain_tags=domain_tags,
            characteristics=[],
            embedding_text=proof_text[:200],
            key_phrases=self._extract_key_phrases(proof_text),
        )

    def _index_exercise(
        self, exercise: ExtractedExercise, *, language: str = "fr"
    ) -> SemanticBlockIndex:
        """Create index for exercise."""
        exercise_text = " | ".join(exercise.questions)

        # Add language tag
        domain_tags = [f"lang:{language}"]

        return SemanticBlockIndex(
            normalized_name=None,
            domain_tags=domain_tags,
            characteristics=[],
            embedding_text=exercise_text[:200],
            key_phrases=self._extract_key_phrases(exercise_text),
        )

    def _normalize_name(
        self, name: str, kind: str, *, output_language: str = "fr"
    ) -> Optional[str]:
        """Normalize mathematical name using LLM."""
        import os

        from .language_detector import format_language_instruction

        # Get normalization language from env (default: EN)
        norm_lang = os.getenv("NORMALIZED_NAME_LANGUAGE", "en").lower()

        lang_instruction = format_language_instruction(output_language)

        prompt = f"""Normalize this mathematical name to its standard form.

Name to normalize: "{name}"
Type: {kind}

**CRITICAL**: The normalized name MUST be in {norm_lang.upper()}, regardless of the input language.
This ensures consistency across all documents for duplicate detection and comparison.

Examples:
- "Sylow subgroup" / "sous-groupe de Sylow" → "Sylow" (EN)
- "Cayley-Hamilton theorem" / "théorème de Cayley-Hamilton" → "Cayley-Hamilton" (EN)
- "incomplete basis" / "base incomplète" → "incomplete basis" (EN, already normalized)
- "basis completion" / "complétion de base" → "incomplete basis" (EN)
- "Théorème de Cantor" → "Cantor" (EN)
- "Opérations sur les fonctions monotones" → "Monotone functions operations" (EN)

{lang_instruction}

Respond only with the normalized name in {norm_lang.upper()}, or "null" if no standard name exists.
Respond in JSON: {{"normalized": "name" | null}}"""

        try:
            response = self.llm.generate("normalization", prompt)
            data = extract_json_obj(response)
            return data.get("normalized")
        except Exception:
            return None

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text (simple heuristic)."""
        # Simple: extract phrases with mathematical terms
        # Could be enhanced with LLM
        phrases = []
        words = text.split()

        # Look for patterns like "théorème X", "définition Y", etc.
        for i in range(len(words) - 1):
            if words[i].lower() in ["théorème", "theorem", "définition", "definition"]:
                if i + 1 < len(words):
                    phrases.append(f"{words[i]} {words[i+1]}")

        return phrases[:5]  # Limit to 5 phrases

    def generate_embedding(self, embedding_text: str) -> Optional[np.ndarray]:
        """
        Generate embedding vector for text.

        Returns:
            numpy array of embeddings, or None if model not available
        """
        if not self.embedding_model:
            return None

        try:
            embedding = self.embedding_model.encode(
                embedding_text, convert_to_numpy=True
            )
            return embedding
        except Exception:
            return None

    def compare_blocks(
        self,
        index1: SemanticBlockIndex,
        index2: SemanticBlockIndex,
        *,
        use_embeddings: bool = True,
    ) -> float:
        """
        Compare two block indexes for similarity.

        Returns:
            Similarity score between 0 and 1
        """
        # 1. Exact name match
        if index1.normalized_name and index2.normalized_name:
            if index1.normalized_name.lower() == index2.normalized_name.lower():
                return 1.0

        # 2. Domain tag overlap
        domain_score = 0.0
        if index1.domain_tags and index2.domain_tags:
            common = set(index1.domain_tags) & set(index2.domain_tags)
            if common:
                domain_score = len(common) / max(
                    len(index1.domain_tags), len(index2.domain_tags)
                )

        # 3. Embedding similarity
        embedding_score = 0.0
        if use_embeddings and self.embedding_model:
            emb1 = self.generate_embedding(index1.embedding_text)
            emb2 = self.generate_embedding(index2.embedding_text)
            if emb1 is not None and emb2 is not None:
                # Cosine similarity
                dot_product = np.dot(emb1, emb2)
                norm1 = np.linalg.norm(emb1)
                norm2 = np.linalg.norm(emb2)
                if norm1 > 0 and norm2 > 0:
                    embedding_score = dot_product / (norm1 * norm2)
                    embedding_score = max(
                        0.0, min(1.0, embedding_score)
                    )  # Clamp to [0, 1]

        # 4. Key phrase overlap
        phrase_score = 0.0
        if index1.key_phrases and index2.key_phrases:
            common = set(index1.key_phrases) & set(index2.key_phrases)
            if common:
                phrase_score = len(common) / max(
                    len(index1.key_phrases), len(index2.key_phrases)
                )

        # Weighted combination
        final_score = (
            0.4 * embedding_score
            + 0.3 * domain_score
            + 0.2 * phrase_score
            + 0.1 * (1.0 if index1.normalized_name == index2.normalized_name else 0.0)
        )

        return final_score
