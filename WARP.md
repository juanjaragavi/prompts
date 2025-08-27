# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a collection of AI system prompts, documentation, and utility projects primarily focused on:
- AI system prompts for various assistants and tools
- Email marketing automation (ActiveCampaign integration)
- Content generation tools
- Personal productivity and course creation
- JSON payloads and API integration examples

Repository URL: https://github.com/juanjaragavi/prompts

## Repository Structure

### Key Directories
- `prompts/` - System prompts for AI assistants (84+ Markdown files)
  - Naming convention: `snake_case` or `kebab-case`, prefix with context (e.g., `TF_` for TopFinanzas)
- `documents/` - Documentation, scripts, and content files
- `json/` - JSON payloads, schemas, and API configurations  
- `projects/` - Utility projects (e.g., jsonl-maker Python script)
- `notes/` - Personal notes and walkthroughs
- `.codellm/rules/` - Repository-specific rules and guidelines

## Common Development Tasks

### Working with Prompts
```bash
# List all prompts
ls -la prompts/

# Search for specific prompt types (e.g., email generators)
grep -r "email" prompts/ --include="*.md"

# Search for TopFinanzas related prompts
find prompts/ -name "TF_*.md"

# Find prompts with specific capabilities
grep -r "ActiveCampaign" prompts/
```

### Working with Scripts
```bash
# List all shell scripts in documents
find documents/ -name "*.sh"

# Check email generation scripts
ls -la documents/email*.sh
```

### Python Projects
```bash
# Navigate to jsonl-maker project
cd projects/jsonl-maker/

# Activate virtual environment (if exists)
source venv/bin/activate

# Run the jsonl maker
python jsonlmaker.py
```

### Git Operations
```bash
# Check repository status
git status

# View recent changes
git log --oneline -10

# Create feature branch for new prompt
git checkout -b add-new-prompt-name

# Stage and commit prompt changes
git add prompts/new-prompt.md
git commit -m "Add system prompt for [purpose]"

# Push to remote
git push origin main
```

### Search and Analysis
```bash
# Find all JSON configuration files
find json/ -name "*.json"

# Search for specific API integrations
grep -r "activecampaign" json/

# Count total number of prompts
ls -1 prompts/*.md | wc -l

# Find recently modified prompts
find prompts/ -name "*.md" -mtime -30
```

## Important Patterns and Standards

### Prompt Structure
All prompts in `prompts/` follow this general structure:
1. System description/role definition
2. Capabilities section
3. Limitations section
4. Expected behavior
5. Ethical guidelines (when applicable)
6. Clear instructions and examples

### Variable Conventions
- Placeholders use CAPS or %VARIABLE% format
- Variables are documented with expected values
- Examples demonstrate variable usage

### File Naming
- Prompts: descriptive names with underscores or hyphens
- Context prefixes: `TF_` (TopFinanzas), `CC_` (Content Creator)
- JSON files: service/purpose descriptive names
- Scripts: purpose-based naming (e.g., `email-broadcast-image-generation-script.sh`)

## Key Integration Points

### ActiveCampaign Email System
- Multiple prompts for email generation in `prompts/`
- JSON payload examples in `json/activecampaign-*.json`
- Shell scripts for automation in `documents/`

### Content Creation Flows
- TopFinanzas content creation prompts (`TF_FLOWS_CC_*.md`)
- Quiz, review, and article generators
- Image prompt optimization tools

### Course Creation Tools
- AI productivity course prompts
- Generative AI course creator systems
- Course design templates

## Security Considerations

- Never commit API keys, tokens, or passwords directly to files
- Use environment variables for sensitive configuration
- Review files before committing to ensure no sensitive data
- Credentials file (`documents/credenciales.txt`) should be gitignored

## Testing and Validation

### Prompt Testing
```bash
# Copy prompt content for testing
cat prompts/[prompt-name].md

# Check prompt formatting
grep -E "^#|^##|^###" prompts/[prompt-name].md
```

### JSON Validation
```bash
# Validate JSON syntax
python -m json.tool json/[file].json

# Pretty print JSON
cat json/[file].json | python -m json.tool
```

## Quick Reference

### Most Used Prompts
- TalentAssisto Builder: `prompts/talent-assisto-saas.md`
- ActiveCampaign Email Generators: `prompts/TF_ActiveCampaign_*.md`, `prompts/email-genius-*.md`
- Content Creation: `prompts/TF_FLOWS_CC_*.md`
- Social Media: `prompts/linkedin-*.md`, `prompts/*social-media*.md`

### Key Scripts
- Email broadcast generator: `documents/emailgenius-broadcasts-generator.sh`
- Image generation: `documents/generate-image.sh`

### Important Configuration Files
- Repository rules: `.codellm/rules/prompts-rules.mdc`
- VS Code settings: `.vscode/settings.json`

## Development Workflow

1. **Adding New Prompts**: Create in `prompts/` following naming conventions and structure standards
2. **Documentation**: Update relevant docs in `documents/` when adding new integrations
3. **JSON Payloads**: Store example payloads in `json/` with descriptive names
4. **Scripts**: Place automation scripts in `documents/` with clear naming
5. **Testing**: Test prompts and scripts before committing
6. **Commit**: Use clear, action-based commit messages
7. **Review**: Self-review changes, ensure no sensitive data

## Maintenance Tasks

```bash
# Archive old prompts (move to archive folder if needed)
mkdir -p prompts/archive
mv prompts/deprecated-*.md prompts/archive/

# Clean up Python virtual environments
find projects/ -type d -name "venv" -exec rm -rf {} +

# Check for large files
find . -type f -size +1M -exec ls -lh {} \;

# Update git ignore for sensitive files
echo "documents/credenciales.txt" >> .gitignore
```

## Notes

- This is primarily a prompt and documentation repository, not a traditional code project
- No build process or test suite - validation is manual
- Focus on maintaining clean organization and clear documentation
- Regular review and updates of prompts for accuracy
