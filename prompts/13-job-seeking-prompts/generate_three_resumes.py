import os
import pypdf
from xhtml2pdf import pisa

def generate_pdf(html_content, output_filename):
    with open(output_filename, "wb") as f:
        pisa_status = pisa.CreatePDF(html_content, dest=f)
    if pisa_status.err:
        return False
    return True

working_dir = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts"

# COMMON CSS STYLES FOR ALL RESUMES
css_styles = """
    @page {
        size: letter;
        margin: 10mm 12mm 10mm 12mm;
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2d3748;
        line-height: 1.3;
        font-size: 8.5pt;
    }
    a {
        color: #1e3a8a;
        text-decoration: none;
    }
    .header {
        text-align: center;
        margin-bottom: 6px;
        border-bottom: 1.5px solid #1e3a8a;
        padding-bottom: 4px;
    }
    .name {
        font-size: 18pt;
        font-weight: bold;
        color: #1a202c;
        margin: 0;
        padding: 0;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }
    .tagline {
        font-size: 9.5pt;
        font-weight: bold;
        color: #1e3a8a;
        margin: 2px 0 3px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .contact-info {
        font-size: 8pt;
        color: #4a5568;
        margin: 2px 0 0 0;
    }
    .contact-sep {
        color: #cbd5e1;
        margin: 0 4px;
    }
    h2 {
        font-size: 10pt;
        color: #1e3a8a;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 1px;
        margin-top: 8px;
        margin-bottom: 4px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    .summary-text {
        text-align: justify;
        margin-bottom: 4px;
        font-size: 8.5pt;
    }
    /* Skills Table Grid */
    .skills-table {
        width: 100%;
        margin-bottom: 4px;
    }
    .skills-table td {
        width: 50%;
        vertical-align: top;
        padding: 1px 6px 2px 0;
    }
    .skills-category {
        font-size: 8pt;
        margin-bottom: 1px;
    }
    .skills-category-title {
        font-weight: bold;
        color: #1a202c;
    }
    .skills-items {
        color: #4a5568;
    }
    /* Experience section */
    .entry {
        margin-bottom: 6px;
    }
    .entry-header-table {
        width: 100%;
        margin-bottom: 1px;
    }
    .entry-header-table td {
        padding: 0;
        vertical-align: top;
    }
    .job-title {
        font-size: 9pt;
        font-weight: bold;
        color: #1a202c;
    }
    .company {
        font-size: 9pt;
        font-weight: bold;
        color: #1e3a8a;
    }
    .date-location {
        font-size: 8pt;
        color: #4a5568;
        text-align: right;
        font-style: italic;
    }
    .focus-text {
        font-size: 8pt;
        color: #718096;
        margin-bottom: 2px;
        font-style: italic;
    }
    .entry-bullets {
        margin: 0;
        padding-left: 12px;
    }
    .entry-bullets li {
        margin-bottom: 2px;
        text-align: justify;
        font-size: 8.2pt;
    }
    .education-table {
        width: 100%;
        margin-bottom: 4px;
    }
    .education-table td {
        padding: 2px 0;
        vertical-align: top;
    }
    .degree-title {
        font-size: 8.5pt;
        font-weight: bold;
        color: #1a202c;
    }
    .institution-name {
        font-size: 8.5pt;
        font-weight: bold;
        color: #1e3a8a;
    }
    .edu-meta {
        font-size: 8pt;
        color: #4a5568;
        text-align: right;
        font-style: italic;
    }
    .edu-focus {
        font-size: 8pt;
        color: #4a5568;
        margin-top: 1px;
    }
    .portfolio-box {
        text-align: center;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 4px;
        margin-top: 6px;
        font-size: 8.5pt;
    }
    .page-break {
        page-break-before: always;
    }
"""

# =========================================================================
# 1. AI/LLM Engineering Resume (emphasizing PEFT, RLHF, Vertex AI, Gemini, LangChain, LangGraph, CrewAI)
# =========================================================================
ai_llm_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Juan Miguel Jaramillo Gaviria - AI/LLM Engineering Resume</title>
<style>{css_styles}</style>
</head>
<body>

    <div class="header">
        <div class="name">Juan Miguel Jaramillo Gaviria</div>
        <div class="tagline">AI Engineering Lead | LLM & Generative AI Architect</div>
        <div class="contact-info">
            Bogotá, Colombia <span class="contact-sep">|</span> 
            <a href="mailto:juanamillo@proton.me">juanamillo@proton.me</a> <span class="contact-sep">|</span> 
            +57 305 420 6139 <span class="contact-sep">|</span> 
            <a href="https://juanjaramillo.tech">juanjaramillo.tech</a> <span class="contact-sep">|</span> 
            <a href="https://www.linkedin.com/in/juan-jaramillo-ai">LinkedIn</a>
        </div>
    </div>

    <h2>Professional Summary</h2>
    <div class="summary-text">
        Enterprise AI Engineering Lead and Generative AI Architect with over 17 years of technical execution and entrepreneurial leadership. Specialist in designing, training, and scaling enterprise-grade generative AI systems, orchestrating multi-agent frameworks, and building production-grade RAG pipelines. Hands-on expert in LLM fine-tuning (PEFT, RLHF), robust prompt engineering, prompt versioning via Git Flow, and hallucination risk mitigation. Highly proficient across Next.js 15/16, React 19, TypeScript, Python, and cloud-native architectures on Google Cloud Platform, delivering high-performance AI products that solve complex business objectives and significantly reduce infrastructure overhead.
    </div>

    <h2>Core Proficiencies & Technical Expertise</h2>
    <table class="skills-table">
        <tr>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">AI Engineering & Tuning:</span>
                    <span class="skills-items">LLM Fine-Tuning (PEFT, LoRA, RLHF), Advanced Prompt Engineering, Hallucination Risk Mitigation, Prompt Versioning (Git Flow), Vector Databases (Chroma, PGVector), RAG Architectures.</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">AI Frameworks & Models:</span>
                    <span class="skills-items">LangChain, LangGraph, CrewAI, Vertex AI Agent-to-Agent (A2A), Gemini 2.5 Flash, n8n Workflow Automation, OpenAI GPT, Hugging Face, Cursor AI IDE.</span>
                </div>
            </td>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">Full-Stack Software Engineering:</span>
                    <span class="skills-items">Python (Advanced), TypeScript, JavaScript, ReactJS/React 19, Next.js 15/16, Astro 5, Node.js, SQL, PostgreSQL, Supabase, PHP (Legacy WordPress Architecture).</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">Cloud Infrastructure & DevOps:</span>
                    <span class="skills-items">Google Cloud Platform (Cloud Run, Cloud Armor, BigQuery, Compute Engine), Supabase, Docker, Vercel, PM2, Git, GitHub Actions.</span>
                </div>
            </td>
        </tr>
    </table>

    <h2>Professional Experience</h2>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">AI Development Lead</span> <span class="company">- TopNetworks Inc.</span></td>
                <td class="date-location">Feb 2025 – Jun 2026 | Remote / Bogotá, Colombia</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: Model Tuning (PEFT, RLHF), Vertex AI, Gemini 2.5, LangChain, Multi-Agent Orchestration, Git Flow Prompt Versioning</div>
        <ul class="entry-bullets">
            <li>Spearheaded generative AI engineering strategy and full-stack machine learning architecture for high-performance publishing platforms serving the US, UK, Mexico, and Latin America.</li>
            <li>Designed, built, and launched a core proprietary internal SaaS ecosystem leveraging state-of-the-art LLMs and multi-agent frameworks:
                <ul>
                    <li><strong>EmailGenius:</strong> High-throughput AI email generation engine engineered with Vertex AI, Gemini 2.5 Flash, and PostgreSQL; implemented LLM fine-tuning and rigorous validation pipelines to ensure high personalization.</li>
                    <li><strong>RouteGenius:</strong> High-concurrency probabilistic web traffic routing engine built on Supabase, running concurrent multi-agent AI workflows in n8n via webhooks to dynamically automate traffic routing based on real-time revenue signals.</li>
                    <li><strong>TrafficGenius:</strong> Real-time invalid traffic detection and security intelligence platform utilizing BigQuery ML models and Cloud Armor to isolate fraudulent traffic patterns.</li>
                    <li><strong>Social Media Genius:</strong> AI-native social content generator featuring an interactive canvas editor driven by generative image and text models.</li>
                </ul>
            </li>
            <li>Managed LLM prompt versioning using Git Flow, structured hallucination risk frameworks, implemented evaluation datasets, and deployed production-grade services on GCP.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Prompt Engineer & AI Consultant</span> <span class="company">- Juan Jaramillo (Independent Practice)</span></td>
                <td class="date-location">Nov 2022 – Present | Remote & On-Site</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: Generative AI Architecture, Prompt Optimization, Custom Agentic Systems, Enterprise LLM Integrations</div>
        <ul class="entry-bullets">
            <li>Deliver specialized technical consulting on generative AI architecture, prompt engineering optimization, and custom LLM integrations for enterprise and mid-market clients, including the <strong>Telefónica Movistar Foundation</strong>, <strong>Universidad Francisco Marroquín</strong>, and <strong>Wundermann Thompson Miami</strong>.</li>
            <li>Architected and implemented multi-agent workflows using LangChain, LangGraph, and CrewAI, establishing robust agent-to-agent (A2A) communications that drastically reduced manual operational steps.</li>
            <li>Achieved documented client outcomes including up to a <strong>46% increase in team productivity</strong> and a <strong>66% reduction in monthly infrastructure</strong> and cloud operational overhead through optimized LLM utilization and precise prompt structures.</li>
        </ul>
    </div>

    <div class="page-break"></div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Director of Innovation</span> <span class="company">- TRADEBOG S.A.S.</span></td>
                <td class="date-location">Dec 2020 – Jun 2023 | Bogotá, Colombia (On-Site)</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Directed full-stack development and technical product roadmap for Colombia’s leading dropshipping and e-commerce platform.</li>
            <li>Optimized complex transactional backend workflows and integrated programmatic data-driven pipelines to support high-concurrency purchase funnels.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Operations Director</span> <span class="company">- FreshWorks | Ideas Frescas</span></td>
                <td class="date-location">May 2014 – Jun 2023 | Mexico, Colombia, Spain</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Managed technical delivery, web architectures, and custom database integrations for enterprise clients including <strong>Grupo Herdez</strong> and <strong>El Corte Inglés</strong>.</li>
            <li>Led cross-functional international teams in delivering digital products, custom CMS architectures, and enterprise UI/UX engineering projects.</li>
        </ul>
    </div>

    <h2>Education & Certifications</h2>
    <table class="education-table">
        <tr>
            <td>
                <span class="degree-title">Generative AI for Business: Driving Growth and Competitive Advantage</span><br>
                <span class="institution-name">University of Toronto</span><br>
                <span class="edu-focus">Focus: AI strategy, innovation, ethics, decision-making, governance, and organizational transformation.</span>
            </td>
            <td class="edu-meta">Dec 2022 – Feb 2023<br>Certified Diploma (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Prompt Engineer with Emphasis on ChatGPT</span><br>
                <span class="institution-name">Platzi</span><br>
                <span class="edu-focus">Focus: Advanced prompt structures, extension and plugin integrations, LLM constraints, and hallucination reduction.</span>
            </td>
            <td class="edu-meta">Feb 2023 – Apr 2023<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Social Network Analysis: Digital Communication & Contents</span><br>
                <span class="institution-name">University of Michigan</span><br>
                <span class="edu-focus">Skills: Algorithmic Communication, Data analysis, and social network strategies.</span>
            </td>
            <td class="edu-meta">Sep 2013 – Dec 2013<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Bachelor's Degree in Advertising and Marketing</span><br>
                <span class="institution-name">Universidad Central</span><br>
                <span class="edu-focus">Focus: Creative direction, strategic messaging, and art direction.</span>
            </td>
            <td class="edu-meta">Feb 2002 – Nov 2007<br>Professional Degree (On-Site)</td>
        </tr>
    </table>

    <h2>Languages & Interests</h2>
    <div style="font-size: 8pt; margin-bottom: 2px;">
        <strong>Languages:</strong> Spanish (Native) <span class="contact-sep">|</span> English (Full Professional & Technical Proficiency)
    </div>
    <div style="font-size: 8pt;">
        <strong>Interests:</strong> Generative AI Research, Multi-Agent Systems, Machine Learning Ethics, Blogging, Technical Mentoring.
    </div>

    <div class="portfolio-box">
        To view my full portfolio of work, featured projects, case studies, and services, please visit:<br>
        <strong><a href="https://juanjaramillo.tech">juanjaramillo.tech</a></strong>
    </div>

</body>
</html>
"""

# =========================================================================
# 2. Vibe Coding & AI-Native Engineering Resume
# =========================================================================
vibe_coding_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Juan Miguel Jaramillo Gaviria - AI-Native Full-Stack Architect (Vibe Coding)</title>
<style>{css_styles}</style>
</head>
<body>

    <div class="header">
        <div class="name">Juan Miguel Jaramillo Gaviria</div>
        <div class="tagline">AI-Native Full-Stack Architect | Vibe Coder | Product Engineer</div>
        <div class="contact-info">
            Bogotá, Colombia <span class="contact-sep">|</span> 
            <a href="mailto:juanamillo@proton.me">juanamillo@proton.me</a> <span class="contact-sep">|</span> 
            +57 305 420 6139 <span class="contact-sep">|</span> 
            <a href="https://juanjaramillo.tech">juanjaramillo.tech</a> <span class="contact-sep">|</span> 
            <a href="https://www.linkedin.com/in/juan-jaramillo-ai">LinkedIn</a>
        </div>
    </div>

    <h2>Professional Summary</h2>
    <div class="summary-text">
        Pioneering AI-Native Full-Stack Architect with over 17 years of leadership experience, specializing in the modern "vibe coding" paradigm. Master of high-velocity, spec-first AI engineering workflows leveraging modern AI IDEs (Cursor, Copilot) and multi-agent execution systems to design, build, and deploy production-grade software ecosystems at 10x traditional speed. Renowned for shipping scalable, secure, and revenue-generating SaaS platforms by translating plain-text design specifications into robust, production-grade architectures. Deeply proficient across Next.js 15/16, React 19, Astro 5, Tailwind CSS v4, TypeScript, Python, and Google Cloud Platform.
    </div>

    <h2>Core Proficiencies & Technical Expertise</h2>
    <table class="skills-table">
        <tr>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">Vibe Coding & AI Workflows:</span>
                    <span class="skills-items">Cursor AI IDE, Spec-First AI Builds, Structured Prompts, Code Synthesis, Prompt-Driven Rapid Prototyping, AI-Driven Refactoring, Agentic Code Generation.</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">AI Stack & Agentic Frameworks:</span>
                    <span class="skills-items">Gemini 2.5 Flash, Vertex AI, LangChain, LangGraph, CrewAI, n8n Automation, Vector Databases, Prompt Versioning with Git Flow.</span>
                </div>
            </td>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">AI-Native Full-Stack Engineering:</span>
                    <span class="skills-items">TypeScript, JavaScript, ReactJS/React 19, Next.js 15/16, Astro 5, Tailwind CSS v4, Python (Core), Node.js, SQL, PostgreSQL, Supabase, Legacy WordPress (15+ yrs).</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">Infrastructure & CI/CD:</span>
                    <span class="skills-items">Google Cloud Platform (Cloud Run, Cloud Armor, BigQuery), Supabase, Docker, Vercel, PM2, Git, GitHub Actions.</span>
                </div>
            </td>
        </tr>
    </table>

    <h2>Professional Experience</h2>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">AI Development Lead</span> <span class="company">- TopNetworks Inc.</span></td>
                <td class="date-location">Feb 2025 – Jun 2026 | Remote / Bogotá, Colombia</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: Vibe Coding Workflow, Cursor IDE, Spec-First Synthesis, Multi-Agent Orchestration, Production-Grade Deployments</div>
        <ul class="entry-bullets">
            <li>Spearheaded AI engineering strategy and full-stack architecture, shifting development entirely to an AI-native paradigm.</li>
            <li>Architected, vibe-coded, and launched TopNetworks' entire proprietary internal SaaS ecosystem from plain-text specifications, achieving extraordinary shipping velocity and direct-to-production deployment:
                <ul>
                    <li><strong>EmailGenius:</strong> High-throughput AI email generation engine engineered with Vertex AI, Next.js 15/16, React 19, and PostgreSQL; fully synthesized and iterated in record time using Cursor IDE.</li>
                    <li><strong>RouteGenius:</strong> High-concurrency traffic routing engine on Supabase; integrates multi-agent n8n workflows via concurrent webhooks. Vibe-coded to process high volumes of live web traffic with zero latency.</li>
                    <li><strong>TrafficGenius:</strong> Real-time invalid traffic detection and security platform using BigQuery and Cloud Armor; optimized using AI-assisted query design.</li>
                    <li><strong>Social Media Genius:</strong> AI-driven content generation app with an interactive canvas editor; build accelerated by AI-native frontend tooling (Tailwind CSS v4).</li>
                </ul>
            </li>
            <li>Maintained strict engineering discipline: paired rapid vibe coding with structured Git Flow versioning, comprehensive automated prompt validation, and rigorous architectural checks.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Prompt Engineer & AI Consultant</span> <span class="company">- Juan Jaramillo (Independent Practice)</span></td>
                <td class="date-location">Nov 2022 – Present | Remote & On-Site</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: AI Developer Experience (DevEx), Cursor IDE Mentoring, High-Velocity Workflows, AI-Assisted Architecture</div>
        <ul class="entry-bullets">
            <li>Advise enterprise and mid-market organizations on adopting AI-native development workflows, including training developer teams on Cursor IDE, structured code-generation prompting, and spec-first software design.</li>
            <li>Consulted for the <strong>Telefónica Movistar Foundation</strong>, <strong>Universidad Francisco Marroquín</strong>, and <strong>Wundermann Thompson Miami</strong>, establishing custom-designed rapid-prototyping environments.</li>
            <li>Delivered outstanding operational results, accelerating client product development cycles by up to 10x, driving a <strong>46% increase in overall team productivity</strong>, and reducing hosting and API infrastructure overhead by <strong>66%</strong>.</li>
        </ul>
    </div>

    <div class="page-break"></div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Director of Innovation</span> <span class="company">- TRADEBOG S.A.S.</span></td>
                <td class="date-location">Dec 2020 – Jun 2023 | Bogotá, Colombia (On-Site)</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Led technical product direction and rapid full-stack engineering for Colombia's top dropshipping and e-commerce network.</li>
            <li>Pioneered low-code and early rapid-development integrations to streamline high-throughput transaction routing and inventory updates.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Operations Director</span> <span class="company">- FreshWorks | Ideas Frescas</span></td>
                <td class="date-location">May 2014 – Jun 2023 | Mexico, Colombia, Spain</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Managed technical delivery, rapid web builds, and agile client transformation roadmaps across three countries.</li>
            <li>Deployed highly optimized custom architectures for enterprise clients, leveraging rapid template iteration and modular component development.</li>
        </ul>
    </div>

    <h2>Education & Certifications</h2>
    <table class="education-table">
        <tr>
            <td>
                <span class="degree-title">Generative AI for Business: Driving Growth and Competitive Advantage</span><br>
                <span class="institution-name">University of Toronto</span><br>
                <span class="edu-focus">Focus: AI strategy, innovation, ethical AI frameworks, governance, and rapid organizational adaptation.</span>
            </td>
            <td class="edu-meta">Dec 2022 – Feb 2023<br>Certified Diploma (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Prompt Engineer with Emphasis on ChatGPT</span><br>
                <span class="institution-name">Platzi</span><br>
                <span class="edu-focus">Focus: Advanced prompt structures, extension and plugin integrations, business use cases, and LLM constraints.</span>
            </td>
            <td class="edu-meta">Feb 2023 – Apr 2023<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Social Network Analysis: Digital Communication & Contents</span><br>
                <span class="institution-name">University of Michigan</span><br>
                <span class="edu-focus">Skills: Network dynamics, algorithmic content distribution, and strategic digital messaging.</span>
            </td>
            <td class="edu-meta">Sep 2013 – Dec 2013<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Bachelor's Degree in Advertising and Marketing</span><br>
                <span class="institution-name">Universidad Central</span><br>
                <span class="edu-focus">Focus: Creative direction, art direction, copywriting strategy, and campaign design.</span>
            </td>
            <td class="edu-meta">Feb 2002 – Nov 2007<br>Professional Degree (On-Site)</td>
        </tr>
    </table>

    <h2>Languages & Interests</h2>
    <div style="font-size: 8pt; margin-bottom: 2px;">
        <strong>Languages:</strong> Spanish (Native) <span class="contact-sep">|</span> English (Full Professional & Technical Proficiency)
    </div>
    <div style="font-size: 8pt;">
        <strong>Interests:</strong> Vibe Coding Research, Rapid Prototyping, DevEx Optimization, Blogging, Tech Mentorship.
    </div>

    <div class="portfolio-box">
        To view my full portfolio of work, featured projects, case studies, and services, please visit:<br>
        <strong><a href="https://juanjaramillo.tech">juanjaramillo.tech</a></strong>
    </div>

</body>
</html>
"""

# =========================================================================
# 3. CMS + React/Next.js Architecture Resume
# =========================================================================
cms_react_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Juan Miguel Jaramillo Gaviria - CMS & Full-Stack Architect Resume</title>
<style>{css_styles}</style>
</head>
<body>

    <div class="header">
        <div class="name">Juan Miguel Jaramillo Gaviria</div>
        <div class="tagline">CMS & Full-Stack Architect | Headless Next.js Specialist | WordPress Expert</div>
        <div class="contact-info">
            Bogotá, Colombia <span class="contact-sep">|</span> 
            <a href="mailto:juanamillo@proton.me">juanamillo@proton.me</a> <span class="contact-sep">|</span> 
            +57 305 420 6139 <span class="contact-sep">|</span> 
            <a href="https://juanjaramillo.tech">juanjaramillo.tech</a> <span class="contact-sep">|</span> 
            <a href="https://www.linkedin.com/in/juan-jaramillo-ai">LinkedIn</a>
        </div>
    </div>

    <h2>Professional Summary</h2>
    <div class="summary-text">
        High-impact Full-Stack Web Architect with a rare combination of over 15 years of deep WordPress and CMS engineering layered with cutting-edge React 19, Next.js 15/16, and Astro 5 architectures. Recognized expert in monolithic legacy modernization, successfully executing decoupled, headless migrations that optimize web speed, Core Web Vitals, and SEO discovery layers. Expert in designing high-concurrency routing architectures, custom WordPress theme/plugin development, Tailwind CSS v4, and integrating custom generative AI workflows directly into CMS ecosystems to maximize content velocity and monetization.
    </div>

    <h2>Core Proficiencies & Technical Expertise</h2>
    <table class="skills-table">
        <tr>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">CMS & WordPress Engineering:</span>
                    <span class="skills-items">WordPress (15+ Years Core, Themes, Plugins), Headless/Decoupled CMS, Monolith Modernization, REST APIs, GraphQL, WooCommerce, PHP (Advanced).</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">Modern Frontend Stack:</span>
                    <span class="skills-items">React 19, Next.js 15/16, Astro 5, Tailwind CSS v4, HTML5, CSS3/SASS, TypeScript, JavaScript (ES6+), UI/UX Engineering.</span>
                </div>
            </td>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">Backend, Cloud & Databases:</span>
                    <span class="skills-items">Node.js, Python, Supabase, Google Cloud Platform (Cloud Run, Cloud Armor, BigQuery), PostgreSQL, SQL, PM2, Docker, Git.</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">Performance & AI Integration:</span>
                    <span class="skills-items">Core Web Vitals Optimization, Cloudflare/CDN, n8n Automation, Prompt Engineering for Content CMS, Gemini 2.5 Flash, Cursor AI.</span>
                </div>
            </td>
        </tr>
    </table>

    <h2>Professional Experience</h2>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">AI Development & Full-Stack Architect Lead</span> <span class="company">- TopNetworks Inc.</span></td>
                <td class="date-location">Feb 2025 – Jun 2026 | Remote / Bogotá, Colombia</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: Decoupled & Headless Frontends, Next.js 15/16, React 19, Astro 5, High-Concurrency Web Architectures, Tailwind v4</div>
        <ul class="entry-bullets">
            <li>Directed full-stack web architectures and content modernization strategy for digital publishing platforms serving the US, UK, Mexico, and LATAM markets.</li>
            <li>Designed and deployed high-performance front-end applications built on React 19, Next.js 15/16, Astro 5, and Tailwind CSS v4, connected to decoupled API gateways:
                <ul>
                    <li><strong>RouteGenius:</strong> Built a high-concurrency traffic routing engine on Supabase with a custom-developed Next.js front-end, dynamically managing traffic distribution across diverse marketing discovery layers and CMS nodes.</li>
                    <li><strong>EmailGenius:</strong> React 19 interactive generative email interface utilizing Vertex AI and PostgreSQL backends.</li>
                    <li><strong>Social Media Genius:</strong> AI-driven content generation app incorporating a highly interactive Next.js 15 canvas editor and customized CSS styling.</li>
                    <li><strong>TrafficGenius:</strong> Security platform leveraging BigQuery and Cloud Armor with real-time Next.js reporting dashboards.</li>
                </ul>
            </li>
            <li>Successfully migrated high-traffic monolithic publishing architectures to headless Astro 5 and Next.js, yielding dramatic improvements in site load times, Core Web Vitals, and SEO-driven organic traffic.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Prompt Engineer & AI-CMS Consultant</span> <span class="company">- Juan Jaramillo (Independent Practice)</span></td>
                <td class="date-location">Nov 2022 – Present | Remote & On-Site</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: CMS Legacy Modernization, Headless Next.js Migrations, AI-Assisted Editorial Workflows</div>
        <ul class="entry-bullets">
            <li>Consult with mid-market agencies and enterprise clients—including the <strong>Telefónica Movistar Foundation</strong>, <strong>Universidad Francisco Marroquín</strong>, and <strong>Wundermann Thompson Miami</strong>—on CMS modernization, WordPress migrations to headless Astro/Next.js stacks, and custom AI content generation integrations.</li>
            <li>Designed and built custom REST/GraphQL API connectors bridging legacy WordPress backends with ultra-fast modern frontend React frameworks.</li>
            <li>Drove major client operational and performance improvements, including up to a <strong>46% increase in editorial team productivity</strong> and a <strong>66% reduction in web hosting overhead</strong> via serverless web architecture.</li>
        </ul>
    </div>

    <div class="page-break"></div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Director of Innovation</span> <span class="company">- TRADEBOG S.A.S.</span></td>
                <td class="date-location">Dec 2020 – Jun 2023 | Bogotá, Colombia (On-Site)</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Led technical product development and full-stack engineering for Colombia’s leading dropshipping and e-commerce platform.</li>
            <li>Engineered custom WooCommerce API endpoints, transactional database schemas, and digital acquisition channels to support tens of thousands of daily active users.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Operations Director / WordPress Architect</span> <span class="company">- FreshWorks | Ideas Frescas</span></td>
                <td class="date-location">May 2014 – Jun 2023 | Mexico, Colombia, Spain</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Spent over 9 years architecting custom WordPress-based systems, custom plugins, and custom themes for world-renowned brands such as <strong>Grupo Herdez</strong> and <strong>El Corte Inglés</strong>.</li>
            <li>Managed multi-country cross-functional teams in digital agency execution, from deep PHP-backend customizations to advanced frontend UI/UX integrations.</li>
            <li>Designed scalable web publishing networks and automated content syndication pipelines for enterprise-level CMS installations.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Project Manager / WordPress Developer</span> <span class="company">- La Quinta P Digital Agency</span></td>
                <td class="date-location">Aug 2009 – Oct 2012 | Bogotá, Colombia</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Led digital project design, custom WordPress theme development, PHP customizations, and front-end CSS/HTML implementations for regional SME clients.</li>
        </ul>
    </div>

    <h2>Education & Certifications</h2>
    <table class="education-table">
        <tr>
            <td>
                <span class="degree-title">Generative AI for Business: Driving Growth and Competitive Advantage</span><br>
                <span class="institution-name">University of Toronto</span><br>
                <span class="edu-focus">Focus: AI integration strategies, innovation ethics, governance, and business-focused tech transitions.</span>
            </td>
            <td class="edu-meta">Dec 2022 – Feb 2023<br>Certified Diploma (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Prompt Engineer with Emphasis on ChatGPT</span><br>
                <span class="institution-name">Platzi</span><br>
                <span class="edu-focus">Focus: Custom prompt structures, CMS integrations, and automated content pipelines.</span>
            </td>
            <td class="edu-meta">Feb 2023 – Apr 2023<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Social Network Analysis: Digital Communication & Contents</span><br>
                <span class="institution-name">University of Michigan</span><br>
                <span class="edu-focus">Skills: Network analysis, digital communications, and social discovery algorithms.</span>
            </td>
            <td class="edu-meta">Sep 2013 – Dec 2013<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Bachelor's Degree in Advertising and Marketing</span><br>
                <span class="institution-name">Universidad Central</span><br>
                <span class="edu-focus">Focus: Creative direction, art direction, and consumer messaging strategies.</span>
            </td>
            <td class="edu-meta">Feb 2002 – Nov 2007<br>Professional Degree (On-Site)</td>
        </tr>
    </table>

    <h2>Languages & Interests</h2>
    <div style="font-size: 8pt; margin-bottom: 2px;">
        <strong>Languages:</strong> Spanish (Native) <span class="contact-sep">|</span> English (Full Professional & Technical Proficiency)
    </div>
    <div style="font-size: 8pt;">
        <strong>Interests:</strong> Headless Web Paradigms, Frontend Performance, Blogging, UI/UX Design, Technical Mentorship.
    </div>

    <div class="portfolio-box">
        To view my full portfolio of work, featured projects, case studies, and services, please visit:<br>
        <strong><a href="https://juanjaramillo.tech">juanjaramillo.tech</a></strong>
    </div>

</body>
</html>
"""

# Dict to compile
resumes_to_generate = {
    "Juan_Jaramillo_Resume_AI_LLM.pdf": ai_llm_html,
    "Juan_Jaramillo_Resume_Vibe_Coding.pdf": vibe_coding_html,
    "Juan_Jaramillo_Resume_CMS_React.pdf": cms_react_html
}

print("Starting generation...")
for filename, html_content in resumes_to_generate.items():
    filepath = os.path.join(working_dir, filename)
    success = generate_pdf(html_content, filepath)
    if success:
        print(f"Successfully generated {filename}")
        # Verify page count
        reader = pypdf.PdfReader(filepath)
        print(f"  Page count for {filename}: {len(reader.pages)}")
        for i, page in enumerate(reader.pages):
            print(f"    Page {i+1} character count: {len(page.extract_text())}")
    else:
        print(f"Failed to generate {filename}")
