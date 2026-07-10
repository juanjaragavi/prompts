# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## High-Level Architecture and Structure

This repository is primarily a collection of AI system prompts, documentation, JSON configurations, and small utility projects. It is not a traditional software application, but rather a knowledge base and automation toolkit.

The core structure consists of:

- `prompts/`: Contains 92+ AI system prompts organized into 13 numbered categories (e.g., `01-email-marketing/`, `02-topfinanzas-content/`). Each category has its own `README.md`.
  - Prompts are written in Markdown. They follow a specific structure: Role definition, capabilities, limitations, expected behavior, instructions, and examples.
  - Variables are typically in CAPS or `%VARIABLE%` format.
- `documents/`: Stores documentation, automation shell scripts (e.g., `emailgenius-broadcasts-generator.sh`), and content files.
- `json/`: Houses JSON payloads, schemas, and API configurations (e.g., ActiveCampaign templates).
- `projects/`: Contains standalone utility projects, such as `jsonl-maker` (Python) and a snake game.
- `scripts/`: Additional automation scripts.
- `.agent/rules/`: Contains repository-specific agent rules (e.g. `prompts-rules.md`).

Key integration points and workflows:

- **Email Marketing (ActiveCampaign)**: Prompts in `01-email-marketing`, combined with JSON payloads and automation scripts in `documents/`.
- **TopFinanzas Content**: Content creation flows (Quiz, Review, Recommender, etc.) located in `02-topfinanzas-content`.
- **Social Media & Courses**: LinkedIn automation and educational material generators located in their respective numbered folders.
- **Master Index**: The root `PROMPTS_INDEX.md` acts as the source of truth for all prompts in the repository.

## Common Development Tasks

There is no global build process or test suite. Validation is manual, and the focus is on maintaining clean organization and clear documentation.

### Formatting

The repository uses Prettier for formatting standard files.

- Format all supported files: `npm run format` or `npm run lint`
- Check formatting: `npm run format:check`

### Working with Prompts

When adding or modifying prompts, follow these steps:

1. Ensure the prompt file uses descriptive `kebab-case` or `snake_case` naming (with contextual prefixes like `TF_` for TopFinanzas).
2. Place it in the appropriate `prompts/XX-<category>/` directory.
3. If introducing a new capability, update the category's `README.md`.
4. Update the master index (`PROMPTS_INDEX.md`) if a new category or major feature is added.

### Validating JSON Payloads

Validate any new or modified JSON files before committing:

```bash
python -m json.tool json/<file>.json
```

### Python Projects (e.g., `jsonl-maker`)

Utility Python projects reside in `projects/` and manage their own virtual environments.

```bash
cd projects/jsonl-maker/
source venv/bin/activate
python jsonlmaker.py
```

### Git Workflow

- Feature branches should be used for major additions (e.g., `add-new-prompt-name`).
- A commit message template exists at `.llm_commit_message.txt.template` and `commit_message.txt.template`.

### Maintenance

Periodically run maintenance commands to keep the repository clean:

- Archive old prompts: `mkdir -p prompts/<category>/archive && mv prompts/<category>/deprecated-*.md prompts/<category>/archive/`
- Clean up Python environments: `find projects/ -type d -name "venv" -exec rm -rf {} +`
