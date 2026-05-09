# teamhq-hero

> Hero target repo for the TeamHQ migration agent demo.
> Pinned at `openai==0.28.1` so the agent can demonstrate a real upgrade
> while preserving the team's `retry_wrapper` convention.

## Layout

```
src/
  retry_wrapper.py   # team-owned (Sarah). Sacred — see PR #347.
  llm_client.py      # uses @with_retries
tests/
  test_retry_wrapper.py
  test_llm_client.py
```

## Team conventions encoded

Migration agent must respect these (sourced from `#backend` Slack + ADR-12 in Notion):

1. All OpenAI calls wrapped in `with_retries` (PR #347, INC-203).
2. Streaming is opt-in only (default `stream=False`).
3. Retry policy: exponential backoff, cap 30s, 5 attempts. Do not change without DevOps signoff.
4. Pydantic models keep `class Config` style; no `@field_validator`.

## CI

GitHub Actions runs `pytest -v` on every PR.
