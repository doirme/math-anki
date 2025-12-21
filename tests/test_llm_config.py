from unittest.mock import patch

from core.llm_config import LLMTaskManager


def test_llm_config_defaults():
    """Verify default LLM configuration exists and is valid."""
    # Clear environment variables that might override defaults
    with patch.dict("os.environ", {}, clear=True):
        manager = LLMTaskManager()

        # Check that we have configs for all expected tasks
        for task in [
            "extraction",
            "block_validation",
            "block_linking",
            "normalization",
        ]:
            config = manager.get_config(task)
            assert config.backend is not None
            assert config.model is not None
            assert len(config.model) > 0


def test_llm_config_env_override(monkeypatch):
    """Verify that environment variables override defaults."""
    monkeypatch.setenv("LLM_TASK_EXTRACTION_BACKEND", "openai")
    monkeypatch.setenv("LLM_TASK_EXTRACTION_MODEL", "gpt-4o-mini")

    manager = LLMTaskManager()
    config = manager.get_config("extraction")

    assert config.backend == "openai"
    assert config.model == "gpt-4o-mini"
