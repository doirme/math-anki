from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from core.enums import BlockKind, MathObjectKind, RelationPredicate, SourceRole
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class LLMUsage(Base):
    __tablename__ = "llm_usage"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    task_name: Mapped[str] = mapped_column(String, index=True)
    model: Mapped[str] = mapped_column(String, index=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    __table_args__ = (Index("idx_llm_usage_task", "task_name"),)


class SemanticBlockTag(Base):
    __tablename__ = "semantic_block_tag"
    semantic_block_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )


class Document(Base):
    __tablename__ = "document"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, index=True)
    source_path: Mapped[Optional[str]] = mapped_column(String, index=True)
    source_hash: Mapped[Optional[str]] = mapped_column(String, index=True)
    md_path: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    language: Mapped[Optional[str]] = mapped_column(String, default="fr")
    subject_area: Mapped[Optional[str]] = mapped_column(String, default="math")
    text_blocks: Mapped[List["TextBlock"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )
    __table_args__ = (
        Index("idx_document_source_hash", "source_hash"),
        Index("idx_document_title", "title"),
    )


class TextBlock(Base):
    __tablename__ = "text_block"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("document.id", ondelete="CASCADE"), index=True
    )
    block_index: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    start_char: Mapped[Optional[int]] = mapped_column(Integer)
    end_char: Mapped[Optional[int]] = mapped_column(Integer)
    heading_path: Mapped[Optional[str]] = mapped_column(String)
    block_type_hint: Mapped[Optional[str]] = mapped_column(String)
    raw_text: Mapped[str] = mapped_column(Text)
    normalized_text: Mapped[Optional[str]] = mapped_column(Text)
    content_hash: Mapped[Optional[str]] = mapped_column(String, index=True)
    document: Mapped["Document"] = relationship(back_populates="text_blocks")
    sources_for_semantic: Mapped[List["SemanticSourceLink"]] = relationship(
        back_populates="text_block", cascade="all, delete-orphan"
    )
    outgoing_refs: Mapped[List["CrossRef"]] = relationship(
        back_populates="from_block",
        foreign_keys="CrossRef.from_text_block_id",
        cascade="all, delete-orphan",
    )
    incoming_refs: Mapped[List["CrossRef"]] = relationship(
        back_populates="to_block",
        foreign_keys="CrossRef.to_text_block_id",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        Index("idx_text_block_document", "document_id", "block_index"),
        Index("idx_text_block_page", "page_number"),
        Index("idx_text_block_hash", "content_hash"),
    )


class MathObject(Base):
    __tablename__ = "math_object"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    kind: Mapped[MathObjectKind] = mapped_column(
        SAEnum(MathObjectKind), default=MathObjectKind.other, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text)
    aliases: Mapped[List["MathObjectAlias"]] = relationship(
        back_populates="math_object", cascade="all, delete-orphan"
    )
    semantic_blocks: Mapped[List["SemanticBlock"]] = relationship(
        back_populates="math_object"
    )
    __table_args__ = (Index("uq_math_object_name", "name", unique=True),)


class MathObjectAlias(Base):
    __tablename__ = "math_object_alias"
    id: Mapped[int] = mapped_column(primary_key=True)
    math_object_id: Mapped[int] = mapped_column(
        ForeignKey("math_object.id", ondelete="CASCADE"), index=True
    )
    alias: Mapped[str] = mapped_column(String, index=True)
    math_object: Mapped["MathObject"] = relationship(back_populates="aliases")
    __table_args__ = (
        Index("uq_math_object_alias", "math_object_id", "alias", unique=True),
    )


class SemanticBlock(Base):
    __tablename__ = "semantic_block"
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[BlockKind] = mapped_column(
        SAEnum(BlockKind), default=BlockKind.unknown, index=True
    )
    name: Mapped[Optional[str]] = mapped_column(String, index=True)
    short_slug: Mapped[Optional[str]] = mapped_column(String, index=True)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    importance_score: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    math_object_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("math_object.id", ondelete="SET NULL"), index=True
    )
    statement_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="SET NULL")
    )
    hypotheses_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="SET NULL")
    )
    conclusion_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="SET NULL")
    )
    math_object: Mapped[Optional["MathObject"]] = relationship(
        back_populates="semantic_blocks"
    )
    statement: Mapped[Optional["SemanticBlock"]] = relationship(
        "SemanticBlock",
        foreign_keys=[statement_id],
        remote_side="SemanticBlock.id",
        uselist=False,
        post_update=True,
    )
    hypotheses: Mapped[Optional["SemanticBlock"]] = relationship(
        "SemanticBlock",
        foreign_keys=[hypotheses_id],
        remote_side="SemanticBlock.id",
        uselist=False,
        post_update=True,
    )
    conclusion: Mapped[Optional["SemanticBlock"]] = relationship(
        "SemanticBlock",
        foreign_keys=[conclusion_id],
        remote_side="SemanticBlock.id",
        uselist=False,
        post_update=True,
    )
    sources: Mapped[List["SemanticSourceLink"]] = relationship(
        back_populates="semantic_block", cascade="all, delete-orphan"
    )
    relations_from: Mapped[List["SemanticRelation"]] = relationship(
        back_populates="subject",
        foreign_keys="SemanticRelation.subject_id",
        cascade="all, delete-orphan",
    )
    relations_to: Mapped[List["SemanticRelation"]] = relationship(
        back_populates="object",
        foreign_keys="SemanticRelation.object_id",
        cascade="all, delete-orphan",
    )
    cluster_memberships: Mapped[List["SemanticClusterMembership"]] = relationship(
        back_populates="semantic_block", cascade="all, delete-orphan"
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary="semantic_block_tag", back_populates="semantic_blocks"
    )
    __table_args__ = (
        Index("idx_semantic_block_kind", "kind"),
        Index("idx_semantic_block_name", "name"),
        Index("idx_semantic_block_importance", "importance_score"),
    )


class SemanticSourceLink(Base):
    __tablename__ = "semantic_source_link"
    id: Mapped[int] = mapped_column(primary_key=True)
    semantic_block_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="CASCADE"), index=True
    )
    text_block_id: Mapped[int] = mapped_column(
        ForeignKey("text_block.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[SourceRole] = mapped_column(
        SAEnum(SourceRole), default=SourceRole.full, index=True
    )
    order_index: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    semantic_block: Mapped["SemanticBlock"] = relationship(back_populates="sources")
    text_block: Mapped["TextBlock"] = relationship(
        back_populates="sources_for_semantic"
    )
    __table_args__ = (
        Index("idx_source_link_semantic", "semantic_block_id", "role", "order_index"),
        Index("idx_source_link_text", "text_block_id"),
    )


class SemanticRelation(Base):
    __tablename__ = "semantic_relation"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="CASCADE"), index=True
    )
    predicate: Mapped[RelationPredicate] = mapped_column(
        SAEnum(RelationPredicate), index=True
    )
    object_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="CASCADE"), index=True
    )
    note: Mapped[Optional[str]] = mapped_column(Text)
    subject: Mapped["SemanticBlock"] = relationship(
        back_populates="relations_from", foreign_keys=[subject_id]
    )
    object: Mapped["SemanticBlock"] = relationship(
        back_populates="relations_to", foreign_keys=[object_id]
    )
    __table_args__ = (
        Index("idx_relation_triple", "subject_id", "predicate", "object_id"),
    )


class CrossRef(Base):
    __tablename__ = "cross_ref"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_text_block_id: Mapped[int] = mapped_column(
        ForeignKey("text_block.id", ondelete="CASCADE"), index=True
    )
    to_text_block_id: Mapped[int] = mapped_column(
        ForeignKey("text_block.id", ondelete="CASCADE"), index=True
    )
    ref_text: Mapped[Optional[str]] = mapped_column(Text)
    ref_type: Mapped[Optional[str]] = mapped_column(String, default="internal")
    from_block: Mapped["TextBlock"] = relationship(
        back_populates="outgoing_refs", foreign_keys=[from_text_block_id]
    )
    to_block: Mapped["TextBlock"] = relationship(
        back_populates="incoming_refs", foreign_keys=[to_text_block_id]
    )
    __table_args__ = (
        Index("idx_cross_ref_from", "from_text_block_id"),
        Index("idx_cross_ref_to", "to_text_block_id"),
    )


class SemanticCluster(Base):
    __tablename__ = "semantic_cluster"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    memberships: Mapped[List["SemanticClusterMembership"]] = relationship(
        back_populates="cluster", cascade="all, delete-orphan"
    )
    __table_args__ = (Index("uq_cluster_name", "name", unique=True),)


class SemanticClusterMembership(Base):
    __tablename__ = "semantic_cluster_membership"
    id: Mapped[int] = mapped_column(primary_key=True)
    cluster_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_cluster.id", ondelete="CASCADE"), index=True
    )
    semantic_block_id: Mapped[int] = mapped_column(
        ForeignKey("semantic_block.id", ondelete="CASCADE"), index=True
    )
    weight: Mapped[Optional[float]] = mapped_column(Float)
    cluster: Mapped["SemanticCluster"] = relationship(back_populates="memberships")
    semantic_block: Mapped["SemanticBlock"] = relationship(
        back_populates="cluster_memberships"
    )
    __table_args__ = (
        Index("uq_cluster_membership", "cluster_id", "semantic_block_id", unique=True),
    )


class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    semantic_blocks: Mapped[List["SemanticBlock"]] = relationship(
        secondary="semantic_block_tag", back_populates="tags"
    )
    __table_args__ = (Index("uq_tag_name", "name", unique=True),)
