---
name: jj-linkedin-jobs
description: Provides Juan Miguel Jaramillo Gaviria's complete job-search profile — confirmed contact facts, target job titles, preferred locations and work modes, compensation range, work authorization, experience history, and skill set — for searching, screening, and applying to opportunities on LinkedIn Jobs. Use this skill any time a task involves searching LinkedIn Jobs, building a LinkedIn job search URL, filtering or scoring job postings for fit, answering LinkedIn Easy Apply screening questions (years of experience, salary expectations, work authorization, sponsorship, relocation, notice period), drafting a cover letter or InMail for a job application, or filling out a LinkedIn job application — even if the request is phrased generically like "find me AI engineer jobs on LinkedIn" or "apply to this posting" without naming him, since this is his personal LinkedIn job-search assistant.
---

# Juan Jaramillo — LinkedIn Job Search & Application

Candidate: Juan Miguel Jaramillo Gaviria ("Juan Jaramillo" on LinkedIn). This skill is the
single source of truth for his job-search preferences and facts — use it instead of asking
the user to repeat this information every time.

## Contact snapshot
- Full name: Juan Miguel Jaramillo Gaviria
- Email: juanamillo@proton.me
- Phone: +57 305 420 6139
- Base: Bogotá, Colombia (GMT-5)
- LinkedIn: https://www.linkedin.com/in/juan-jaramillo-ai/
- GitHub: https://github.com/juanjaragavi

## Target job titles / search keywords
Use these (individually or OR'd together) as LinkedIn Jobs search keywords:
- Artificial Intelligence Engineer / AI Engineer / AI Developer
- Prompt Engineer
- AI Strategy Consultant / Artificial Intelligence Consultant
- Machine Learning Engineer
- Generative AI Engineer / LLM Engineer
- AI Solutions Architect / AI Solutions Lead
- Vibe Coder / AI-Native IDE Engineer / AI-Native Full-Stack Engineer

CMS + React/Next.js roles (e.g. "Next.js Developer", "Headless CMS Engineer") are **only**
a fit when AI-assisted development or headless modernization is central to the role — screen
these out otherwise, they are not a general target.

## Location & work mode
- Location types: **On-site** and **Remote** (Hybrid is not selected/wanted)
- On-site and remote locations (same set for both):
  - Bogotá, D.C., Capital District, Colombia
  - Medellín, Antioquia, Colombia
  - Mexico City, Mexico
  - Buenos Aires Province, Argentina
- Fully remote roles are acceptable from anywhere as long as they are open to hiring someone
  based in Colombia (contractor or remote-employee basis).

## Availability & employment type
- Start date: Immediately — actively applying, available to start right away.
- Employment types wanted: Full-time, Contract, Temporary, Hourly.
  - Note: LinkedIn's native `f_JT` filter does not have a distinct "Hourly" value (only
    Full-time/Part-time/Contract/Temporary/Volunteer/Internship/Other). When filtering by UI,
    treat "Hourly" as covered by Contract/Temporary, and surface hourly-rate interest in the
    application message/cover letter instead of relying on a filter.

## Compensation target
USD $3,500–$4,500/month, or the annual equivalent (~USD $42,000–$54,000/year). Quote this
range (or state "open to negotiation within this band") whenever a screening question asks
for desired/expected salary.

## Work authorization
- Authorized to work in Colombia.
- **Not** authorized to work in the U.S., U.K., or EU — do not claim otherwise, and do not
  pursue roles that require in-country sponsorship/relocation to those regions.
- Available globally as an independent contractor / remote developer regardless of client
  location, as long as the engagement does not require local work authorization.

## Experience & skills summary
- 17+ years in digital/technology roles (entrepreneurship, web/software development, digital
  marketing, and — since ~2022 — enterprise generative AI).
- ~4 years each in Python, ML, GenAI, LLM/NLP, and prompt engineering.
- Full professional proficiency in English (native Spanish speaker).
- Key skills: Python, JS/TS, SQL, Next.js, React, Astro, Tailwind, WordPress, Vertex AI/Gemini,
  LangChain, LangGraph, CrewAI, PEFT/RLHF, GCP, PostgreSQL, BigQuery, Supabase, Docker, Vercel,
  Cursor / AI-assisted development.
- Other skills: ML, LLM/NLP, prompt engineering, AI-assisted development, CMS modernization,
  headless architecture, cloud platforms (GCP, AWS), containerization (Docker), database
  management (PostgreSQL, BigQuery), front-end frameworks (React, Next.js, Astro), styling
  (Tailwind), version control (Git/GitHub).

For the full experience timeline (companies, dates, project details) and LinkedIn profile
analysis, read `references/profile.md` — use it to tailor cover letters/answers to a specific
job posting instead of guessing at background details.

For ready-to-use answers to common Easy Apply screening questions, read
`references/screening-answers.md` before filling out an application.

## Building a LinkedIn Jobs search
Run `scripts/build_search_url.py` to generate a search URL instead of manually reasoning
through LinkedIn's filter query params (they use short non-obvious codes). Example:

```bash
python3 scripts/build_search_url.py \
  --titles "Prompt Engineer" "AI Engineer" "Machine Learning Engineer" \
  --locations "Bogota, D.C., Capital District, Colombia" "Remote" \
  --work-mode remote onsite \
  --employment-type F C T
```

This prints one search URL per requested location (LinkedIn only accepts a single `location`
value per search, so the preference set of 4 cities needs one run per city, or a keywords-only
search with `f_WT=2` for remote-anywhere). Open the printed URL with the browser automation
tool available in the session (e.g. a `chrome-devtools`/Playwright MCP `new_page`/`navigate`
call) to actually view results.

## Screening job postings for fit
Treat a posting as a strong match when it satisfies ALL of:
1. Title/responsibilities align with the target roles above (or is an AI-centric CMS/Next.js
   role).
2. Location is Remote (open to Colombia-based candidates) OR on-site/hybrid in one of the four
   listed cities.
3. Compensation is at or above $3,500/month (or unspecified/negotiable).
4. Does not require U.S./U.K./EU work authorization as a hard condition — remote/contractor
   arrangements are fine even for companies based there.

Flag/skip postings that:
- Require on-site presence outside the four listed cities.
- Explicitly require U.S./U.K./EU citizenship, green card, or visa sponsorship with no remote
  option.
- Are pure WordPress/CMS/front-end roles with no AI angle (outside the conditional CMS+AI
  exception above).
- Pay meaningfully below the target compensation band with no stated flexibility.

## Applying (Easy Apply / forms)
When actually filling out application forms, pair this skill with the
`playwright-automation-fill-in-form` skill for the mechanics of driving the browser — use this
skill's contact snapshot, preferences, and `references/screening-answers.md` as the source of
truth for what to type into each field.
