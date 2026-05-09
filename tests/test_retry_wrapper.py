"""Tests for team-owned retry wrapper. The migration agent MUST keep all of
these passing.
"""
from __future__ import annotations

import pytest

from src.retry_wrapper import (
    BACKOFF_FACTOR,
    INITIAL_DELAY_S,
    MAX_ATTEMPTS,
    MAX_DELAY_S,
    RetriesExhausted,
    with_retries,
)


def test_succeeds_on_first_try():
    @with_retries
    def f():
        return 42

    assert f() == 42


def test_retries_until_success():
    counter = {"n": 0}

    @with_retries
    def flaky():
        counter["n"] += 1
        if counter["n"] < 3:
            raise RuntimeError("transient")
        return "ok"

    assert flaky() == "ok"
    assert counter["n"] == 3


def test_raises_after_max_attempts():
    @with_retries
    def always_fail():
        raise RuntimeError("nope")

    with pytest.raises(RetriesExhausted):
        always_fail()


def test_policy_constants_are_team_locked():
    """Team policy from ADR-12 is encoded as constants. Migration must NOT
    change these without DevOps sign-off."""
    assert MAX_ATTEMPTS == 5
    assert MAX_DELAY_S == 30.0
    assert BACKOFF_FACTOR == 2.0
    assert INITIAL_DELAY_S == 0.5
