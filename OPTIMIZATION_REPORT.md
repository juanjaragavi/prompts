# Repository Optimization Report

**Date:** 2026-08-06
**Scope:** Structural cleanup, deduplication, and portability pass on the `prompts` knowledge base.
**No git commit/push performed** — all changes are in the working tree for review.

---

## Before / After

| Metric                                             | Before   | After                              |
| -------------------------------------------------- | -------- | ---------------------------------- |
| Tracked repo size                                  | 122.6 MB | 63.5 MB                            |
| Tracked `prompts/` (excl. local `venv`)            | ~64 MB   | **5.0 MB**                         |
| Files deleted/moved out of the tree                | —        | 472 (`git status` `D`)             |
| Files modified                                     | —        | 53                                 |
| New files (indexes, scripts, changelogs)           | —        | 14 (incl. 2 scripts, catalog JSON) |
| `prompts/` `.md` files (excl. archive)             | ~245     | 227                                |
| Zero-byte files (excl. archive/venv)               | 14+      | **0**                              |
| Hardcoded `/Users/` paths in `.md`                 | 23 files | **0**                              |
| `Juan_Jaramillo_Job_Applications_Report.md` copies | 4        | **1**                              |
| `PROMPTS_INDEX.md` phantom entries                 | 12       | **0**                              |

---

## What was done

### 1. Security & `.gitignore`

- Appended artifact/credential patterns to `.gitignore` (kept the existing 4 entries):
  `screenshots/`, `**/logs/`, `**/terminal_logs/`, `**/__pycache__/`, `**/.playwright-mcp/`,
  `13-job/*.html`, `13-job/lib/`, `*_filled_form.png`, plus `**/venv/`, `.freebuff/`, `.pytest_cache/`.
- Quarantined **7 credential/auth files** to `~/quarantine-20260806/` (no copies left in-tree):
  `documents/env.txt`, `keys_screenshot_1.md`, `keys_screenshot_2.md`, `linkedin_credentials.md`,
  `google_account_test.txt`, `accenture_login_view.txt`, `linkedin_login_snapshot.txt`.
- Verified remaining repo matches on `ghp_ | sk-... | BEGIN PRIVATE | password` are prose false positives only.

### 2. Runtime artifacts removed (`13-job-seeking-prompts/`)

- Deleted whole artifact trees: `logs/` (incl. all zero-byte), `terminal_logs/`, `__pycache__/`,
  `.playwright-mcp/`, `inspections/`, `screenshots/`, `lib/`, `Skills/`.
- Deleted 15 HTML page dumps, all root-level `.png` screenshots, ~80 `.txt` page snapshots,
  ~45 JSON run dumps, 2 stray `.log` files.
- Deleted `list_all_tabs2.py` (byte-identical to `list_all_tabs.py`); removed `resume.pdf`
  (byte-identical to referenced `3bha32.pdf`).
- Kept: all `.py` scripts, `.md` reports, `prompts/`, `scripts/`, `cover_letters/`,
  `.agent/`, `.agents/`, `.github/`, `evals/`, `config.*`, `skills-lock.json`, PDFs.
- **Everything moved to `/tmp/artifact-cleanup-20260806/` (450 files) — recoverable until reboot.**

### 3. Juan persona deduplicated → 1 canonical location

- Canonical: `prompts/13-job-seeking-prompts/.agents/skills/juan-jaramillo-job-persona/`.
- Removed 3 full/partial copies (`juan-jaramillo-job-persona/`, `.agent/skills/…/`,
  `prompts/juan-jaramillo-job-persona-clone/`) and the redundant `juan-jaramillo-job-persona.zip`.
- The canonical `clone/` files were 7-line _relocation stubs_; merged in the **fullest clone set**
  from `prompts/juan-jaramillo-job-persona-clone/` (151–322-line files) so `SKILL.md`'s
  `clone/*.md` references resolve to real content.
- Deleted 5 top-level duplicates (byte-verified identical to canonical).
- Updated the `clone/` path reference in `.github/prompts/linkedin-assistant.prompt.md`.
- Kept `evals/juan-jaramillo-job-persona/` (different content — eval configs).

### 4. Version-sprawl archived (not deleted) + CHANGELOGs

- **01 EmailGenius:** kept MCP-integrated canonical; archived v1/v2/v3 (differ by <25 lines),
  2 zero-byte placeholders, and the 4 `email-genius-activecampaign-*` variants.
- **10 Milton:** kept `milton-v5.md` + filter/scheduler/messenger; archived `milton-v4.md`,
  `milton-optimized.md`, and the zero-byte `parcero-processor.md`.
- **03 LinkedIn:** kept `jj-linkedin-poster.md`; archived `linkedin-matic(.md/-V2)`, `linkedin-poster.md`.
- **Near-dupes:** archived `07/code-and-text-optimizer.md`, `11/maker.md`,
  `marstals_latam_community_mananger.md`, `budgetbee-…-tool-usage.md` (its unique
  "Tool Usage, Memory, and Context Management" section was appended to the canonical).
- `CHANGELOG.md` written in 01, 03, 07, 10, 11; category READMEs got archive pointers.

### 5. Token heavyweights

- **`dropshipper-json.md`:** extracted the 47 KB embedded catalog verbatim to
  `json/dropshipper-product-catalog.json` (JSON round-trips via `python3 -m json.tool`);
  prompt now carries `<!-- Catalog: … -->` + a load-instruction line. File: 59 KB → 12.6 KB.
- **`sebas.md` (37 KB):** inspected — it is persona _instructions_ with embedded Astro
  site-source reference material (not a transcript). Left intact per plan; added
  `<!-- tokens: ~5.5K … -->` note.

### 6. Portability

- Replaced hardcoded macOS home-directory prefixes in **17 `.md`/`.agent.md`/`.prompt.md`**
  files (repo paths → repo-relative; local paths → `~/`); one generic placeholder example fixed.
- Rewrote root `README.md` (accurate overview + fixed broken
  `talent-assisto-saas.md` link → `prompts/04-talent-assisto/talent-assisto-saas.md`).

### 7. Validator + regenerated index

- **`scripts/validate_prompts.py`** (stdlib-only): zero-byte files, intra-category md5 dupes,
  index drift, `/Users/` paths, broken links, front-matter warning. **Exits 0.**
- **`scripts/regenerate_index.py`** (stdlib-only): regenerates `PROMPTS_INDEX.md` from disk
  (size + ~tokens per file, correct counts, accurate statistics).
- `PROMPTS_INDEX.md` regenerated from disk — lists **117 real entries** (114 prompts + the
  `text-formatter.txt` template + 2 job-seeking notes), zero phantom files.

### 8. Verification (all pass)

- `python3 scripts/validate_prompts.py` → **exit 0** (113 informational front-matter warnings).
- `grep -r '/Users/' prompts --include='*.md'` → **0**.
- Zero-byte files (excl. archive/venv) → **0**. Persona report copies → **1**.
- Tracked `prompts/` size → **5.0 MB**.

---

## Left ambiguous / needs human decision

1. **`EFSET_Certificate.pdf` is byte-identical to `Juan_Jaramillo_Master_Cover_Letter.pdf`**
   (same md5) — likely a mislabeled file. Both kept in the canonical persona dir; verify which is real.
2. **Recruiter outreach skill duplicated** at repo-root `.agent/skills/recruiter-outreach-response/`
   (full templates) and `13-job/.agent/skills/…` (templates.md is a relocation stub →
   `prompts/recruiter-outreach-response-templates.md`). ~1.7 MB of PDFs duplicated; kept both per
   the "keep `.agent/`" rule — decide whether the workspace copy should be removed.
3. **`juan-jaramillo-resume.md`** exists both at `13-job/` root and inside the recruiter skill
   (identical). Same decision as #2.
4. **Milton v4/optimized and the LinkedIn poster variants differ substantially** (200+ diff lines)
   from the kept canonicals — archived rather than deleted, so nothing is lost.
5. **`loom-video-script.md` vs `loom_video_script.md`** and root vs `prompts/`
   `job-application-agentic-workflow-prompt.md` — each pair differs; both copies kept.
6. **`venv/` (164 MB, untracked)** left in place and gitignored — deleting it requires your call.
7. **`.py` scripts with hardcoded `/Users/` paths** were left untouched (out of scope for this pass,
   and several carry uncommitted edits). Flagging for a future pass.
8. **Category READMEs** (01/03/10) still describe archived files in their listings — now annotated
   with archive pointers; consider pruning later.
9. **`commit_message.txt.template` == `.llm_commit_message.txt.template`** (identical, both kept).
10. **Top-level `prompts/archive/minimal-writing.md`** left as-is (already archived).

## Housekeeping

- `~/quarantine-20260806/` — 7 credential files (delete after confirming you don't need them).
- `/tmp/artifact-cleanup-20260806/` — 450 staged artifact files (auto-cleared on reboot).
- Nothing was committed or staged. Review `git status` and stage selectively (`git add` per file,
  not `git add -A`).
