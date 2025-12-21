"""
Database utilities for Streamlit UI
Handles saving blocks, duplicate detection, and retrieval
"""

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.block_indexer import BlockIndexer
from core.enums import BlockKind
from db.models import Document, SemanticBlock, Tag
from db.session import get_db_session


class DatabaseManager:
    """Manages database operations for Streamlit app"""

    def __init__(self):
        self.indexer = BlockIndexer()

    def save_document(self, pdf_path: str, md_text: str) -> int:
        """
        Save document to database

        Returns:
            Document ID
        """
        with get_db_session() as session:
            # Calculate hash
            file_hash = hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest()[:16]

            # Check if already exists
            existing = session.query(Document).filter_by(source_hash=file_hash).first()
            if existing:
                return existing.id

            # Create new document
            doc = Document(
                title=Path(pdf_path).stem,
                source_path=str(pdf_path),
                source_hash=file_hash,
                created_at=datetime.utcnow(),
                language="fr",
                subject_area="math",
            )

            session.add(doc)
            session.flush()

            return doc.id

    def save_blocks(
        self,
        blocks: List[Dict[str, Any]],
        document_id: int,
        generate_embeddings: bool = True,
    ) -> List[int]:
        """
        Save validated blocks to database with optional embedding generation

        Args:
            blocks: List of validated block dictionaries
            document_id: Document ID to link blocks to
            generate_embeddings: Whether to generate embeddings for duplicate detection

        Returns:
            List of created SemanticBlock IDs
        """
        with get_db_session() as session:
            block_ids = []

            for block_data in blocks:
                # Map kind string to BlockKind enum
                kind_str = block_data.get("kind", "unknown")
                kind = self._map_kind(kind_str)

                # Create semantic block
                semantic_block = SemanticBlock(
                    kind=kind,
                    name=self._extract_name(block_data),
                    summary=block_data.get("normalized_text", ""),
                    created_at=datetime.utcnow(),
                )

                session.add(semantic_block)
                session.flush()

                # Add tags
                for tag_name in block_data.get("tags", []):
                    tag = session.query(Tag).filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        session.add(tag)
                    semantic_block.tags.append(tag)

                # Generate and store embeddings if requested
                if generate_embeddings:
                    self._generate_and_store_embedding(semantic_block, block_data)

                block_ids.append(semantic_block.id)

            return block_ids

    def find_duplicates(
        self, blocks: List[Dict[str, Any]], threshold: float = 0.85
    ) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]]]]:
        """
        Find potential duplicates for given blocks

        Args:
            blocks: New blocks to check
            threshold: Similarity threshold (0.0-1.0)

        Returns:
            List of (new_block, [similar_existing_blocks])
        """
        duplicates = []

        with get_db_session() as session:
            for block in blocks:
                kind = self._map_kind(block.get("kind", "unknown"))

                # Query existing blocks of same kind
                existing_blocks = (
                    session.query(SemanticBlock).filter_by(kind=kind).all()
                )

                similar_blocks = []

                for existing in existing_blocks:
                    # Simple name-based comparison for now
                    # TODO: Use embeddings for better comparison
                    if self._is_similar(block, existing):
                        similar_blocks.append(
                            {
                                "id": existing.id,
                                "name": existing.name,
                                "summary": existing.summary[:200],
                                "created_at": existing.created_at.isoformat(),
                            }
                        )

                if similar_blocks:
                    duplicates.append((block, similar_blocks))

        return duplicates

    def get_all_blocks(self, kind: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all blocks from database

        Args:
            kind: Optional filter by block kind

        Returns:
            List of block dictionaries
        """
        with get_db_session() as session:
            query = session.query(SemanticBlock)

            if kind:
                kind_enum = self._map_kind(kind)
                query = query.filter_by(kind=kind_enum)

            blocks = query.all()

            return [
                {
                    "id": b.id,
                    "kind": b.kind.value,
                    "name": b.name,
                    "summary": b.summary,
                    "tags": [t.name for t in b.tags],
                    "created_at": b.created_at.isoformat() if b.created_at else None,
                }
                for b in blocks
            ]

    def delete_block(self, block_id: int):
        """Delete a block from database"""
        with get_db_session() as session:
            block = session.query(SemanticBlock).filter_by(id=block_id).first()
            if block:
                session.delete(block)

    def merge_blocks(self, keep_id: int, delete_ids: List[int]):
        """
        Merge multiple blocks into one

        Args:
            keep_id: ID of block to keep
            delete_ids: IDs of blocks to delete
        """
        with get_db_session() as session:
            keep_block = session.query(SemanticBlock).filter_by(id=keep_id).first()
            if not keep_block:
                return

            # Merge tags from deleted blocks
            for del_id in delete_ids:
                del_block = session.query(SemanticBlock).filter_by(id=del_id).first()
                if del_block:
                    for tag in del_block.tags:
                        if tag not in keep_block.tags:
                            keep_block.tags.append(tag)
                    session.delete(del_block)

    def filter_blocks(
        self,
        kinds: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        document_ids: Optional[List[int]] = None,
        search_text: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Advanced filtering of database blocks

        Args:
            kinds: Filter by block types (theorem, definition, etc.)
            tags: Filter by tags (must have ALL specified tags)
            document_ids: Filter by source document IDs
            search_text: Search in name and summary

        Returns:
            List of filtered block dictionaries with source information
        """
        with get_db_session() as session:
            from db.models import SemanticSourceLink, TextBlock

            query = session.query(SemanticBlock)

            # Filter by kind
            if kinds:
                kind_enums = [self._map_kind(k) for k in kinds]
                query = query.filter(SemanticBlock.kind.in_(kind_enums))

            # Filter by tags
            if tags:
                for tag_name in tags:
                    query = query.join(SemanticBlock.tags).filter(Tag.name == tag_name)

            # Filter by document source
            if document_ids:
                query = (
                    query.join(SemanticBlock.sources)
                    .join(SemanticSourceLink.text_block)
                    .filter(TextBlock.document_id.in_(document_ids))
                )

            # Search in text
            if search_text:
                search_pattern = f"%{search_text}%"
                query = query.filter(
                    (SemanticBlock.name.ilike(search_pattern))
                    | (SemanticBlock.summary.ilike(search_pattern))
                )

            blocks = query.distinct().all()

            # Enrich with source documents
            result = []
            for block in blocks:
                # Get all source documents for this block
                source_docs = []
                for source_link in block.sources:
                    if source_link.text_block and source_link.text_block.document:
                        doc = source_link.text_block.document
                        source_docs.append(
                            {
                                "id": doc.id,
                                "title": doc.title,
                                "source_path": doc.source_path,
                            }
                        )

                result.append(
                    {
                        "id": block.id,
                        "kind": block.kind.value,
                        "name": block.name,
                        "summary": block.summary,
                        "tags": [t.name for t in block.tags],
                        "created_at": block.created_at.isoformat()
                        if block.created_at
                        else None,
                        "sources": source_docs,
                        "source_count": len(source_docs),
                    }
                )

            return result

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get list of all documents in database

        Returns:
            List of document dictionaries
        """
        with get_db_session() as session:
            docs = session.query(Document).all()

            return [
                {
                    "id": d.id,
                    "title": d.title,
                    "source_path": d.source_path,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                }
                for d in docs
            ]

    def get_all_tags(self) -> List[str]:
        """
        Get list of all unique tags in database

        Returns:
            List of tag names
        """
        with get_db_session() as session:
            tags = session.query(Tag).all()
            return [t.name for t in tags]

    def get_blocks_by_ids(self, block_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Retrieve specific blocks by their IDs

        Args:
            block_ids: List of block IDs to retrieve

        Returns:
            List of block dictionaries
        """
        with get_db_session() as session:
            blocks = (
                session.query(SemanticBlock)
                .filter(SemanticBlock.id.in_(block_ids))
                .all()
            )

            return [
                {
                    "id": b.id,
                    "kind": b.kind.value,
                    "name": b.name,
                    "summary": b.summary,
                    "tags": [t.name for t in b.tags],
                    "created_at": b.created_at.isoformat() if b.created_at else None,
                }
                for b in blocks
            ]

    # Helper methods

    def _map_kind(self, kind_str: str) -> BlockKind:
        """Map string kind to BlockKind enum"""
        mapping = {
            "theorem": BlockKind.theorem,
            "definition": BlockKind.definition,
            "proof": BlockKind.proof,
            "example": BlockKind.example,
            "exercise": BlockKind.exercise,
            "lemma": BlockKind.lemma,
            "corollary": BlockKind.corollary,
            "proposition": BlockKind.proposition,
            "remark": BlockKind.remark,
        }
        return mapping.get(kind_str.lower(), BlockKind.unknown)

    def _extract_name(self, block_data: Dict[str, Any]) -> Optional[str]:
        """Extract name from block data"""
        tags = block_data.get("tags", [])
        return tags[0] if tags else None

    def _generate_and_store_embedding(self, semantic_block, block_data):
        """Generate embedding for block (placeholder for now)"""
        # TODO: Store embedding in database
        # This would require adding an embedding column to SemanticBlock
        embedding_text = block_data.get("normalized_text", "")
        if embedding_text and self.indexer.embedding_model:
            embedding = self.indexer.generate_embedding(embedding_text)
            # Store embedding (need to add column to DB schema first)

    def _is_similar(self, new_block: Dict, existing_block) -> bool:
        """Check if two blocks are similar (simple heuristic)"""
        # Simple name-based comparison
        new_name = self._extract_name(new_block) or ""
        existing_name = existing_block.name or ""

        if new_name and existing_name:
            return new_name.lower() == existing_name.lower()

        # Fallback to summary comparison
        new_summary = new_block.get("normalized_text", "")[:100].lower()
        existing_summary = (existing_block.summary or "")[:100].lower()

        if len(new_summary) > 20 and len(existing_summary) > 20:
            # Simple substring check
            return new_summary in existing_summary or existing_summary in new_summary

        return False
