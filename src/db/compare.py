
from __future__ import annotations


def equal_math_objects(a, b) -> bool:
    na = (getattr(a, "name", None) or "").strip().lower()
    nb = (getattr(b, "name", None) or "").strip().lower()
    if na and nb:
        return na == nb
    da = (getattr(a, "description", None) or "").strip().lower()
    db = (getattr(b, "description", None) or "").strip().lower()
    return bool(da) and (da == db)


def equal_semantic_blocks_by_name_or_text(a, b) -> bool:
    na = (getattr(a, "name", None) or "").strip().lower()
    nb = (getattr(b, "name", None) or "").strip().lower()
    if na and nb:
        return na == nb
    sa = (getattr(a, "summary", None) or "").strip().lower()
    sb = (getattr(b, "summary", None) or "").strip().lower()
    return bool(sa) and (sa == sb)
