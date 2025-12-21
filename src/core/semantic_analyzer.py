"""
Main Semantic Analyzer Orchestrator

Coordinates all phases of semantic analysis:
1. Block creation with validation
2. Block linking
3. Semantic extraction
4. Block indexing
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .block_creator import BlockCreator
from .block_indexer import BlockIndexer
from .block_linker import BlockLinker
from .config import settings
from .language_detector import detect_language
from .semantic_extractor import SemanticExtractor
from .semantic_schemas import SemanticBlockIndex


class SemanticAnalyzer:
    """Main orchestrator for semantic analysis pipeline."""
    
    def __init__(self, embedding_model: Optional[str] = None):
        self.block_creator = BlockCreator()
        self.block_linker = BlockLinker()
        self.extractor = SemanticExtractor()
        self.indexer = BlockIndexer(embedding_model=embedding_model)
    
    def analyze(
        self,
        md_text: str,
        *,
        context_window: int = 3,
        generate_embeddings: bool = True,
        output_language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze markdown and extract semantic blocks.
        
        Args:
            md_text: Markdown text to analyze
            context_window: Number of preceding/following blocks to consider
            generate_embeddings: Whether to generate embeddings
            output_language: Output language ("fr", "en", etc.). If "auto" or None, detects from text.
        
        Returns:
            Dict with:
            - blocks: List of validated blocks
            - linked_blocks: List of linked blocks
            - extracted: List of extracted semantic data
            - indexes: List of block indexes
            - language: Detected/used language code
        """
        # Determine output language
        if output_language is None or output_language == "auto":
            output_language = settings.output_language
        
        if output_language == "auto":
            # Detect language from markdown
            output_language = detect_language(md_text)
        
        # Phase 1: Create and validate blocks
        validated_blocks = self.block_creator.create_blocks(
            md_text,
            context_window=context_window,
            output_language=output_language,
        )
        
        # Phase 2: Link blocks
        linked_blocks = self.block_linker.link_blocks(validated_blocks, output_language=output_language)
        
        # Phase 3: Extract semantic data
        extracted = self.extractor.extract(linked_blocks, output_language=output_language)
        
        # Phase 4: Create indexes
        indexes = []
        for item in extracted:
            index = self.indexer.create_index(item, language=output_language)
            indexes.append({
                "block_id": item["block_id"],
                "kind": item["kind"],
                "index": index,
                "embedding": None,
            })
            
            # Generate embedding if requested
            if generate_embeddings:
                embedding = self.indexer.generate_embedding(index.embedding_text)
                if embedding is not None:
                    indexes[-1]["embedding"] = embedding.tolist()  # Convert to list for JSON
        
        return {
            "blocks": [b.model_dump() for b in validated_blocks],
            "linked_blocks": [
                {
                    "block": lb.block.model_dump(),
                    "linked_to": lb.linked_to,
                    "context_blocks": lb.context_blocks,
                }
                for lb in linked_blocks
            ],
            "extracted": [
                {
                    "block_id": item["block_id"],
                    "kind": item["kind"],
                    "data": item["data"].model_dump() if hasattr(item["data"], "model_dump") else item["data"],
                }
                for item in extracted
            ],
            "indexes": indexes,
            "language": output_language,
        }
    
    def find_similar_blocks(
        self,
        target_index: SemanticBlockIndex,
        candidate_indexes: List[SemanticBlockIndex],
        *,
        threshold: float = 0.7,
    ) -> List[tuple]:
        """
        Find blocks similar to target.
        
        Args:
            target_index: Index to compare against
            candidate_indexes: List of candidate indexes
            threshold: Minimum similarity score
        
        Returns:
            List of (index, score) tuples, sorted by score descending
        """
        similarities = []
        for candidate in candidate_indexes:
            score = self.indexer.compare_blocks(target_index, candidate)
            if score >= threshold:
                similarities.append((candidate, score))
        
        # Sort by score descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

