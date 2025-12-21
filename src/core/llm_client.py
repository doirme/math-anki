from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import requests

from .config import settings
from .llm_cache import LLMCache


class LLMClient:
    """
    Client LLM simple et interchangeable.
    backends:
      - 'ollama'     : API locale Ollama (http://localhost:11434)
      - 'openrouter' : API OpenRouter (OpenAI-compatible), via openai sdk
      - 'openai'     : API OpenAI officielle (optionnel si besoin)

    Env attendues (openrouter):
      - OPENROUTER_API_KEY       (obligatoire)
      - OPENROUTER_SITE          (optionnel, ex: https://ton-site)
      - OPENROUTER_TITLE         (optionnel, ex: "Math-Anki App")
    Env (openai):
      - OPENAI_API_KEY
    Env (ollama):
      - OLLAMA_HOST (defaut: http://localhost:11434)
    """

    def __init__(
        self,
        backend: str,
        model: str,
        *,
        ollama_host: Optional[str] = None,
        timeout: float = 120.0,
        max_retries: int = 2,
        usage_callback: Optional[callable] = None,
    ):
        self.backend = backend.lower().strip()
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.ollama_host = ollama_host or os.getenv(
            "OLLAMA_HOST", "http://localhost:11434"
        )
        self.usage_callback = usage_callback
        self.cache = (
            LLMCache(cache_dir=settings.llm_cache_dir)
            if settings.llm_use_cache
            else None
        )

    # ----------------- public -----------------
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
        task_name: str = "unknown",
        expect_json: bool = False,
    ) -> str:
        extra = extra or {}
        print(
            f"DEBUG: LLM generate task={task_name} backend={self.backend} model=[{self.model}]"
        )

        # Check cache
        if self.cache:
            # Include expect_json in cache key to distinguish between plain text and JSON mode
            cache_extra = extra.copy()
            if expect_json:
                cache_extra["_expect_json"] = True

            cached = self.cache.get(
                backend=self.backend,
                model=self.model,
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                extra=cache_extra,
            )
            if cached:
                print(f"DEBUG: LLM cache hit for task={task_name}")
                return cached

        if self.backend == "ollama":
            response = self._ollama_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                extra=extra,
                task_name=task_name,
            )
        elif self.backend == "openrouter":
            response = self._openrouter_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                extra=extra,
                task_name=task_name,
                expect_json=expect_json,
            )
        elif self.backend == "openai":
            response = self._openai_generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                extra=extra,
                task_name=task_name,
                expect_json=expect_json,
            )
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

        # Store in cache
        if self.cache and response:
            should_cache = True
            if expect_json:
                from .json_utils import extract_json_obj

                try:
                    extract_json_obj(response)
                except Exception:
                    print(
                        f"DEBUG: LLM response for task={task_name} is not valid JSON, skipping cache."
                    )
                    should_cache = False

            if should_cache:
                # Use same cache_extra for setting as used for getting
                cache_extra = extra.copy()
                if expect_json:
                    cache_extra["_expect_json"] = True

                self.cache.set(
                    backend=self.backend,
                    model=self.model,
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    extra=cache_extra,
                    response=response,
                )

        return response

    # ----------------- private: OLLAMA -----------------
    def _ollama_generate(
        self,
        prompt: str,
        *,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Dict[str, Any],
        task_name: str,
    ) -> str:
        url = f"{self.ollama_host.rstrip('/')}/api/generate"
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens
        # Merge extra options
        if extra:
            opts = payload.setdefault("options", {})
            for k, v in extra.items():
                if k in (
                    "temperature",
                    "top_p",
                    "top_k",
                    "stop",
                    "repeat_penalty",
                    "seed",
                    "num_predict",
                    "presence_penalty",
                    "frequency_penalty",
                ):
                    opts[k] = v
                else:
                    payload[k] = v

        last_err = None
        for _ in range(self.max_retries + 1):
            try:
                resp = requests.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()

                # Track usage (Ollama provides token counts)
                if self.usage_callback:
                    prompt_tokens = data.get("prompt_eval_count", 0)
                    completion_tokens = data.get("eval_count", 0)
                    total_tokens = prompt_tokens + completion_tokens
                    self.usage_callback(
                        task_name=task_name,
                        model=self.model,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens,
                        cost_usd=0.0,  # Local is free
                    )

                return data.get("response", "") or ""
            except Exception as e:
                last_err = e
                time.sleep(0.4)
        raise RuntimeError(f"Ollama generate failed: {last_err}")

    # ----------------- private: OPENROUTER (OpenAI-compatible) -----------------
    def _openrouter_generate(
        self,
        prompt: str,
        *,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Dict[str, Any],
        task_name: str,
        expect_json: bool = False,
    ) -> str:
        # OpenRouter parle l'API OpenAI. On utilise le SDK openai avec base_url custom.
        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError(
                "openai package is required for OpenRouter backend. pip install openai"
            ) from e

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENROUTER_API_KEY for OpenRouter backend")

        # Headers conseillés par OpenRouter (facultatifs mais utiles)
        default_headers = {}
        site = os.getenv("OPENROUTER_SITE")
        title = os.getenv("OPENROUTER_TITLE")
        if site:
            default_headers["HTTP-Referer"] = site
        if title:
            default_headers["X-Title"] = title

        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers=default_headers or None,
            timeout=self.timeout,
        )

        sys_msg = (
            system
            or "You are a helpful assistant. Output plain text or JSON as requested."
        )
        args: Dict[str, Any] = {
            "model": self.model,  # ex: "openrouter/anthropic/claude-3.5-sonnet"
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }
        if max_tokens is not None:
            args["max_tokens"] = max_tokens

        if expect_json:
            args["response_format"] = {"type": "json_object"}

        # Transférer quelques extras courants (top_p, stop, etc.)
        for k in ("top_p", "frequency_penalty", "presence_penalty", "stop"):
            if k in extra:
                args[k] = extra[k]

        # Ask for pricing info in response
        args["extra_body"] = {
            "include_reasoning": True
        }  # Sometimes needed for extra fields, but mainly we rely on response object

        last_err = None
        for _ in range(self.max_retries + 1):
            try:
                resp = client.chat.completions.create(**args)
                content = resp.choices[0].message.content if resp.choices else ""

                # Track usage
                if self.usage_callback:
                    usage = resp.usage
                    prompt_tokens = usage.prompt_tokens if usage else 0
                    completion_tokens = usage.completion_tokens if usage else 0
                    total_tokens = usage.total_tokens if usage else 0

                    cost = 0.0
                    # OpenRouter returns pricing in 'model_extra' (pydantic v2) or dict
                    # Structure: resp.model_extra['pricing'] = { 'prompt': '...', 'completion': '...', ... }
                    try:
                        # Access extra fields safely
                        extra_fields = getattr(resp, "model_extra", {}) or {}
                        pricing = extra_fields.get("pricing")

                        if pricing:
                            # Pricing values are strings representing USD per token/unit
                            prompt_rate = float(pricing.get("prompt", "0"))
                            completion_rate = float(pricing.get("completion", "0"))
                            request_rate = float(pricing.get("request", "0"))

                            cost = (
                                (prompt_tokens * prompt_rate)
                                + (completion_tokens * completion_rate)
                                + request_rate
                            )
                    except Exception:
                        # Fallback or log error (silent fail for cost calculation to avoid breaking flow)
                        pass

                    self.usage_callback(
                        task_name=task_name,
                        model=self.model,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens,
                        cost_usd=cost,
                    )

                return content or ""
            except Exception as e:
                last_err = e
                time.sleep(0.5)
        raise RuntimeError(f"OpenRouter generate failed: {last_err}")

    # ----------------- private: OPENAI (optionnel) -----------------
    def _openai_generate(
        self,
        prompt: str,
        *,
        system: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        extra: Dict[str, Any],
        task_name: str,
        expect_json: bool = False,
    ) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=self.timeout)

        sys_msg = (
            system
            or "You are a helpful assistant. Output plain text or JSON as requested."
        )
        args: Dict[str, Any] = {
            "model": self.model,  # ex: "gpt-4o-mini", "gpt-4.1", etc.
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }
        if max_tokens is not None:
            args["max_tokens"] = max_tokens

        if expect_json:
            args["response_format"] = {"type": "json_object"}

        for k in ("top_p", "frequency_penalty", "presence_penalty", "stop"):
            if k in extra:
                args[k] = extra[k]

        last_err = None
        for _ in range(self.max_retries + 1):
            try:
                resp = client.chat.completions.create(**args)

                if self.usage_callback:
                    usage = resp.usage
                    self.usage_callback(
                        task_name=task_name,
                        model=self.model,
                        prompt_tokens=usage.prompt_tokens,
                        completion_tokens=usage.completion_tokens,
                        total_tokens=usage.total_tokens,
                        cost_usd=0.0,  # OpenAI doesn't return cost directly
                    )

                return resp.choices[0].message.content or ""
            except Exception as e:
                last_err = e
                time.sleep(0.5)
        raise RuntimeError(f"OpenAI generate failed: {last_err}")
