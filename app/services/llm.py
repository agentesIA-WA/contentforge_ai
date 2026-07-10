"""Lightweight LLM integration service.

This module provides a simple wrapper to call an LLM provider (OpenAI).
If `OPENAI_API_KEY` is not set in the environment, a simulated response
is returned to make local testing and CI deterministic.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import httpx

OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _simulate_response(prompt: str) -> Dict[str, Any]:
    return {
        "id": "simulated-1",
        "object": "chat.completion",
        "choices": [{"message": {"role": "assistant", "content": f"Simulated response for: {prompt}"}}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def generate_text(conteudo: str, modelo: str | None = None, parametros: dict | None = None) -> Dict[str, Any]:
    """Generate text for `conteudo` using the configured provider.

    - If `OPENAI_API_KEY` is not set, returns a simulated response.
    - Otherwise performs a synchronous HTTP request to the OpenAI Chat Completions API.
    """
    modelo = modelo or "gpt-3.5-turbo"
    parametros = parametros or {}

    if not OPENAI_API_KEY:
        return _simulate_response(conteudo)

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": modelo,
        "messages": [{"role": "user", "content": conteudo}],
        **({"temperature": parametros.get("temperature", 0.7)} if parametros else {}),
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(OPENAI_API_URL, json=body, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:  # pragma: no cover - network/error handling
        return {"error": str(exc)}
