"""SSE endpoint scaffolding for streaming chat completions.

Framework-agnostic: yields encoded `text/event-stream` byte frames so this
can plug into Flask `Response`, FastAPI `StreamingResponse`, or raw WSGI
without committing to a web framework in this PR.

Paying-customer gating is a TODO — entitlement check will live in the
HTTP handler that imports `iter_sse_frames`, not here.
"""
from __future__ import annotations

from typing import Iterator

from ..ml.inference import stream_text_deltas


def _format_event(data: str, *, event: str | None = None) -> bytes:
    lines = []
    if event:
        lines.append(f"event: {event}")
    for ln in data.splitlines() or [""]:
        lines.append(f"data: {ln}")
    return ("\n".join(lines) + "\n\n").encode("utf-8")


def iter_sse_frames(prompt: str) -> Iterator[bytes]:
    """Yield SSE-encoded frames for a single chat prompt.

    Caller MUST iterate to completion (INC-203).
    """
    try:
        for delta in stream_text_deltas(prompt):
            yield _format_event(delta, event="delta")
        yield _format_event("[DONE]", event="done")
    except Exception as e:  # surface upstream failure to the client
        yield _format_event(str(e), event="error")
