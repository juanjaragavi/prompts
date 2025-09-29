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

- `prompts/` - **87 AI system prompts organized into 12 categories** 📂
  - `01-email-marketing/` (14 prompts) - Email automation, ActiveCampaign
  - `02-topfinanzas-content/` (8 prompts) - Financial content creation
  - `03-social-media/` (9 prompts) - LinkedIn, social media automation
  - `04-talent-assisto/` (3 prompts) - ⭐ Featured SaaS product
  - `05-seo-content/` (7 prompts) - SEO blog posts, optimization
  - `06-courses-education/` (3 prompts) - Course creation
  - `07-development-coding/` (9 prompts) - Code generation, APIs
  - `08-ecommerce-dropshipping/` (3 prompts) - E-commerce automation
  - `09-business-proposals/` (3 prompts) - Business documents
  - `10-utilities-assistants/` (22 prompts) - Personal assistants
  - `11-landing-pages/` (2 prompts) - Marketing pages
  - `12-templates-system/` (4 files) - Base templates
  - Each category has its own README.md for documentation
- `documents/` - Documentation, scripts, and content files (44 files)
- `json/` - JSON payloads, schemas, and API configurations (12 files)
- `projects/` - Utility projects (jsonl-maker, snake game)
- `notes/` - Personal notes and walkthroughs
- `scripts/` - Automation scripts (commit_and_push.sh)
- `.codellm/rules/` - Repository-specific rules and guidelines

## Common Development Tasks

### Working with Prompts

```bash
# List all prompt categories
ls -d prompts/*/

# View a specific category
ls -la prompts/01-email-marketing/

# Read a category's documentation
cat prompts/01-email-marketing/README.md

# Search for specific prompt types (e.g., email generators)
find prompts/ -name "*email*"

# Search for TopFinanzas related prompts
find prompts/02-topfinanzas-content/ -name "*.md"

# Find prompts with specific capabilities
grep -r "ActiveCampaign" prompts/01-email-marketing/

# Count prompts by category
for dir in prompts/*/; do echo "$(basename $dir): $(ls -1 $dir/*.md 2>/dev/null | wc -l | tr -d ' ') files"; done
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

# Stage and commit prompt changes (use appropriate category)
git add prompts/[category-name]/new-prompt.md
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
find prompts/ -name "*.md" | wc -l

# Find recently modified prompts
find prompts/ -name "*.md" -mtime -30

# View the master index
cat PROMPTS_INDEX.md
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
- Category prefixes: `01-` through `12-` for organization
- JSON files: service/purpose descriptive names
- Scripts: purpose-based naming (e.g., `email-broadcast-image-generation-script.sh`)

### Directory Organization

- All prompts are organized into 12 categorized subdirectories
- Each category has a README.md explaining its prompts
- Master index at repository root: `PROMPTS_INDEX.md`
- Categories use numbered prefixes (01-12) for consistent ordering

## Key Integration Points

### ActiveCampaign Email System

- Email prompts in `prompts/01-email-marketing/` (14 prompts)
- JSON payload examples in `json/activecampaign-*.json`
- Shell scripts for automation in `documents/`
- Featured: EmailGenius with MCP tools integration

### Content Creation Flows

- TopFinanzas prompts in `prompts/02-topfinanzas-content/` (8 prompts)
- TF_FLOWS_CC series: Quiz, Review, Recommender, Requirements, Coder
- Image prompt optimization tools
- Mexico and UK market-specific content

### Social Media Management

- Social media prompts in `prompts/03-social-media/` (9 prompts)
- LinkedIn automation (4 prompts)
- BudgetBee social media manager (MCP-integrated)
- Community management for Marstals

### Course Creation Tools

- Course prompts in `prompts/06-courses-education/` (3 prompts)
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
cat prompts/[category]/[prompt-name].md

# Check prompt formatting
grep -E "^#|^##|^###" prompts/[category]/[prompt-name].md

# View all prompts in a category
ls -1 prompts/01-email-marketing/
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

- TalentAssisto Builder: `prompts/04-talent-assisto/talent-assisto-saas.md` ⭐
- EmailGenius MCP: `prompts/01-email-marketing/system-prompt-emailgenius-broadcasts-generator-with-tools-and-mcp.md`
- BudgetBee Social: `prompts/03-social-media/budgetbee-social-media-manager-tool-usage.md`
- TopFinanzas Coder: `prompts/02-topfinanzas-content/TF_FLOWS_CC_Coder.md`
- LinkedIn Poster: `prompts/03-social-media/jj-linkedin-poster.md`

### Key Scripts

- Email broadcast generator: `documents/emailgenius-broadcasts-generator.sh`
- Image generation: `documents/generate-image.sh`

### Important Configuration Files

- Master prompts index: `PROMPTS_INDEX.md` 📚
- Repository rules: `.codellm/rules/prompts-rules.mdc`
- VS Code settings: `.vscode/settings.json`
- Category READMEs: `prompts/*/README.md`

## Development Workflow

1. **Adding New Prompts**: 
   - Identify the appropriate category (01-12)
   - Create prompt in `prompts/[category]/` following naming conventions
   - Update category README.md if needed
   - Update `PROMPTS_INDEX.md` if adding new category features
2. **Documentation**: Update relevant docs in `documents/` when adding new integrations
3. **JSON Payloads**: Store example payloads in `json/` with descriptive names
4. **Scripts**: Place automation scripts in `documents/` or `scripts/` with clear naming
5. **Testing**: Test prompts and scripts before committing
6. **Commit**: Use clear, action-based commit messages
7. **Review**: Self-review changes, ensure no sensitive data

## Category Selection Guide

When adding a new prompt, choose the appropriate category:

- **01-email-marketing**: Email campaigns, ActiveCampaign, SendGrid
- **02-topfinanzas-content**: Financial content, TF_FLOWS_CC series
- **03-social-media**: LinkedIn, Twitter, Facebook, Instagram automation
- **04-talent-assisto**: Recruitment, HR, talent management
- **05-seo-content**: SEO blog posts, image optimization
- **06-courses-education**: Course creation, educational content
- **07-development-coding**: Code generation, APIs, development tools
- **08-ecommerce-dropshipping**: Product management, e-commerce
- **09-business-proposals**: Business docs, proposals, startup planning
- **10-utilities-assistants**: Personal assistants, data extraction, general tools
- **11-landing-pages**: Landing pages, marketing copy
- **12-templates-system**: Base templates, system configurations

## Maintenance Tasks

```bash
# Archive old prompts (move to category archive folder)
mkdir -p prompts/[category]/archive
mv prompts/[category]/deprecated-*.md prompts/[category]/archive/

# Clean up Python virtual environments (181MB!)
find projects/ -type d -name "venv" -exec rm -rf {} +

# Check for large files
find . -type f -size +1M -exec ls -lh {} \;

# Update git ignore for sensitive files
echo "documents/credenciales.txt" >> .gitignore

# Verify prompt organization
for dir in prompts/*/; do 
  echo "$(basename $dir): $(ls -1 $dir/*.md 2>/dev/null | wc -l | tr -d ' ') prompts"
done

# Regenerate PROMPTS_INDEX.md if needed
cat PROMPTS_INDEX.md
```

## Notes

- This is primarily a prompt and documentation repository, not a traditional code project
- No build process or test suite - validation is manual
- Focus on maintaining clean organization and clear documentation
- Regular review and updates of prompts for accuracy
