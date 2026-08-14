# Resume Variants

## Purpose

This file maps each job-search track to the specific resume PDF variant, primary keywords, and when to use it. Use this whenever an application asks which resume to submit or when tailoring materials for a specific role.

**The only target role is Forward Deployed Engineer (FDE).** The tracks below are no longer separate role targets — they are resume framings. Choose the one whose keyword set best matches the specific FDE posting's emphasis.

## Track-to-Resume Mapping

| Track                                                    | Resume PDF                              | Primary Keywords                                                                                                                                              | Use When                                                                                                                                               |
| :------------------------------------------------------- | :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Track 1: AI/LLM Engineering**                          | `Juan_Jaramillo_Resume_AI_LLM.pdf`      | Vertex AI (Gemini 3), GPT-5.x, Claude 4/5, Llama 4, LangChain, LangGraph, CrewAI, PEFT, RLHF, fine-tuning, prompt engineering, RAG, agentic workflows         | Role focuses on model selection, custom RAG pipelines, fine-tuning, multi-agent orchestration, or ML engineering                                       |
| **Track 2: Vibe Coding / AI-Native Product Engineering** | `Juan_Jaramillo_Resume_Vibe_Coding.pdf` | Next.js 16, React 19.2, Astro 6, Tailwind CSS v4, TypeScript, AI-assisted dev (Cursor, Claude Code, Copilot), rapid prototyping, prompt versioning (Git Flow) | Role focuses on high-velocity AI-assisted development, vibe coding, forward-deployed engineering, or AI-native product building                        |
| **Track 3: CMS + React/Next.js Architecture**            | `Juan_Jaramillo_Resume_CMS_React.pdf`   | Headless WordPress, WPGraphQL, decoupled CMS, Next.js migrations, React 19.2, Astro 6, Core Web Vitals, SSR/SSG, legacy modernization                         | Role focuses on modernizing monolithic content platforms, headless CMS migrations, or full-stack React/Next.js architecture                            |
| **General / Multi-track / Senior Leadership**            | `Juan_Jaramillo_Master_Resume.pdf`      | AI-Native Full-Stack Architect, AI Development Lead, TopNetworks ecosystem, 17+ years, full-stack + AI specialization                                         | Role spans multiple tracks, is a senior leadership role, or the JD is broad enough that a generalist positioning is stronger than a track-specific one |

## Cover Letter Variants

Five tailored cover letters are available in the workspace at `cover_letters/`:

| File                | Target Role Pattern                                        | Use When                                                            |
| :------------------ | :--------------------------------------------------------- | :------------------------------------------------------------------ |
| `cover_letter_1.md` | Vibe Coder / AI-native product builder (Darwin AI example) | Track 2 roles emphasizing AI-assisted velocity and product building |
| `cover_letter_2.md` | (Inspect file before use)                                  | Verify target role against the letter's opening                     |
| `cover_letter_3.md` | (Inspect file before use)                                  | Verify target role against the letter's opening                     |
| `cover_letter_4.md` | (Inspect file before use)                                  | Verify target role against the letter's opening                     |
| `cover_letter_5.md` | (Inspect file before use)                                  | Verify target role against the letter's opening                     |

The master cover letter style reference is `Juan_Jaramillo_Master_Cover_Letter.pdf`.

## Selection Heuristics

1. **Every application is for a Forward Deployed Engineer role.** Pick the resume variant whose keyword set best matches that specific FDE posting's technical emphasis — do not treat the variants as alternative role targets.
2. **Match the resume to the JD's primary language.** If the FDE posting emphasizes LangGraph/CrewAI/RAG/fine-tuning, use the AI/LLM variant. If it emphasizes Next.js/Astro/AI-assisted delivery velocity, use the Vibe Coding variant. If it emphasizes legacy modernization and headless/SSR migrations, use the CMS/React variant.
3. **When in doubt, use the Master Resume.** It carries the broadest client-embedded delivery narrative and works for most FDE postings.
4. **Never submit two resume variants to the same application.** Pick the strongest single fit.
5. **Tailor the cover letter to the specific role and company.** The five existing cover letters are starting points, not final drafts. Always reframe the opening around Forward Deployed Engineering — last-mile delivery, custom integrations, and client-embedded production work.
6. **Cross-check against `career-goals.md`** to confirm the FDE framing and compensation intent.

## File Inventory

All resume PDFs live in the root of the persona package:

- `Juan_Jaramillo_Master_Resume.pdf`
- `Juan_Jaramillo_Resume_AI_LLM.pdf`
- `Juan_Jaramillo_Resume_Vibe_Coding.pdf`
- `Juan_Jaramillo_Resume_CMS_React.pdf`
- `Juan_Jaramillo_Master_Cover_Letter.pdf`

The general-purpose resume source (for the LinkedIn Automation pipeline) is hosted at `https://files.catbox.moe/3bha32.pdf` per `30_day_execution_strategy.md:164`.

## Maintenance Rule

When a new resume variant is created, update this file before submitting any application. Keep the mapping current so the agent always picks the right PDF without guessing.
