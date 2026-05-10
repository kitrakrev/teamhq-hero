"""Streaming inference adapter for the chat UI.

First step toward streaming completions: wraps `llm_client.complete_stream`
and yields plain text deltas. Retry policy stays in `llm_client` (ADR-12,
INC-203 — do not re-wrap with a second retry layer here).

Caller MUST drain the iterator (INC-203).
"""
from __future__ import annotations

from typing import Iterator

from ..llm_client import DEFAULT_MODEL, complete_stream


def stream_text_deltas(prompt: str, *, model: str = DEFAULT_MODEL) -> Iterator[str]:
    for chunk in complete_stream(prompt, model=model):
        choices = chunk.get("choices") if isinstance(chunk, dict) else getattr(chunk, "choices", None)
        if not choices:
            continue
        delta = choices[0].get("delta") if isinstance(choices[0], dict) else getattr(choices[0], "delta", {})
        content = delta.get("content") if isinstance(delta, dict) else getattr(delta, "content", None)
        if content:
            yield content
