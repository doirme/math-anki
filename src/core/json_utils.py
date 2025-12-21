import json
import re
from typing import Any

_JSON_BLOCK = re.compile(r"(\{[\s\S]*\}|\[[\s\S]*\])", re.M)


def extract_json_obj(text: str) -> Any:
    """
    Cherche le premier bloc JSON (objet ou liste). Tente json.loads, sinon petites réparations.
    Lève ValueError si rien d'exploitable.
    """
    m = _JSON_BLOCK.search(text)
    if not m:
        raise ValueError("Aucun objet ou liste JSON détecté")
    blob = m.group(0).strip()

    # Tentative directe avec strict=False pour autoriser les retours à la ligne littéraux dans les chaînes
    try:
        return json.loads(blob, strict=False)
    except Exception:
        pass

    # Réparations légères
    # 1. Quotes simples -> doubles sur clés/strings simples
    repaired = re.sub(r"([{\s,])'([^']+?)'\s*:", r'\1"\2":', blob)  # 'key':
    repaired = re.sub(r":\s*'([^']*)'", r': "\1"', repaired)  # : 'value'

    # 2. Booléens et None Python
    repaired = repaired.replace("True", "true").replace("False", "false")
    repaired = repaired.replace("None", "null")

    # 3. Échappement des backslashes LaTeX (le plus fréquent)
    try:
        return json.loads(repaired, strict=False)
    except json.JSONDecodeError:
        # Si ça échoue encore, on tente une réparation plus agressive des backslashes
        # On double TOUS les backslashes sauf s'ils sont déjà doublés ou s'ils échappent une quote

        def aggressive_fix(match):
            s = match.group(0)
            if s == '\\"':
                return '\\"'  # quote
            if s == "\\\\":
                return "\\\\"  # already double
            if s == "\\n":
                return "\\n"  # newline literal (\n)
            if s == "\\t":
                return "\\t"  # tab
            if s == "\\r":
                return "\\r"  # carriage return
            if s == "\\/":
                return "\\/"  # slash
            if s == "\\b":
                return "\\b"  # backspace
            if s == "\\f":
                return "\\f"  # formfeed
            if s == "\\u":
                return s  # unicode escape

            # Pour tout le reste (dont LaTeX!), on double le backslash
            return "\\\\" + s[1:]

        # On cherche \ suivi de n'importe quoi
        repaired_aggr = re.sub(r"\\.", aggressive_fix, repaired)

        # Gérer aussi les backslashes isolés (ex: en fin de ligne)
        repaired_aggr = re.sub(r'\\(?![\\nrt"/\bfu])', r"\\\\", repaired_aggr)

        try:
            return json.loads(repaired_aggr, strict=False)
        except Exception as e:
            raise ValueError(
                f"Échec parsing JSON (repaired_aggr): {e}\nDébut du blob: {blob[:500]}..."
            )
