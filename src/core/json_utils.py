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

    # Tentative directe
    try:
        return json.loads(blob)
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
    # On cherche les backslashes qui ne sont pas déjà suivis d'un caractère d'échappement JSON valide
    # Caractères valides: " \ / b f n r t u
    # On utilise une approche prudente : on double les backslashes s'ils ne sont pas suivis d'un des caractères ci-dessus
    # Mais attention aux doubles backslashes déjà présents.

    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        # Si ça échoue encore, on tente une réparation plus agressive des backslashes
        # On remplace les backslashes par des doubles backslashes, SAUF s'ils sont déjà doublés
        # ou s'ils précèdent une quote (qui doit rester \")
        def fix_slashes(match):
            s = match.group(0)
            if s == '\\"':
                return '\\"'  # Garder l'échappement de quote
            if s == "\\\\":
                return "\\\\"  # Garder le double backslash
            return "\\\\" + s[1:]  # Doubler le backslash

        repaired_slashes = re.sub(r"\\.", fix_slashes, repaired)
        # On doit aussi gérer les backslashes isolés en fin de mot ou avant ponctuation
        repaired_slashes = re.sub(r'\\([^\s"\\/bfnrtu])', r"\\\\\1", repaired)

        try:
            return json.loads(repaired_slashes)
        except Exception as e:
            # Dernier recours : si on a toujours une erreur d'escape, on peut essayer de supprimer les backslashes problématiques
            # ou lever l'erreur originale pour debug
            raise ValueError(
                f"Échec final du parsing JSON après réparations: {e}\nBlob: {blob[:200]}..."
            )
