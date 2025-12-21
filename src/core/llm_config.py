"""
LLM Configuration per Task

Allows different models for different semantic analysis tasks.
Supports OpenRouter and other backends via LLMClient.
Configurations are loaded from environment variables with defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .config import settings
from .llm_client import LLMClient


@dataclass
class LLMTaskConfig:
    """Configuration for a specific LLM task."""

    backend: str  # "openrouter", "ollama", "openai"
    model: str  # Model identifier
    temperature: float = 0.0
    max_tokens: Optional[int] = None


class LLMTaskManager:
    """
    Manages LLM clients for different semantic analysis tasks.

    Tasks:
    - block_validation: Check if blocks are self-contained
    - block_linking: Detect relationships between blocks
    - extraction: Extract structured data (definitions, theorems, etc.)
    - normalization: Normalize names and extract domain tags
    - embedding_context: Generate context for embeddings (optional)
    """

    # Default models (can be overridden via env vars)
    # Using free/open-source models by default
    DEFAULT_MODELS = {
        "block_validation": {
            "backend": "openrouter",
            "model": "mistralai/mistral-7b-instruct:free",  # Verified ID
            "temperature": 0.0,
        },
        "block_linking": {
            "backend": "openrouter",
            "model": "mistralai/mistral-7b-instruct:free",
            "temperature": 0.0,
        },
        "extraction": {
            "backend": "openrouter",
            "model": "xiaomi/mimo-v2-flash:free",
            "temperature": 0.0,
        },
        "normalization": {
            "backend": "openrouter",
            "model": "mistralai/mistral-7b-instruct:free",
            "temperature": 0.0,
        },
    }

    def __init__(self):
        self._clients: Dict[str, LLMClient] = {}
        self._configs: Dict[str, LLMTaskConfig] = {}
        self._load_configs()

    def _load_configs(self):
        """Load configurations from env vars or use defaults."""
        for task_name, default in self.DEFAULT_MODELS.items():
            # Env var format: LLM_TASK_{TASK_NAME}_BACKEND, LLM_TASK_{TASK_NAME}_MODEL

            backend = settings.get_task_config_value(
                task_name, "BACKEND", default["backend"]
            )
            model = settings.get_task_config_value(task_name, "MODEL", default["model"])
            if model:
                # Strip whitespace and any accidental trailing dots
                model = model.strip().rstrip(".")

            temp_str = settings.get_task_config_value(task_name, "TEMPERATURE")
            temperature = (
                float(temp_str)
                if temp_str is not None
                else default.get("temperature", 0.0)
            )

            max_tokens_str = settings.get_task_config_value(task_name, "MAX_TOKENS")
            max_tokens = int(max_tokens_str) if max_tokens_str else None

            config = LLMTaskConfig(
                backend=backend,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            self._configs[task_name] = config

    def get_client(self, task_name: str) -> LLMClient:
        """
        Get or create LLM client for a specific task.

        Args:
            task_name: One of "block_validation", "block_linking", "extraction", "normalization"

        Returns:
            LLMClient configured for the task
        """
        if task_name not in self._configs:
            raise ValueError(
                f"Unknown task: {task_name}. Available: {list(self.DEFAULT_MODELS.keys())}"
            )

        if task_name not in self._clients:
            config = self._configs[task_name]
            self._clients[task_name] = LLMClient(
                backend=config.backend,
                model=config.model,
            )

        return self._clients[task_name]

    def get_config(self, task_name: str) -> LLMTaskConfig:
        """Get configuration for a task."""
        if task_name not in self._configs:
            raise ValueError(f"Unknown task: {task_name}")
        return self._configs[task_name]

    def generate(
        self, task_name: str, prompt: str, *, system: Optional[str] = None, **kwargs
    ) -> str:
        """
        Generate text using the appropriate model for a task.
        """
        client = self.get_client(task_name)
        config = self.get_config(task_name)

        # Use config defaults, allow override via kwargs
        temperature = kwargs.get("temperature", config.temperature)
        max_tokens = kwargs.get("max_tokens", config.max_tokens)

        # Allow overriding the task name used for logging
        log_task_name = kwargs.get("display_name", task_name)
        expect_json = kwargs.get("expect_json", False)

        return client.generate(
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            task_name=log_task_name,
            expect_json=expect_json,
            extra={
                k: v
                for k, v in kwargs.items()
                if k not in ("temperature", "max_tokens", "display_name", "expect_json")
            },
        )


# Global instance
_llm_task_manager: Optional[LLMTaskManager] = None


def get_llm_task_manager() -> LLMTaskManager:
    """Get global LLM task manager instance."""
    global _llm_task_manager
    if _llm_task_manager is None:
        _llm_task_manager = LLMTaskManager()
    return _llm_task_manager
