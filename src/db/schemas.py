
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .enums import BlockKind, SourceRole, RelationPredicate, MathObjectKind

class DocumentBase(BaseModel):
    title: Optional[str] = None
    source_path: Optional[str] = None
    source_hash: Optional[str] = None
    md_path: Optional[str] = None
    language: Optional[str] = "fr"
    subject_area: Optional[str] = "math"

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TextBlockBase(BaseModel):
    document_id: int
    raw_text: str
    block_index: Optional[int] = None
    page_number: Optional[int] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    heading_path: Optional[str] = None
    block_type_hint: Optional[str] = None
    normalized_text: Optional[str] = None
    content_hash: Optional[str] = None

class TextBlockCreate(TextBlockBase):
    temp_id: str | None = None

class TextBlockRead(TextBlockBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class MathObjectBase(BaseModel):
    name: str
    kind: MathObjectKind = MathObjectKind.other
    description: Optional[str] = None

class MathObjectCreate(MathObjectBase):
    pass

class MathObjectRead(MathObjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SemanticBlockBase(BaseModel):
    kind: BlockKind = BlockKind.unknown
    name: Optional[str] = None
    short_slug: Optional[str] = None
    summary: Optional[str] = None
    importance_score: Optional[float] = None
    math_object_id: Optional[int] = None
    statement_id: Optional[int] = None
    hypotheses_id: Optional[int] = None
    conclusion_id: Optional[int] = None

class SemanticBlockCreate(SemanticBlockBase):
    temp_id: str | None = None

class SemanticBlockRead(SemanticBlockBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SemanticSourceLinkBase(BaseModel):
    semantic_block_id: int | str
    text_block_id: int | str
    role: SourceRole = SourceRole.full
    order_index: Optional[int] = None

class SemanticSourceLinkCreate(SemanticSourceLinkBase):
    pass

class SemanticSourceLinkRead(SemanticSourceLinkBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SemanticRelationBase(BaseModel):
    subject_id: int | str
    predicate: RelationPredicate
    object_id: int | str
    note: Optional[str] = None

class SemanticRelationCreate(SemanticRelationBase):
    pass

class SemanticRelationRead(SemanticRelationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SemanticClusterBase(BaseModel):
    name: str
    description: Optional[str] = None

class SemanticClusterCreate(SemanticClusterBase):
    pass

class SemanticClusterRead(SemanticClusterBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SemanticClusterMembershipBase(BaseModel):
    cluster_id: int
    semantic_block_id: int
    weight: Optional[float] = None

class SemanticClusterMembershipCreate(SemanticClusterMembershipBase):
    pass

class SemanticClusterMembershipRead(SemanticClusterMembershipBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
