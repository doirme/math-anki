
from __future__ import annotations
from enum import Enum


class BlockKind(str, Enum):
    definition = "definition"; theorem = "theorem"; lemma = "lemma"; proposition = "proposition"; corollary = "corollary"
    example = "example"; exercise = "exercise"; remark = "remark"; note = "note"
    statement = "statement"; hypotheses = "hypotheses"; conclusion = "conclusion"; proof = "proof"; unknown = "unknown"


class SourceRole(str, Enum):
    full = "full"; statement = "statement"; hypotheses = "hypotheses"; conclusion = "conclusion"; proof = "proof"; context = "context"; name_occurrence = "name_occurrence"


class RelationPredicate(str, Enum):
    proves = "proves"; states = "states"; uses = "uses"; refers_to = "refers_to"; depends_on = "depends_on"; is_part_of = "is_part_of"; generalizes = "generalizes"; 
    specializes = "specializes"; contradicts = "contradicts"; equivalent_to = "equivalent_to"


class MathObjectKind(str, Enum):
    notion = "notion"; structure = "structure"; set = "set"; space = "space"; function = "function"; operator = "operator"; number_system = "number_system"; 
    property = "property"; other = "other"
