#!/bin/bash

# Script to create README files for remaining prompt categories
# Author: Juan Jaramillo
# Date: September 29, 2025

PROMPTS_DIR="/Users/macbookpro/Github/prompts/prompts"

# Category 05: SEO Content
cat > "$PROMPTS_DIR/05-seo-content/README.md" << 'EOF'
# 📝 SEO & Content Optimization

**Category:** SEO-Optimized Content Generation  
**Prompt Count:** 7 prompts  
**Focus:** Blog posts, images, text optimization

## Prompts

- `seo-optimized-blog-posts-generator.md` (14KB)
- `seo-optimized-blog-posts-generator-xml.md` (15KB) ⭐
- `images-prompt-optimization-assistant.md` (2.8KB)
- `optimized-image-generator-english.md` (4.2KB)
- `optimized-image-generator-spanish.md` (4.7KB)
- `text-optimizer-prompt-gpt5-xml.md` (1.1KB)
- `code-and-text-optimizer.md` (1.2KB)

## Use Cases
- SEO blog post generation
- Image prompt optimization (DALL-E/Midjourney)
- Text content optimization
- Multilingual content (English/Spanish)

---
**Last Updated:** September 29, 2025
EOF

# Category 06: Courses & Education
cat > "$PROMPTS_DIR/06-courses-education/README.md" << 'EOF'
# 🎓 Courses & Education

**Category:** Educational Content Creation  
**Prompt Count:** 3 prompts  
**Focus:** AI productivity, course design

## Prompts

- `ai-for-personal-productivity-course-writer.md` (2.8KB)
- `generative-ai-course-creator.md` (4.9KB)
- `course-designer.md` (7.2KB)

## Use Cases
- AI productivity course creation
- Generative AI educational content
- Course curriculum design
- Learning module development

---
**Last Updated:** September 29, 2025
EOF

# Category 07: Development & Coding
cat > "$PROMPTS_DIR/07-development-coding/README.md" << 'EOF'
# 💻 Development & Coding

**Category:** Programming & Development Tools  
**Prompt Count:** 9 prompts  
**Focus:** Code generation, conversion, API integration

## Prompts

- `codecraft-pro.md` (5.6KB)
- `expert-programmer.md` (2.4KB)
- `code-converter-system-prompt.md` (5.7KB)
- `techguru.md` (3.6KB)
- `github-local-repo-analyzer.md` (1.3KB)
- `send-grid-api-assistant.md` (4.0KB) ⭐
- `prompt-engineer.md` (4.0KB)
- `system-prompt-maker.md` (2.5KB)
- `system-prompt-maker-es.md` (2.5KB)

## Use Cases
- Code generation & conversion
- GitHub repository analysis
- SendGrid API integration
- System prompt engineering
- Technical documentation

---
**Last Updated:** September 29, 2025
EOF

# Category 08: E-commerce & Dropshipping
cat > "$PROMPTS_DIR/08-ecommerce-dropshipping/README.md" << 'EOF'
# 🛒 E-commerce & Dropshipping

**Category:** E-commerce Automation  
**Prompt Count:** 3 prompts  
**Focus:** Product management, dropshipping

## Prompts

- `dropshipper-json.md` (58KB) 🔥 **LARGEST FILE**
- `gina-dropshipping-assistant.md` (13KB)
- `gina-wiki.md` (6.5KB)

## Use Cases
- Dropshipping product management
- Product catalog automation
- E-commerce content generation
- Supplier integration

---
**Last Updated:** September 29, 2025
EOF

# Category 09: Business Proposals
cat > "$PROMPTS_DIR/09-business-proposals/README.md" << 'EOF'
# 💼 Business Proposals

**Category:** Business Development  
**Prompt Count:** 3 prompts  
**Focus:** Proposals, economic documents, startups

## Prompts

- `economic-proposal-genie.md` (4.9KB)
- `proposal-maker.md` (3.5KB)
- `startup-gpt.md` (2.5KB)

## Use Cases
- Economic proposal generation
- Business proposal creation
- Startup business planning
- Investment documents

---
**Last Updated:** September 29, 2025
EOF

# Category 10: Utilities & Assistants
cat > "$PROMPTS_DIR/10-utilities-assistants/README.md" << 'EOF'
# 🔧 Utilities & Personal Assistants

**Category:** General-Purpose AI Assistants  
**Prompt Count:** 22 prompts  
**Focus:** Personal assistants, data extraction, communication

## Personal Assistants
- `jj-assistant.md` (4.7KB) ⭐
- `super-ai-assistant.md` (2.3KB)
- `sebas.md` (36KB) 🔥 **SECOND LARGEST**

## Data Tools
- `data-extractor.md` (2.6KB)
- `structured-data-extractor.md` (2.7KB)
- `multilingual-summarizer-es.md` (2.5KB)

## Specialized Tools
- `food-analyzer.md` (1.6KB)
- `reaction-checker.md` (2.0KB)
- `mx-to-uk-migration-agent-pro.md` (2.7KB)
- `clima-ai.md` (4.0KB)

## Milton Communication Suite
- `milton-v4.md` (3.8KB)
- `milton-v5.md` (6.3KB)
- `milton-optimized.md` (5.1KB)
- `milton-filter.md` (1.7KB)
- `milton-scheduler.md` (2.8KB)
- `milton-messenger-system-prompt.md` (2.7KB)

## Parcero Suite
- `parcero.md` (4.6KB)
- `parcero-sms.md` (2.3KB)
- `parcero-processor.md`

## Meta Prompts
- `claude-reflection.md` (1.9KB)
- `prompt-reflection.md` (299B)
- `model-response.md` (1.4KB)

---
**Last Updated:** September 29, 2025
EOF

# Category 11: Landing Pages
cat > "$PROMPTS_DIR/11-landing-pages/README.md" << 'EOF'
# 🚀 Landing Pages & Marketing

**Category:** Landing Page Creation  
**Prompt Count:** 2 prompts  
**Focus:** Marketing pages, product launches

## Prompts

- `covox-landing-page.md` (2.7KB)
- `maker.md` (2.2KB)

## Use Cases
- Landing page content generation
- Product launch pages
- Marketing copy creation
- CTA optimization

---
**Last Updated:** September 29, 2025
EOF

# Category 12: Templates & System
cat > "$PROMPTS_DIR/12-templates-system/README.md" << 'EOF'
# 📋 Templates & System Files

**Category:** Base Templates & System Prompts  
**Prompt Count:** 4 files  
**Focus:** Template files, system configurations

## Files

- `00-template.md` (1.1KB) ⭐ **Modified Today!**
- `system-prompt.md` (12KB)
- `prompt.md` (9.5KB)
- `text-formatter.txt` (2.2KB)

## Purpose

These are foundational template files used as starting points for creating new prompts. The 00-template.md file serves as the standard template for all new prompt files.

---
**Last Updated:** September 29, 2025
EOF

echo "✅ All category README files created successfully!"
echo "📁 Location: $PROMPTS_DIR/*/README.md"