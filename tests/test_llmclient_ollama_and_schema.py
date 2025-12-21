import json
from types import SimpleNamespace

from core.json_utils import extract_json_obj
from core.llm_client import LLMClient
from core.semantic_schemas import ExtractedTheorem as TheoremStruct


class DummyResp:
    def __init__(self, payload):
        self._payload = payload
    def raise_for_status(self):
        return
    def json(self):
        return self._payload

def test_ollama_client_generate_and_theorem_schema(monkeypatch):
    # --- mock requests.post pour simuler Ollama ---
    called = SimpleNamespace(count=0)

    def fake_post(url, json=None, timeout=60.0):
        called.count += 1
        # Simule une réponse Ollama avec un champ "response" contenant du JSON texte
        # on ignorerait réellement le prompt; on renvoie une réponse JSON valide
        model_json = {
            "name": "Théorème de Cantor",
            "hypotheses": [
                "Le corps \\mathbb{R} est muni de l'ordre usuel.",
                "On considère une suite réelle (a_n)_{n\\in\\mathbb{N}}."
            ],
            "conclusion": "Il existe x \\in \\mathbb{R} qui n'appartient pas à l'image de (a_n)_{n\\in\\mathbb{N}}.",
            "conclusion_text": "Il existe x \\in \\mathbb{R} qui n'appartient pas à l'image de (a_n)_{n\\in\\mathbb{N}}.",
            "has_proof": True
        }
        payload = {"response": json_dumps(model_json)}
        return DummyResp(payload)

    # helper pour dumps avec ensure_ascii=False pour garder le LaTeX propre
    def json_dumps(obj):
        return json.dumps(obj, ensure_ascii=False)

    monkeypatch.setattr("requests.post", fake_post)

    # --- appel client ---
    client = LLMClient(backend="ollama", model="llama3:8b", ollama_host="http://localhost:11434")
    out = client.generate("Peux-tu extraire le théorème ?")

    # --- extraction du JSON dans la réponse et validation pydantic ---
    data = extract_json_obj(out)
    obj = TheoremStruct(**data)

    assert obj.name == "Théorème de Cantor"
    assert obj.has_proof is True
    assert len(obj.hypotheses) >= 1
    assert "x \\in \\mathbb{R}" in obj.conclusion
