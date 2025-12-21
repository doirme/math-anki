from __future__ import annotations

from enum import Enum


class BlockKind(str, Enum):
    """Types of semantic blocks."""

    definition = "definition"
    theorem = "theorem"
    lemma = "lemma"
    proposition = "proposition"
    corollary = "corollary"
    example = "example"
    exercise = "exercise"
    remark = "remark"
    note = "note"
    proof = "proof"
    demonstration = "demonstration"
    context = "context"  # Non-semantic context block
    statement = "statement"  # For sub-blocks
    hypotheses = "hypotheses"  # For sub-blocks
    conclusion = "conclusion"  # For sub-blocks
    formula = "formula"
    manual_review = (
        "manual_review"  # For blocks requiring user attention (e.g. too long)
    )
    unknown = "unknown"


class SourceRole(str, Enum):
    """Role of a text block in a semantic block."""

    full = "full"
    statement = "statement"
    hypotheses = "hypotheses"
    conclusion = "conclusion"
    proof = "proof"
    context = "context"
    name_occurrence = "name_occurrence"


class RelationPredicate(str, Enum):
    """Types of relationships between semantic blocks."""

    proves = "proves"
    states = "states"
    uses = "uses"
    refers_to = "refers_to"
    depends_on = "depends_on"
    is_part_of = "is_part_of"
    generalizes = "generalizes"
    specializes = "specializes"
    contradicts = "contradicts"
    equivalent_to = "equivalent_to"
    has_proof = "has_proof"
    uses_definition = "uses_definition"
    uses_theorem = "uses_theorem"
    example_of = "example_of"
    context_for = "context_for"


class MathObjectKind(str, Enum):
    """Types of mathematical objects."""

    notion = "notion"
    structure = "structure"
    set = "set"
    space = "space"
    function = "function"
    operator = "operator"
    number_system = "number_system"
    property = "property"
    other = "other"
