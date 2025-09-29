# 🏦 TopFinanzas Content Creation

**Category:** Financial Content Automation  
**Prompt Count:** 8 prompts  
**Primary Use:** TopFinanzas platform content generation

## Overview

This category contains specialized AI system prompts for creating financial content for the TopFinanzas ecosystem. The prompts follow standardized workflows (TF_FLOWS_CC_*) for generating quizzes, reviews, articles, recommendations, and other financial content types.

## TF_FLOWS_CC Series (Version 1.0)

These are the core content creation flows for TopFinanzas:

### 📝 **Quiz Generator** 
- **File:** `TF_FLOWS_CC_Quiz_Generator_1_0.md` (9.4KB)
- **Purpose:** Generate interactive credit card and financial product quizzes
- **Output:** Quiz questions, answers, scoring logic

### ⭐ **Review Generator**
- **File:** `TF_FLOWS_CC_Review_Generator_1_0.md` (8.7KB)
- **Purpose:** Create comprehensive financial product reviews
- **Output:** Structured reviews with pros/cons, ratings, comparisons

### 🎯 **Recommender Generator**
- **File:** `TF_FLOWS_CC_Recommender_Generator_1_0.md` (9.3KB)
- **Purpose:** Build personalized financial product recommendation systems
- **Output:** Recommendation logic, matching algorithms

### 📋 **Requirements Generator**
- **File:** `TF_FLOWS_CC_Reqs_Generator_1_0.md` (8.7KB)
- **Purpose:** Generate financial product requirement documents
- **Output:** Detailed requirement specifications

### 💻 **Coder**
- **File:** `TF_FLOWS_CC_Coder.md` (11KB)
- **Purpose:** Generate code for TopFinanzas features and integrations
- **Output:** React/TypeScript/Next.js code

### 🖼️ **Article Image Prompt Generator**
- **File:** `TF_FLOWS_CC_Article_Image_Prompt_Generator_1.0.md` (3.6KB)
- **Purpose:** Create optimized image prompts for financial articles
- **Output:** DALL-E/Midjourney prompts for financial imagery

## General Content Prompts

### 📰 **TopFinanzas Content Creation**
- **File:** `topfinanzas-content-creation-prompt.md` (4.3KB)
- **Purpose:** General-purpose TopFinanzas content generation
- **Scope:** Articles, blog posts, landing pages

### 🇲🇽 **TopFinanzas Pages MX System**
- **File:** `topfinanzas-pages-mx-system-prompt.md` (11KB)
- **Purpose:** Mexico-specific TopFinanzas page generation
- **Market:** Mexican financial products and regulations
- **Language:** Spanish (es-MX)

## Content Types Supported

| Type | Generator | Output Format |
|------|-----------|---------------|
| **Quizzes** | Quiz Generator | Interactive JSON/HTML |
| **Reviews** | Review Generator | Structured Markdown/HTML |
| **Recommendations** | Recommender Generator | Logic + UI components |
| **Articles** | Content Creation | SEO-optimized blog posts |
| **Requirements** | Reqs Generator | Technical specifications |
| **Images** | Image Prompt Generator | AI image prompts |
| **Code** | Coder | React/TypeScript |

## Integration Points

### Related TopFinanzas Projects
- **mejoresfinanzas** - Mexican financial wellness platform
- **uk-topfinanzas-com** - UK market version
- **quiz-topfinanzas-mx** - Quiz app (Next.js)

### Content Workflow
```
1. Requirements Generator → Define product specs
2. Content Creation → Write article/page
3. Image Prompt Generator → Create visual prompts
4. Review/Quiz Generator → Add interactive elements
5. Recommender Generator → Add personalization
6. Coder → Implement features
```

## Quick Start

```bash
# View all TopFinanzas prompts
ls -la /Users/macbookpro/Github/prompts/prompts/02-topfinanzas-content/

# Use the quiz generator
cat TF_FLOWS_CC_Quiz_Generator_1_0.md

# Generate Mexico-specific content
cat topfinanzas-pages-mx-system-prompt.md
```

## Naming Convention

**Format:** `TF_FLOWS_CC_[ContentType]_[Version].md`

- **TF** = TopFinanzas
- **FLOWS** = Standardized workflows
- **CC** = Content Creator
- **ContentType** = Quiz, Review, Recommender, etc.
- **Version** = 1_0, 2_0, etc.

## Related Resources

### Documentation (in `/documents/`)
- `TF_page-content-creation-flow.md` - Complete workflow guide

### Related Categories
- [01-email-marketing](../01-email-marketing/) - For email campaigns
- [05-seo-content](../05-seo-content/) - For SEO optimization
- [03-social-media](../03-social-media/) - For social promotion

## Notes

- All prompts are v1.0 - expect v2.0 iterations
- Mexico (MX) and UK markets have specific prompts
- Coder prompt generates Next.js/React/TypeScript code
- Image generator is optimized for financial visuals

---

**Last Updated:** September 29, 2025  
**Maintained by:** Juan Jaramillo  
**Platform:** TopFinanzas Ecosystem