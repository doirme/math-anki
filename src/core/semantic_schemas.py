"""
Enhanced schemas for semantic analysis pipeline.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .enums import BlockKind


class RawBlock(BaseModel):
    """Raw block from initial segmentation."""

    type: str
    text: str
    page: int = 0
    is_toc: bool = False
    start_line: int = 0
    end_line: int = 0


class ValidatedBlock(BaseModel):
    """Block after LLM validation and merging."""

    id: str  # Unique identifier
    kind: BlockKind
    raw_text: str  # Original text
    validated_text: str  # After validation/merging
    page: int = 0
    start_line: int = 0
    end_line: int = 0

    # Normalization (populated during validation)
    normalized_text: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    # Context references
    preceding_blocks: List[str] = Field(default_factory=list)  # IDs of preceding blocks
    following_blocks: List[str] = Field(default_factory=list)  # IDs of following blocks

    # Self-containedness
    is_self_contained: bool = False
    missing_context: List[str] = Field(default_factory=list)  # What's missing
    validation_errors: List[str] = Field(
        default_factory=list
    )  # Errors found during validation (e.g. "Block too long")

    # Relationships (will be populated by linker)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)

    # Rich metadata for semantic extraction (optional)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LinkedBlock(BaseModel):
    """Block with relationships established."""

    block: ValidatedBlock
    linked_to: List[Dict[str, Any]] = Field(
        default_factory=list
    )  # [{block_id, relation, ...}]
    context_blocks: List[str] = Field(
        default_factory=list
    )  # IDs of attached context blocks


class ExtractedDefinition(BaseModel):
    """Extracted definition structure."""

    term: Optional[str] = None
    normalized_term: Optional[str] = None  # Normalized name (e.g., "Sylow")
    statement: str
    domain_tags: List[str] = Field(default_factory=list)  # ["finite groups", "algebra"]
    characteristics: List[str] = Field(
        default_factory=list
    )  # ["finite", "prime order"]

    # If multiple definitions in one block
    is_multiple: bool = False
    definitions: List[Dict[str, str]] = Field(
        default_factory=list
    )  # [{term, statement}]


class ExtractedTheorem(BaseModel):
    """Extracted theorem structure."""

    name: Optional[str] = None
    normalized_name: Optional[str] = None  # e.g., "Cayley-Hamilton"
    hypotheses: List[str] = Field(default_factory=list)
    conclusion: str
    equivalent_statements: List[str] = Field(
        default_factory=list
    )  # For equivalences (i <=> ii <=> iii)
    has_proof: bool = False
    proof_block_id: Optional[str] = None  # Link to proof block

    domain_tags: List[str] = Field(default_factory=list)
    characteristics: List[str] = Field(default_factory=list)

    # Structured parts
    hypothesis_text: Optional[str] = None  # Full hypothesis text
    conclusion_text: str  # Full conclusion text


class ExtractedFormula(BaseModel):
    """Extracted formula structure."""

    name: Optional[str] = None
    normalized_name: Optional[str] = None
    statement: str  # The formula itself (LaTeX)
    domain_tags: List[str] = Field(default_factory=list)
    characteristics: List[str] = Field(default_factory=list)


class ExtractedProof(BaseModel):
    """Extracted proof structure."""

    theorem_block_id: Optional[str] = None  # Link to theorem
    steps: List[str] = Field(default_factory=list)
    uses_definitions: List[str] = Field(default_factory=list)  # Definition IDs used
    uses_theorems: List[str] = Field(default_factory=list)  # Theorem IDs used


class ExtractedExercise(BaseModel):
    """Extracted exercise structure."""

    questions: List[str] = Field(default_factory=list)
    solution_steps: List[str] = Field(default_factory=list)
    solved: bool = False
    uses_concepts: List[str] = Field(default_factory=list)  # Definition/theorem IDs


class SemanticBlockIndex(BaseModel):
    """Index for database comparison."""

    normalized_name: Optional[str] = None
    domain_tags: List[str] = Field(default_factory=list)
    characteristics: List[str] = Field(default_factory=list)
    embedding_text: str  # Text to generate embedding from
    key_phrases: List[str] = Field(
        default_factory=list
    )  # Important phrases for matching


class SelfContainedCheck(BaseModel):
    """Result of self-containedness check."""

    is_self_contained: bool
    missing: List[str] = Field(default_factory=list)
    needs_preceding: bool = False
    needs_following: bool = False
    suggested_merge_with: List[str] = Field(
        default_factory=list
    )  # Block IDs to merge with

    # Normalization
    normalized_text: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
