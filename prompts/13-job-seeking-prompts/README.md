# Job-Seeking Automation Workspace (13-job-seeking-prompts)

Personal workspace for Juan Jaramillo's automated job-search and application pipeline.
This is an _automation project_ (Playwright bots, scripts, agent files) rather than a
pure prompt library — see the master index for the prompt categories.

## Contents

- `.github/agents/` + `.github/prompts/` — GitHub agent definitions and the linked-in
  assistant prompt.
- `.agents/skills/` — skills used by the pipeline, including the canonical
  `juan-jaramillo-job-persona` skill (single source of truth for Juan's persona).
- `prompts/` — application/workflow prompts (e.g. `job-application-agentic-workflow-prompt.md`).
- `scripts/`, `cover_letters/`, and root-level `*.py` — automation entry points and helpers.
- `*.md` reports — run logs and status summaries.

## Notes

- Runtime artifacts (screenshots, logs, HTML dumps, `lib/`, `venv/`) are gitignored —
  see root `.gitignore`.
- The persona skill lives in exactly one place:
  `.agents/skills/juan-jaramillo-job-persona/` (including the `clone/` module set).
