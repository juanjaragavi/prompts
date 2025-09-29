# 📧 Email Marketing & ActiveCampaign

**Category:** Email Marketing Automation  
**Prompt Count:** 14 prompts  
**Primary Integration:** ActiveCampaign API, SendGrid

## Overview

This category contains AI system prompts designed for email marketing automation, broadcast
generation, and email campaign management. These prompts integrate primarily with ActiveCampaign and
SendGrid APIs to automate email workflows.

## Key Use Cases

- 📬 Email broadcast generation and automation
- 🎯 Marketing campaign creation
- 📝 Email content optimization
- 🔗 API integration with ActiveCampaign
- 📊 Email template management

## Featured Prompts

### ⭐ Top Priority

- **`system-prompt-emailgenius-broadcasts-generator-with-tools-and-mcp.md`** (22KB) - Most
  comprehensive, includes MCP tools integration
- **`activecampaign-email-builder.md`** (10KB) - ActiveCampaign email builder with Gutenberg support
- **`TF_ActiveCampaign_Email_Generator.md`** - TopFinanzas-specific email generator

### EmailGenius Suite (Versioned)

1. **v1** - `v1-system-prompt-emailgenius-broadcasts-generator.md` (17KB) - Initial version
2. **v2** - `v2-system-prompt-emailgenius-broadcasts-generator-with-tools.md` (18KB) - Added tool
   integration
3. **v3** - `v3-system-prompt-emailgenius-broadcasts-generator-integrated.md` (18KB) - Fully
   integrated

### Specialized Variants

- **`email-genius-activecampaign-FINAL-REMOTE.md`** (6.7KB) - Production remote version
- **`email-genius-activecampaign-agentic.md`** - Agentic AI approach
- **`email-genius-activecampaign-minimal.md`** - Minimal/lightweight version
- **`email-genius-activecampaign-programatic.md`** - Programmatic automation
- **`email-genius-activecampaign.md`** - Standard version

### Other Tools

- **`parcero-emailer.md`** - Parcero email automation system
- **`system-prompt-emailgenius-broadcasts-generator.md`** - Base version
- **`system-prompt-emailgenius-broadcasts-generator-with-tools.md`** - With tools integration

## Related Resources

### Shell Scripts (in `/documents/`)

- `emailgenius-broadcasts-generator.sh` - Main automation script
- `email-broadcast-image-generation-script.sh` - Image generation for emails
- `email-broadcast-image-generation-script-minimized.sh` - Optimized version

### JSON Payloads (in `/json/`)

- `activecampaign-message-example-json-payload.json` - Example API payload

## Integration Details

### ActiveCampaign API

All prompts in this category support ActiveCampaign API integration for:

- Campaign creation and management
- Contact list management
- Automation triggers
- Email template deployment

### Tools & Technologies

- ActiveCampaign API v3
- SendGrid API
- MCP (Model Context Protocol) integration
- WordPress Gutenberg blocks
- JSON/HTML email templates

## Quick Start

```bash
# View all email marketing prompts
ls -la /Users/macbookpro/Github/prompts/prompts/01-email-marketing/

# Copy a prompt to use
cat email-genius-activecampaign.md

# Run automation script
./documents/emailgenius-broadcasts-generator.sh
```

## Version History

- **Latest:** MCP-integrated version with full tool support
- **v3:** Fully integrated with external services
- **v2:** Added tool integration capabilities
- **v1:** Initial EmailGenius system prompt

## Notes

- Some files may be empty placeholders for future development
- FINAL-REMOTE versions are production-ready
- Agentic versions use autonomous AI decision-making
- Programmatic versions focus on API automation

---

**Last Updated:** September 29, 2025  
**Maintained by:** Juan Jaramillo  
**Related Categories:** [05-seo-content](../05-seo-content/),
[02-topfinanzas-content](../02-topfinanzas-content/)
