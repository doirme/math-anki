from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from typing import Any, Dict, List, Optional

from core.enums import BlockKind, SourceRole
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models


@dataclass
class Batch:
    documents: list[dict]
    text_blocks: list[dict]
    semantic_blocks: list[dict]
    source_links: list[dict]
    relations: list[dict]


def _hash(text: str) -> str:
    return sha1(text.encode("utf-8")).hexdigest()


class SemanticPersister:
    def __init__(self, session: Session):
        self.s = session

    def _upsert_document(self, d: dict) -> models.Document:
        # Start building a SELECT query targeting the Document model
        q = select(models.Document)

        # Check if we have unique identifiers (hash + path) to find an existing document
        if d.get("source_hash") and d.get("md_path"):
            # Add WHERE clause: WHERE source_hash = ... AND md_path = ...
            q = q.where(
                models.Document.source_hash == d["source_hash"],
                models.Document.md_path == d["md_path"],
            )
        else:
            # Fallback: try to find by title and source path
            # Add WHERE clause: WHERE title = ... AND source_path = ...
            q = q.where(
                models.Document.title == d.get("title"),
                models.Document.source_path == d.get("source_path"),
            )

        # Execute the query and retrieve a single result (or None if not found)
        # scalar_one_or_none() returns the object directly or None
        obj = self.s.execute(q).scalar_one_or_none()

        # If the document exists, update its fields
        if obj:
            for k, v in d.items():
                setattr(obj, k, v)  # Update attribute k with value v
            return obj

        # If not found, create a new Document instance
        obj = models.Document(**d)  # Unpack dict d as arguments
        self.s.add(obj)  # Add to the session (staged for commit)
        self.s.flush()  # Flush to DB to generate the ID immediately
        return obj

    def _upsert_text_block(self, t: dict) -> models.TextBlock:
        if not t.get("content_hash"):
            t["content_hash"] = _hash(t.get("raw_text") or "")
        q = select(models.TextBlock).where(
            models.TextBlock.document_id == t["document_id"],
            models.TextBlock.content_hash == t["content_hash"],
        )
        obj = self.s.execute(q).scalar_one_or_none()
        if obj:
            for k in (
                "block_index",
                "page_number",
                "heading_path",
                "block_type_hint",
                "normalized_text",
            ):
                if k in t and t[k] is not None:
                    setattr(obj, k, t[k])
            return obj
        obj = models.TextBlock(**t)
        self.s.add(obj)
        self.s.flush()
        return obj

    def _insert_semantic_block(self, sdata: dict) -> models.SemanticBlock:
        # Try to find existing block by name and kind to avoid duplicates if re-running
        if sdata.get("name"):
            q = select(models.SemanticBlock).where(
                models.SemanticBlock.kind == sdata["kind"],
                models.SemanticBlock.name == sdata["name"],
            )
            obj = self.s.execute(q).scalar_one_or_none()
            if obj:
                for k in (
                    "short_slug",
                    "summary",
                    "importance_score",
                    "statement_id",
                    "hypotheses_id",
                    "conclusion_id",
                    "math_object_id",
                ):
                    if k in sdata and sdata[k] is not None:
                        setattr(obj, k, sdata[k])
                return obj

        obj = models.SemanticBlock(**sdata)
        self.s.add(obj)
        self.s.flush()
        return obj

    def _get_or_create_tag(self, name: str) -> models.Tag:
        q = select(models.Tag).where(models.Tag.name == name)
        tag = self.s.execute(q).scalar_one_or_none()
        if not tag:
            tag = models.Tag(name=name)
            self.s.add(tag)
            self.s.flush()
        return tag

    def _add_tag(self, semantic_block: models.SemanticBlock, tag_name: str):
        tag = self._get_or_create_tag(tag_name)
        if tag not in semantic_block.tags:
            semantic_block.tags.append(tag)

    def persist_analysis_results(
        self, results: Dict[str, Any], doc_title: str, doc_path: str
    ):
        """
        Persist the results of SemanticAnalyzer.analyze to the database.
        """
        # 1. Create/Get Document
        doc_data = {
            "title": doc_title,
            "source_path": doc_path,
            "md_path": doc_path,  # simplified
            "language": results.get("language", "fr"),
        }
        doc = self._upsert_document(doc_data)

        # 2. Persist TextBlocks (from results["blocks"])
        # Map block_id (str) -> TextBlock.id (int)
        text_block_map: Dict[str, int] = {}

        for i, block_data in enumerate(results["blocks"]):
            # block_data is a dict (ValidatedBlock.dict())
            tb_data = {
                "document_id": doc.id,
                "block_index": i,
                "page_number": block_data.get("page"),
                "raw_text": block_data.get("raw_text"),
                "normalized_text": block_data.get("validated_text"),
                "content_hash": _hash(block_data.get("raw_text") or ""),
                "block_type_hint": block_data.get("kind"),
            }
            tb = self._upsert_text_block(tb_data)
            text_block_map[block_data["id"]] = tb.id

        # 3. Persist SemanticBlocks (from results["extracted"])
        # Map block_id (str) -> SemanticBlock.id (int)
        semantic_block_map: Dict[str, int] = {}

        # First pass: Create SemanticBlocks without relationships
        for item in results["extracted"]:
            block_id = item["block_id"]
            kind_str = item["kind"]
            data = item["data"]  # dict

            # Map string kind to Enum
            try:
                kind = BlockKind(kind_str)
            except ValueError:
                kind = BlockKind.unknown

            # Handle name mapping (Definition uses 'term', Theorem uses 'name')
            name = data.get("name")
            if not name and kind == BlockKind.definition:
                name = data.get("term")

            sb_data = {
                "kind": kind,
                "name": name,
                "summary": data.get("statement")
                or data.get("conclusion")
                or data.get("raw_text"),
                # TODO: Add importance score, etc.
            }

            sb = self._insert_semantic_block(sb_data)
            semantic_block_map[block_id] = sb.id

            # Special handling for Theorem/Proposition/Lemma to store structured data
            if kind in (
                BlockKind.theorem,
                BlockKind.proposition,
                BlockKind.lemma,
                BlockKind.corollary,
            ):
                # Handle Hypotheses
                hyps = data.get("hypotheses", [])
                if hyps:
                    hyp_text = "\n".join(hyps) if isinstance(hyps, list) else str(hyps)
                    hyp_block = self._insert_semantic_block(
                        {
                            "kind": BlockKind.unknown,
                            "summary": hyp_text,
                            "name": "Hypothèses",
                        }
                    )
                    sb.hypotheses_id = hyp_block.id

                # Handle Conclusion
                conc = data.get("conclusion")
                if conc:
                    conc_block = self._insert_semantic_block(
                        {
                            "kind": BlockKind.unknown,
                            "summary": conc,
                            "name": "Conclusion",
                        }
                    )
                    sb.conclusion_id = conc_block.id

            # Link to TextBlock
            if block_id in text_block_map:
                # Check if link exists
                q = select(models.SemanticSourceLink).where(
                    models.SemanticSourceLink.semantic_block_id == sb.id,
                    models.SemanticSourceLink.text_block_id == text_block_map[block_id],
                )
                link = self.s.execute(q).scalar_one_or_none()
                if not link:
                    self.s.add(
                        models.SemanticSourceLink(
                            semantic_block_id=sb.id,
                            text_block_id=text_block_map[block_id],
                            role=SourceRole.full,
                        )
                    )

            # Handle Tags
            if "domain_tags" in data and data["domain_tags"]:
                for tag_name in data["domain_tags"]:
                    self._add_tag(sb, tag_name)

        self.s.flush()

        # Second pass: Link SemanticBlocks (relationships)
        # This requires parsing the relationships from the extracted data or linked_blocks
        # For now, we'll handle basic relationships if present in extracted data (like proof -> theorem)

        for item in results["extracted"]:
            block_id = item["block_id"]
            data = item["data"]

            if block_id not in semantic_block_map:
                continue

            sb_id = semantic_block_map[block_id]

            # Example: Theorem has proof_block_id
            if "proof_block_id" in data and data["proof_block_id"]:
                proof_id_str = data["proof_block_id"]
                if proof_id_str in semantic_block_map:
                    proof_sb_id = semantic_block_map[proof_id_str]

                    # Create relation: Proof PROVES Theorem
                    # Or just link them if we have specific fields.
                    # The models have relations_from/to but not explicit proof_id field on SemanticBlock except via relations

                    # Let's use SemanticRelation
                    # Subject: Proof, Predicate: PROVES, Object: Theorem
                    # Or Subject: Theorem, Predicate: PROVED_BY, Object: Proof
                    pass  # TODO: Implement relations logic based on specific requirements

        self.s.commit()

    def persist_batch(self, batch: Batch) -> dict:
        idmap: dict[str, int] = {}

        # Documents
        for d in batch.documents:
            self._upsert_document(d)
            self.s.flush()

        # TextBlocks
        tb_map: dict[str, int] = {}
        for t in batch.text_blocks:
            temp = t.pop("temp_id", None)
            obj = self._upsert_text_block(t)
            self.s.flush()
            if temp:
                tb_map[temp] = obj.id

        # SemanticBlocks
        sb_map: dict[str, int] = {}
        for sdata in batch.semantic_blocks:
            temp = sdata.pop("temp_id", None)
            for k in ("statement_id", "hypotheses_id", "conclusion_id"):
                if isinstance(sdata.get(k), str):
                    sdata[k] = sb_map.get(sdata[k])
            obj = self._insert_semantic_block(sdata)
            self.s.flush()
            if temp:
                sb_map[temp] = obj.id

        # Source links
        for link in batch.source_links:
            sb_id = link["semantic_block_id"]
            tb_id = link["text_block_id"]
            if isinstance(sb_id, str):
                sb_id = sb_map.get(sb_id)
            if isinstance(tb_id, str):
                tb_id = tb_map.get(tb_id)
            if not (sb_id and tb_id):
                continue
            exists = self.s.execute(
                select(models.SemanticSourceLink).where(
                    models.SemanticSourceLink.semantic_block_id == sb_id,
                    models.SemanticSourceLink.text_block_id == tb_id,
                    models.SemanticSourceLink.role == link.get("role"),
                    models.SemanticSourceLink.order_index == link.get("order_index"),
                )
            ).scalar_one_or_none()
            if not exists:
                self.s.add(
                    models.SemanticSourceLink(
                        semantic_block_id=sb_id,
                        text_block_id=tb_id,
                        role=link.get("role"),
                        order_index=link.get("order_index"),
                    )
                )
        self.s.flush()

        # Relations
        for rel in batch.relations:
            sbj = rel.get("subject_id")
            obj = rel.get("object_id")
            if isinstance(sbj, str):
                sbj = sb_map.get(sbj)
            if isinstance(obj, str):
                obj = sb_map.get(obj)
            if not (sbj and obj):
                continue
            exists = self.s.execute(
                select(models.SemanticRelation).where(
                    models.SemanticRelation.subject_id == sbj,
                    models.SemanticRelation.predicate == rel.get("predicate"),
                    models.SemanticRelation.object_id == obj,
                )
            ).scalar_one_or_none()
            if not exists:
                self.s.add(
                    models.SemanticRelation(
                        subject_id=sbj,
                        predicate=rel.get("predicate"),
                        object_id=obj,
                        note=rel.get("note"),
                    )
                )
        self.s.flush()

        idmap.update(tb_map)
        idmap.update(sb_map)
        return idmap
