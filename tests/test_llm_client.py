"""Tests for the LLM client. These exercise both that the OpenAI SDK is
called correctly AND that the team's @with_retries decorator is still in
place after migration.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from src import llm_client
from src.retry_wrapper import RetriesExhausted


def test_complete_calls_chatcompletion(monkeypatch):
    """Sanity check: complete() routes through the OpenAI SDK at all."""
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return {"choices": [{"message": {"content": "hi"}}]}

    # v0.28: patch openai.ChatCompletion.create
    # Migration agent will need to update this test target too.
    monkeypatch.setattr(llm_client.openai.ChatCompletion, "create", fake_create)

    result = llm_client.complete("hello")
    assert "choices" in result
    assert captured["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["model"] == llm_client.DEFAULT_MODEL


def test_streaming_is_opt_in(monkeypatch):
    """Default stream=False per team policy (INC-203)."""
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return {}

    monkeypatch.setattr(llm_client.openai.ChatCompletion, "create", fake_create)
    llm_client.complete("hi")
    assert captured["stream"] is False


def test_explicit_streaming_path(monkeypatch):
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return iter([])

    monkeypatch.setattr(llm_client.openai.ChatCompletion, "create", fake_create)
    llm_client.complete_stream("hi")
    assert captured["stream"] is True


def test_retry_wrapper_is_present():
    """Team rule: complete() MUST be wrapped by @with_retries.

    The migration agent needs to keep this true after porting to openai>=1.0.
    Detection: the wrapped function has __wrapped__ pointing back to the original
    AND it's the with_retries decorator (which raises RetriesExhausted on failure).
    """
    assert hasattr(llm_client.complete, "__wrapped__"), (
        "complete() lost its @with_retries decorator! See PR #347 / ADR-12."
    )
    assert hasattr(llm_client.complete_stream, "__wrapped__")


def test_complete_raises_retries_exhausted_after_failures(monkeypatch):
    """Verifies the retry path actually retries (rather than only being labeled)."""
    calls = {"n": 0}

    def fake_create(**kwargs):
        calls["n"] += 1
        raise RuntimeError("simulated 500")

    monkeypatch.setattr(llm_client.openai.ChatCompletion, "create", fake_create)
    with pytest.raises(RetriesExhausted):
        llm_client.complete("x")
    # MAX_ATTEMPTS = 5 (team policy)
    assert calls["n"] == 5
