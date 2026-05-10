# TeamHQ agent setup

This repo is the target codebase for the [TeamHQ](https://github.com/kitrakrev/teamhq)
migration agent. This note explains how the agent operates against this repo
so reviewers know what to expect on incoming PRs.

## How the agent runs

1. Agent reads repo layout + `CODEOWNERS` to determine affected teams.
2. Per affected team, agent drafts a plan card grounded in that team's
   Hyperspell brain (Slack `#backend`, Notion ADRs, prior GitHub PRs).
3. Team leads approve their plan card via the TeamHQ web app.
4. On quorum, agent opens a PR on a `teamhq/run-<id>` branch with the
   smallest reviewable first step toward the approved plans.
5. Each run appends one line to `TEAMHQ-NOTES.md` with run id + trigger.

## Conventions the agent must respect

Sourced from `README.md` and surfaced via Hyperspell. Agent treats these
as hard constraints:

- All OpenAI calls wrapped in `with_retries` (see PR #347, INC-203).
- Streaming opt-in only. Default `stream=False`.
- Retry policy fixed: exponential backoff, cap 30s, 5 attempts. DevOps
  signoff required to change.
- Pydantic models use `class Config` style. No `@field_validator`.

## Where to look

| Item | Path |
| --- | --- |
| Migration plan | `CHANGELOG.md` |
| Sacred retry wrapper | `src/retry_wrapper.py` |
| LLM client (migration target) | `src/llm_client.py` |
| Run log | `TEAMHQ-NOTES.md` |
| Agent source | https://github.com/kitrakrev/teamhq |
