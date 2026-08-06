#!/usr/bin/env python3
"""Validate the prompts/ knowledge base.

Checks (exits non-zero on failure):
  1. Zero-byte files anywhere under prompts/ (excluding archive/)
  2. Duplicate content (md5 collisions) within the same category
  3. Index drift: every .md listed in PROMPTS_INDEX.md exists on disk, and every
     category .md on disk is listed (excluding README.md, 00-notes.md, CHANGELOG.md)
  4. Hardcoded /Users/ paths in .md files
  5. Broken relative links in README.md / PROMPTS_INDEX.md
  6. YAML front-matter presence (informational warning only)

Usage: python3 scripts/validate_prompts.py
"""

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
INDEX = ROOT / "PROMPTS_INDEX.md"
EXCLUDED_NAMES = {"README.md", "00-notes.md", "CHANGELOG.md"}
# Directories that are not repo content (gitignored local environments/tool data)
IGNORED_DIR_NAMES = {"venv", ".venv", "node_modules", ".git", ".freebuff",
                     ".pytest_cache", "__pycache__", "archive"}
SCAN_DIRS = [PROMPTS, ROOT / ".github", ROOT / ".agent", ROOT / ".agents", ROOT]

errors = []
warnings = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def is_excluded(rel: Path) -> bool:
    # Skip gitignored local dirs and any archive/ directory
    return any(part in IGNORED_DIR_NAMES for part in rel.parts)


# ---------------------------------------------------------------------------
# 1. Zero-byte files
# ---------------------------------------------------------------------------
for p in PROMPTS.rglob("*"):
    if p.is_file() and p.stat().st_size == 0:
        rel = p.relative_to(ROOT)
        if not is_excluded(rel):
            err(f"zero-byte file: {rel}")

# ---------------------------------------------------------------------------
# 2. Duplicate content within a category (md5)
# ---------------------------------------------------------------------------
categories = sorted(
    d for d in PROMPTS.iterdir()
    if d.is_dir() and d.name not in IGNORED_DIR_NAMES
)
for cat in categories:
    hashes = {}
    for f in sorted(cat.glob("*.md")):
        if f.name in EXCLUDED_NAMES:
            continue
        digest = hashlib.md5(f.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(f.name)
    for digest, names in hashes.items():
        if len(names) > 1:
            err(f"duplicate content in {cat.name}/: {', '.join(names)}")

# ---------------------------------------------------------------------------
# 3. Index drift
# ---------------------------------------------------------------------------
index_text = INDEX.read_text(encoding="utf-8", errors="ignore") if INDEX.exists() else ""
indexed = set(re.findall(r"`([^`]+\.md)`", index_text))

for name in sorted(indexed):
    matches = [m for m in PROMPTS.rglob(name) if not is_excluded(m.relative_to(ROOT))]
    if not matches:
        err(f"PROMPTS_INDEX.md lists missing file: {name}")

for cat in categories:
    for f in sorted(cat.glob("*.md")):
        if f.name in EXCLUDED_NAMES:
            continue
        if f.name not in indexed:
            err(f"on disk but not in PROMPTS_INDEX.md: {f.relative_to(ROOT)}")

# ---------------------------------------------------------------------------
# 4. Hardcoded /Users/ paths
# ---------------------------------------------------------------------------
md_files = []
for base in (ROOT, PROMPTS, ROOT / ".github", ROOT / ".agent", ROOT / ".agents"):
    if base.exists():
        md_files += [p for p in base.rglob("*.md") if p.is_file()]
seen = set()
for p in md_files:
    if p in seen or is_excluded(p.relative_to(ROOT)):
        continue
    seen.add(p)
    text = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"/Users/[A-Za-z0-9_\- ]+", text):
        err(f"hardcoded /Users/ path in {p.relative_to(ROOT)}: {m.group(0)!r}")
        break  # one error per file is enough

# ---------------------------------------------------------------------------
# 5. Broken relative links in README.md / PROMPTS_INDEX.md
# ---------------------------------------------------------------------------
for idx_file in (ROOT / "README.md", INDEX):
    if not idx_file.exists():
        continue
    text = idx_file.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"\]\(([^)]+)\)", text):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "#", "mailto:", "data:")):
            continue
        target_path = target.split("#")[0]
        if not target_path:
            continue
        resolved = (idx_file.parent / target_path).resolve()
        if not resolved.exists():
            err(f"broken link in {idx_file.name}: {target}")

# ---------------------------------------------------------------------------
# 6. YAML front-matter presence (informational)
# ---------------------------------------------------------------------------
for cat in categories:
    for f in sorted(cat.glob("*.md")):
        if f.name in EXCLUDED_NAMES:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        has_fm = text.startswith("---") and "description:" in text.split("---", 2)[1][:1000]
        if not has_fm:
            warn(f"no YAML description front-matter: {f.relative_to(ROOT)}")

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print("=" * 60)
print("prompts repository validator")
print("=" * 60)
for w in warnings:
    print(f"WARN  {w}")
for e in errors:
    print(f"ERROR {e}")
print("-" * 60)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
