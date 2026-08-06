#!/usr/bin/env python3
"""Regenerate PROMPTS_INDEX.md from the actual contents of prompts/.

Preserves the existing index style (emoji headers, per-category tables) and lists
real files with byte sizes and a ~tokens estimate (words x 1.33). Removes phantom
entries and corrects the statistics block. Keeps the "By Integration" section.

Usage: python3 scripts/regenerate_index.py [--write]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
INDEX = ROOT / "PROMPTS_INDEX.md"

EXCLUDED_NAMES = {"README.md", "00-notes.md", "CHANGELOG.md"}

CATEGORY_EMOJIS = {
    "01-email-marketing": "📧",
    "02-topfinanzas-content": "🏦",
    "03-social-media": "📱",
    "04-talent-assisto": "💼",
    "05-seo-content": "📝",
    "06-courses-education": "🎓",
    "07-development-coding": "💻",
    "08-ecommerce-dropshipping": "🛒",
    "09-business-proposals": "💼",
    "10-utilities-assistants": "🔧",
    "11-landing-pages": "🚀",
    "12-templates-system": "📋",
    "13-job-seeking-prompts": "💼",
}

FALLBACK_FOCUS = {
    "01-email-marketing": "Email campaign automation, ActiveCampaign/SendGrid integration",
    "02-topfinanzas-content": "Financial content automation for TopFinanzas ecosystem",
    "03-social-media": "LinkedIn automation, multi-platform social media management",
    "04-talent-assisto": "AI talent management platform",
    "05-seo-content": "SEO blog posts, image optimization, text enhancement",
    "06-courses-education": "Educational content, AI productivity courses",
    "07-development-coding": "Code generation, API integration, system prompt engineering",
    "08-ecommerce-dropshipping": "Product management, dropshipping automation",
    "09-business-proposals": "Business proposals, economic documents, startup planning",
    "10-utilities-assistants": "General-purpose AI assistants, data tools, communication",
    "11-landing-pages": "Landing page content, marketing copy",
    "12-templates-system": "Base templates, system configurations",
    "13-job-seeking-prompts": "Job-search automation workspace, skills, and reports",
}

CATEGORY_NAMES = {
    "01-email-marketing": "Email Marketing & ActiveCampaign",
    "02-topfinanzas-content": "TopFinanzas Content Creation",
    "03-social-media": "Social Media Management",
    "04-talent-assisto": "TalentAssisto SaaS",
    "05-seo-content": "SEO & Content Optimization",
    "06-courses-education": "Courses & Education",
    "07-development-coding": "Development & Coding",
    "08-ecommerce-dropshipping": "E-commerce & Dropshipping",
    "09-business-proposals": "Business Proposals",
    "10-utilities-assistants": "Utilities & Personal Assistants",
    "11-landing-pages": "Landing Pages & Marketing",
    "12-templates-system": "Templates & System Files",
    "13-job-seeking-prompts": "Job Seeking & Career Development",
}


def fmt_size(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f}MB"
    if size >= 1024:
        return f"{size / 1024:.1f}KB"
    return f"{size}B"


def fmt_tokens(words: int) -> str:
    tokens = words * 1.33
    if tokens >= 1000:
        return f"~{round(tokens / 100) * 100}"
    return f"~{max(10, round(tokens / 10) * 10)}"


def collect_categories():
    out = []
    for d in sorted(PROMPTS.iterdir()):
        if not d.is_dir() or not re.match(r"^\d\d-", d.name):
            continue
        files = [
            p
            for p in sorted(list(d.glob("*.md")) + list(d.glob("*.txt")))
            if p.name not in EXCLUDED_NAMES and p.is_file()
        ]
        out.append((d, files))
    return out


def main() -> int:
    write = "--write" in sys.argv
    categories = collect_categories()

    total_prompts = sum(len(files) for _, files in categories)
    largest_cat = max(categories, key=lambda c: len(c[1]))
    smallest_cats = [c for c in categories if len(c[1]) == min(len(f) for _, f in categories)]
    all_files = [(p.stat().st_size, p) for _, files in categories for p in files]
    largest_file = max(all_files) if all_files else (0, None)
    total_words = sum(
        len(p.read_text(encoding="utf-8", errors="ignore").split())
        for _, files in categories
        for p in files
    )

    lines = []
    lines.append("# 📚 Prompts Index & Catalog")
    lines.append("")
    lines.append(f"**Total Prompts:** {total_prompts} system prompts  ")
    lines.append(f"**Total Categories:** {len(categories)} organized categories  ")
    lines.append("**Repository:** <https://github.com/juanjaragavi/prompts>  ")
    lines.append("**Maintained by:** <https://juanjaramilloai.vercel.app>")
    lines.append("**Last Updated:** regenerated automatically from disk")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📂 Category Structure")
    lines.append("")
    lines.append("All prompts are organized into categorized subdirectories within `prompts/`:")
    lines.append("")
    lines.append("```markdown")
    lines.append("prompts/")
    for d, files in categories:
        n = len(files)
        label = "prompt" if n == 1 else "prompts"
        lines.append(
            f"├── {d.name}/ ({n} {label}) {CATEGORY_EMOJIS.get(d.name, '📄')}"
        )
    lines.append("```")
    lines.append("")

    for d, files in categories:
        num = d.name[:2]
        emoji = CATEGORY_EMOJIS.get(d.name, "📄")
        title = CATEGORY_NAMES.get(d.name, d.name.replace("-", " ").title())
        focus = FALLBACK_FOCUS.get(d.name, "")
        n = len(files)
        label = "prompt" if n == 1 else "prompts"
        lines.append(f"## {emoji} {num}. {title} ({n} {label})")
        lines.append("")
        lines.append(f"**Path:** `prompts/{d.name}/`  ")
        lines.append(f"**Focus:** {focus}")
        lines.append("")
        lines.append("| File | Size | ~Tokens |")
        lines.append("| ---- | ---- | ------- |")
        for p in files:
            size = p.stat().st_size
            words = len(p.read_text(encoding="utf-8", errors="ignore").split())
            lines.append(f"| `{p.name}` | {fmt_size(size)} | {fmt_tokens(words)} |")
        lines.append("")
        if (d / "README.md").exists():
            lines.append(f"[📖 View Category README](./prompts/{d.name}/README.md)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Quick navigation
    lines.append("## 🔍 Quick Navigation")
    lines.append("")
    lines.append("### By Use Case")
    lines.append("")
    for d, _ in categories:
        lines.append(
            f"**{CATEGORY_NAMES.get(d.name, d.name)}:** [{d.name}](./prompts/{d.name}/)"
        )
    lines.append("")
    lines.append("### By Integration")
    lines.append("")
    lines.append("**ActiveCampaign:** [01-email-marketing](./prompts/01-email-marketing/)  ")
    lines.append("**SendGrid:** [07-development-coding](./prompts/07-development-coding/)  ")
    lines.append("**LinkedIn:** [03-social-media](./prompts/03-social-media/)  ")
    lines.append("**BudgetBee:** [03-social-media](./prompts/03-social-media/)  ")
    lines.append("**TopFinanzas:** [02-topfinanzas-content](./prompts/02-topfinanzas-content/)")
    lines.append("")

    # Statistics
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Statistics")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("| ------ | ----- |")
    lines.append(f"| **Total Prompts** | {total_prompts} |")
    lines.append(f"| **Total Categories** | {len(categories)} |")
    lines.append(f"| **Largest Category** | {largest_cat[0].name} ({len(largest_cat[1])}) |")
    lines.append(
        f"| **Smallest Categories** | {', '.join(c[0].name for c in smallest_cats)} "
        f"({len(smallest_cats[0][1])}) |"
    )
    lines.append(f"| **Total Words** | {total_words:,} |")
    if largest_file[1]:
        lines.append(
            f"| **Largest File** | {largest_file[1].name} ({fmt_size(largest_file[0])}) |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📝 Notes")
    lines.append("")
    lines.append("- All prompts use `snake_case` or `kebab-case` naming")
    lines.append(
        "- `13-job-seeking-prompts/` is an automation workspace; its entries include "
        "run reports and skill files alongside prompts"
    )
    lines.append("- Numbered prefixes (01-13) maintain category order")
    lines.append("- Each category has its own README.md")
    lines.append("- Superseded/duplicate versions are archived under each category's `archive/`")
    lines.append("- `~Tokens` estimates are words × 1.33")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Repository:** <https://github.com/juanjaragavi/prompts>  ")
    lines.append("**Maintained by:** <https://juanjaramilloai.vercel.app>  ")
    lines.append("**Last Updated:** regenerated automatically from disk  ")
    lines.append(f"**Total Categories:** {len(categories)}")
    lines.append("")

    content = "\n".join(lines)
    if write:
        INDEX.write_text(content, encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)} ({len(lines)} lines, {total_prompts} prompts)")
    else:
        print(content)
        print(f"(dry run — {total_prompts} prompts; pass --write to write the file)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
