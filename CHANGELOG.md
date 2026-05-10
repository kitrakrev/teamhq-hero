# Changelog

All notable changes to this repo tracked here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Migration plan: openai 0.28.1 → 1.x

First reviewable step. Full migration lands across multiple PRs to keep
per-team conventions intact.

- [ ] Pin upgrade target and document rollout (this PR).
- [ ] Swap `openai.ChatCompletion.create` → `OpenAI().chat.completions.create`
      in `src/llm_client.py`. Keep `with_retries` wrapper untouched (PR #347,
      INC-203).
- [ ] Preserve retry policy: exponential backoff, cap 30s, 5 attempts.
      No change without DevOps signoff.
- [ ] Keep `stream=False` default. Streaming opt-in only.
- [ ] Pydantic models stay on `class Config`. No `@field_validator`.
- [ ] Update `tests/test_llm_client.py` mocks to new client shape.
- [ ] Bump `requirements.txt` once green on CI.

### Added
- `CHANGELOG.md` (this file).
- `TEAMHQ.md` — agent setup + per-team convention pointers.
