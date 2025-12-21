import hashlib
import json
import pathlib
from typing import Any, Dict, Optional


class LLMCache:
    """
    Simple disk-based cache for LLM responses.
    """

    def __init__(self, cache_dir: str = "./data/llm_cache"):
        self.cache_dir = pathlib.Path(cache_dir).expanduser().resolve()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_hash(
        self,
        backend: str,
        model: str,
        prompt: str,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Optional[Dict[str, Any]],
    ) -> str:
        """Generate a unique hash for the request parameters."""
        key_data = {
            "backend": backend,
            "model": model,
            "prompt": prompt,
            "system": system,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "extra": extra,
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

    def get(
        self,
        backend: str,
        model: str,
        prompt: str,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Retrieve a cached response if it exists."""
        h = self._get_hash(
            backend, model, prompt, system, temperature, max_tokens, extra
        )
        cache_file = self.cache_dir / f"{h}.txt"
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")
        return None

    def set(
        self,
        backend: str,
        model: str,
        prompt: str,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Optional[Dict[str, Any]],
        response: str,
    ):
        """Store a response in the cache."""
        h = self._get_hash(
            backend, model, prompt, system, temperature, max_tokens, extra
        )
        cache_file = self.cache_dir / f"{h}.txt"
        cache_file.write_text(response, encoding="utf-8")

        # Also save a .json file with metadata for debugging/transparency
        meta_file = self.cache_dir / f"{h}.json"
        meta_data = {
            "backend": backend,
            "model": model,
            "system": system,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "extra": extra,
        }
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
