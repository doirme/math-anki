from __future__ import annotations
import re

_FRONT_MATTER = re.compile(r"^---\s*\n[\s\S]*?\n---\s*\n", re.M)

def mmd_to_md(text: str) -> str:
    """
    Conversion douce MultiMarkdown -> Markdown:
    - retire un éventuel front-matter '--- ... ---' au début
    - normalise les fins de ligne
    - (on laisse le reste tel quel: c'est déjà compatible pour nos usages)
    """
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    txt = text.replace("\r\n", "\n").replace("\r", "\n")
    # retire un front-matter éventuel
    txt = _FRONT_MATTER.sub("", txt, count=1)
    # compactage d'espaces surnuméraires
    return txt
