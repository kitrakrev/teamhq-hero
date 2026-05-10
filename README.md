# teamhq-hero

> The **target repo** for the [TeamHQ](https://github.com/kitrakrev/teamhq) migration agent demo.
> Pinned at `openai==0.28.1` so the agent can demonstrate a real upgrade
> while preserving the team's `retry_wrapper` convention.

## Why this repo exists

This repo is the *codebase under change* in the TeamHQ demo. The agent reads
its layout, drafts per-team plans grounded in the team's Hyperspell brain
(Slack + Notion + GitHub history), and opens real PRs back here once each
team-lead approves their plan card.

| Surface | Link |
| --- | --- |
| Agent + web app source | https://github.com/kitrakrev/teamhq |
| Live web demo | https://web-nine-lemon-57.vercel.app |
| Example agent-opened PR | https://github.com/kitrakrev/teamhq-hero/pull/4 |

## Layout

```
src/
  retry_wrapper.py    # team-owned (Sarah). Sacred — see PR #347.
  llm_client.py       # uses @with_retries
tests/
  test_retry_wrapper.py
  test_llm_client.py
TEAMHQ-NOTES.md       # appended by every agent run
```

## Team conventions encoded

The migration agent must respect these (sourced from `#backend` Slack +
ADR-12 in Notion, surfaced via Hyperspell):

1. All OpenAI calls wrapped in `with_retries` (PR #347, INC-203).
2. Streaming is opt-in only (default `stream=False`).
3. Retry policy: exponential backoff, cap 30 s, 5 attempts. Do not change
   without DevOps signoff.
4. Pydantic models keep `class Config` style; no `@field_validator`.

## CI

GitHub Actions runs `pytest -v` on every PR.

## Recent agent activity

Each TeamHQ run appends a line to `TEAMHQ-NOTES.md` with the run id and
trigger. PRs opened by the agent live under `pull/*` and follow the
branch-name pattern `teamhq/run-<id>`.
