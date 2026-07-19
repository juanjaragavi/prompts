<!-- OPENWIKI:START -->

## OpenWiki

This repository uses OpenWiki for recurring code documentation. Start with `openwiki/quickstart.md`, then follow its links to architecture, workflows, domain concepts, operations, integrations, testing guidance, and source maps.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->

# Claude Guidelines for Prompts Repository

## Project Overview
This repository is a collection of AI system prompts, documentation, and utility projects (email marketing, content generation, TopFinanzas, BudgetBee). There is no automated build process or test suite; validation is manual.

## Commands
- **Find Prompts**: `find prompts/ -name \"*.md\"`
- **Validate JSON**: `python -m json.tool json/<file>.json`
- **Run jsonl-maker**: `cd projects/jsonl-maker/ && source venv/bin/activate && python jsonlmaker.py`
- **Check Formatting**: `grep -E \"^#|^##|^###\" prompts/<category>/<prompt-name>.md`

## Directory Structure
- `prompts/`: AI system prompts organized into numbered categories (`01-` to `13-`).
- `documents/`: Documentation, shell scripts, and content files.
- `json/`: JSON payloads, schemas, and API configurations.
- `projects/`: Utility projects (e.g., jsonl-maker).
- `scripts/`: Automation scripts (e.g., `commit_and_push.sh`).

## Style & Formatting
- **Prompt Structure**: Must include:
  1. System description/role definition
  2. Capabilities section
  3. Limitations section
  4. Expected behavior
  5. Ethical guidelines (when applicable)
  6. Clear instructions and examples
- **Variables**: Use ALL CAPS or `%VARIABLE%` format.
- **Naming Conventions**: 
  - Prompts: Descriptive names with hyphens. Use `TF_` for TopFinanzas and `CC_` for Content Creator.
  - Categories: Use numbered prefixes (`01-13`) for consistent ordering.
  - JSON & Scripts: Purpose-based naming.
- **Documentation**: Always update the `PROMPTS_INDEX.md` and category `README.md` when adding new prompts.

## Important Rules
- **Security**: NEVER commit API keys, tokens, or passwords. Make sure `documents/credenciales.txt` is gitignored. Use environment variables for sensitive configurations.
- **Non-Interactive Execution**: Deployment scripts and automated workflows must NOT open interactive editors like nano or vim (no commands that require manual intervention like `:qa` or `Ctrl+x`).
- **Cross-Repo Sync**: When managing TopFinanzas/BudgetBee tasks, ensure codebase parity across the related Next.js repositories (`topfinanzas-us-next`, `uk-topfinanzas-com`, `topfinanzas-mx-next`, `budgetbee-next`) while respecting project-specific localization and branding.
