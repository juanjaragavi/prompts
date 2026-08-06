# Changelog — 01 Email Marketing & ActiveCampaign

## 2026-08-06 — Version-sprawl consolidation

Consolidated the EmailGenius and ActiveCampaign variants. Content is preserved in `archive/`.

### Kept (canonical)

- `system-prompt-emailgenius-broadcasts-generator-with-tools-and-mcp.md` — the MCP-integrated
  EmailGenius prompt (canonical for the EmailGenius suite).
- `email-genius-activecampaign.md` — standard ActiveCampaign generator (simple, non-tools option).
- `TF_ActiveCampaign_Email_Generator.md`, `parcero-emailer.md`, `activecampaign-email-builder.md` —
  meaningfully different scopes; kept as-is.

### Archived

- `v1-system-prompt-emailgenius-broadcasts-generator.md`, `v2-system-prompt-emailgenius-broadcasts-generator-with-tools.md`,
  `v3-system-prompt-emailgenius-broadcasts-generator-integrated.md` — the v1/v2/v3 suite; differ
  from each other by <25 lines and are superseded by the MCP-integrated canonical.
- `system-prompt-emailgenius-broadcasts-generator.md`, `system-prompt-emailgenius-broadcasts-generator-with-tools.md`
  — zero-byte placeholders.
- `email-genius-activecampaign-FINAL-REMOTE.md`, `email-genius-activecampaign-agentic.md`,
  `email-genius-activecampaign-minimal.md`, `email-genius-activecampaign-programatic.md` — same
  scope as the standard `email-genius-activecampaign.md`, different emphasis.
