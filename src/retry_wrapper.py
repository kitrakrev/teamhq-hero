"""Team-owned retry wrapper for OpenAI client calls.

OWNER: Sarah (Backend) — see CODEOWNERS.

DO NOT REMOVE OR REPLACE during SDK migrations. PR #347 (Aug 2024) reverted
@field_validator and confirmed this wrapper as the canonical retry policy.
INC-203 was the trigger.

Policy:
  - exponential backoff
  - cap = 30s
  - 5 attempts max
  - DevOps must sign off on any change to these numbers
"""
from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")

MAX_ATTEMPTS = 5
INITIAL_DELAY_S = 0.5
MAX_DELAY_S = 30.0
BACKOFF_FACTOR = 2.0


class RetriesExhausted(Exception):
    """Raised after MAX_ATTEMPTS retries fail."""


def with_retries(fn: Callable[..., T]) -> Callable[..., T]:
    """Decorator that retries `fn` with exponential backoff capped at MAX_DELAY_S.

    Conforms to team policy from #backend Slack and ADR-12.
    """

    @functools.wraps(fn)
    def wrapped(*args: Any, **kwargs: Any) -> T:
        delay = INITIAL_DELAY_S
        last_exc: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:  # noqa: BLE001 — wrapper is intentionally broad
                last_exc = e
                if attempt == MAX_ATTEMPTS:
                    break
                time.sleep(min(delay, MAX_DELAY_S))
                delay *= BACKOFF_FACTOR
        raise RetriesExhausted(
            f"{fn.__name__} failed after {MAX_ATTEMPTS} attempts"
        ) from last_exc

    return wrapped
