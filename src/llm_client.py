"""Thin OpenAI client used by the rest of the codebase.

Pinned to openai==0.28 (legacy global API). The migration agent's job is to
move this to openai>=1.0 (`OpenAI()` client + `client.chat.completions.create`)
WITHOUT removing or breaking the @with_retries decorator on `complete`.

Streaming is opt-in only — default `stream=False`. Default-on caused INC-203.
"""
from __future__ import annotations

import os
from typing import Any, Iterator

import openai

from .retry_wrapper import with_retries


# Legacy v0.28 module-level config. Migration must convert this to a per-call
# OpenAI(api_key=...) client.
openai.api_key = os.environ.get("OPENAI_API_KEY", "test-key")

DEFAULT_MODEL = "gpt-3.5-turbo"


@with_retries
def complete(prompt: str, *, model: str = DEFAULT_MODEL, stream: bool = False) -> Any:
    """Single-prompt chat completion.

    LEGACY (v0.28) call shape:
        openai.ChatCompletion.create(model=..., messages=[...], stream=...)

    POST-MIGRATION (v1.x) target:
        client.chat.completions.create(model=..., messages=[...], stream=...)

    The @with_retries decorator MUST be preserved (team rule).
    """
    return openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=stream,
    )


@with_retries
def complete_stream(prompt: str, *, model: str = DEFAULT_MODEL) -> Iterator[Any]:
    """Explicit streaming entrypoint. Callers MUST drain the iterator (INC-203)."""
    return openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
