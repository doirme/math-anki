import os
import pathlib

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    llm_backend: str = os.getenv("LLM_BACKEND", "ollama")
    llm_model: str = os.getenv("LLM_MODEL", "llama3:8b")
    db_url: str = os.getenv("DB_URL", "sqlite:///./data/math_anki.db")
    # --- nouveau : activer la réparation LaTeX par LLM dans fix_math ---
    fixmath_use_llm: bool = os.getenv("FIXMATH_USE_LLM", "false").lower() in (
        "1",
        "true",
        "yes",
    )
    # Chunked extraction settings
    chunk_size_chars: int = int(os.getenv("CHUNK_SIZE_CHARS", "40000"))
    chunk_overlap_chars: int = int(os.getenv("CHUNK_OVERLAP_CHARS", "5000"))
    dedupe_similarity_threshold: float = float(
        os.getenv("DEDUPE_SIMILARITY_THRESHOLD", "0.9")
    )
    dedupe_offset_overlap_threshold: float = float(
        os.getenv("DEDUPE_OFFSET_OVERLAP_THRESHOLD", "0.7")
    )

    # --- Cache & Marker API ---
    marker_api_key: str | None = os.getenv("MARKER_API_KEY")  # Datalab Marker API key
    md_cache_dir: str | None = os.getenv("MD_CACHE_DIR")  # ex: ./data/library
    md_cache_strict_hash: bool = os.getenv("MD_CACHE_STRICT_HASH", "true").lower() in (
        "1",
        "true",
        "yes",
    )

    # --- LLM Cache ---
    llm_cache_dir: str = os.getenv("LLM_CACHE_DIR", "./data/llm_cache")
    llm_use_cache: bool = os.getenv("LLM_USE_CACHE", "true").lower() in (
        "1",
        "true",
        "yes",
    )
    llm_batch_size: int = int(os.getenv("LLM_BATCH_SIZE", "3"))

    # --- Language settings ---
    output_language: str = os.getenv(
        "OUTPUT_LANGUAGE", "auto"
    )  # "auto", "fr", "en", etc.

    def get_cache_dir(self) -> pathlib.Path | None:
        if not self.md_cache_dir:
            return None
        p = pathlib.Path(self.md_cache_dir).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_task_config_value(
        self, task_name: str, key_suffix: str, default: any = None
    ) -> any:
        """
        Get configuration value for a specific task from environment variables.

        Args:
            task_name: Name of the task (e.g., "extraction")
            key_suffix: Suffix of the key (e.g., "BACKEND", "MODEL")
            default: Default value if not found

        Returns:
            Value from env var LLM_TASK_{TASK}_{SUFFIX} or default
        """
        env_key = f"LLM_TASK_{task_name.upper()}_{key_suffix.upper()}"
        return os.getenv(env_key, default)


settings = Settings()
