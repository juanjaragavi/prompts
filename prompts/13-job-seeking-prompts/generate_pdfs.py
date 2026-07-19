import sys
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

# Optimized Resume HTML (targeting exactly 2 pages)
resume_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Juan Miguel Jaramillo Gaviria - Master Resume</title>
<style>
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
</style>
</head>
<body>

    <div class="header">
        <div class="name">Juan Miguel Jaramillo Gaviria</div>
        <div class="tagline">AI-Native Full-Stack Architect | AI Development Lead | Tech Entrepreneur</div>
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
        Enterprise AI Development Lead and Full-Stack Architect with over 17 years of leadership experience spanning digital transformation, software engineering, and technology entrepreneurship. Expert in designing and deploying production-grade generative AI systems, orchestrating multi-agent frameworks, executing LLM fine-tuning (PEFT, RLHF), and managing hallucination risk. Highly proficient across Next.js 15/16, React 19, TypeScript, Python, and cloud-native architectures on Google Cloud Platform. Well before generative AI reshaped the global tech landscape, founded and scaled multiple successful digital and technology ventures. A pioneer in combining modern legacy-modernization expertise (CMS/WordPress) with AI-assisted high-velocity coding workflows.
    </div>

    <h2>Core Proficiencies & Technical Expertise</h2>
    <table class="skills-table">
        <tr>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">AI & Machine Learning:</span>
                    <span class="skills-items">LLM Fine-Tuning (PEFT, RLHF), Advanced Prompt Engineering, Hallucination Risk Mitigation, Prompt Versioning (Git Flow), RAG Pipelines, Vector Databases.</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">AI Frameworks & Tools:</span>
                    <span class="skills-items">LangChain, LangGraph, CrewAI, Vertex AI Agent-to-Agent (A2A), n8n Workflow Automation, Gemini 2.5 Flash, Cursor AI IDE.</span>
                </div>
            </td>
            <td>
                <div class="skills-category">
                    <span class="skills-category-title">Full-Stack Software Engineering:</span>
                    <span class="skills-items">TypeScript, JavaScript, ReactJS/React 19, Next.js 15/16, Astro 5, Node.js, Python, SQL, WordPress Legacy Architecture (15+ years).</span>
                </div>
                <div class="skills-category" style="margin-top: 2px;">
                    <span class="skills-category-title">Cloud & Infrastructure:</span>
                    <span class="skills-items">Google Cloud Platform (Cloud Run, Cloud Armor, BigQuery, Compute), Supabase, PostgreSQL, Docker, Vercel, PM2, Git.</span>
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
        <div class="focus-text">Key Focus: Prompt Engineering, Hallucination Risk Management, GenAI Prompt Versioning with Git Flow, High-velocity AI-Native Workflows</div>
        <ul class="entry-bullets">
            <li>Spearheaded AI engineering strategy and full-stack architecture for high-performance publishing platforms serving markets across the US, UK, Mexico, and Latin America.</li>
            <li>Designed, built, and launched a core proprietary internal SaaS ecosystem leveraging rapid, spec-first, AI-native workflows (such as Cursor, agentic coding, and advanced prompt-driven rapid iteration):
                <ul>
                    <li><strong>EmailGenius:</strong> Scalable, high-throughput AI email generation engine engineered with Vertex AI and PostgreSQL.</li>
                    <li><strong>TrafficGenius:</strong> Real-time invalid traffic detection and security intelligence platform utilizing BigQuery and Cloud Armor.</li>
                    <li><strong>RouteGenius:</strong> High-concurrency probabilistic traffic routing distribution engine built on Supabase, featuring multi-agent workflow integration in n8n via webhooks to automate traffic optimization.</li>
                    <li><strong>Social Media Genius:</strong> AI-driven social content generation application featuring a custom interactive canvas editor.</li>
                </ul>
            </li>
            <li>Managed prompt versioning via Git Flow, structured hallucination risk frameworks, and deployed all services using Next.js 15/16, TypeScript, React 19, Astro 5, Tailwind v4, and Gemini 2.5 Flash on GCP.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Prompt Engineer & AI Consultant</span> <span class="company">- Juan Jaramillo (Independent Practice)</span></td>
                <td class="date-location">Nov 2022 – Present | Remote & On-Site</td>
            </tr>
        </table>
        <div class="focus-text">Key Focus: Prompt Engineering & Optimization, LLM Fundamentals, Hallucination Mitigation, UI/UX Design workflows</div>
        <ul class="entry-bullets">
            <li>Deliver specialized technical consulting on generative AI architecture, prompt engineering optimization, and custom LLM integrations for mid-market and enterprise clients, including the <strong>Telefónica Movistar Foundation</strong>, <strong>Universidad Francisco Marroquín (Guatemala)</strong>, and <strong>Wundermann Thompson Miami</strong>.</li>
            <li>Architect and build front-end and back-end environments for custom AI applications while directly managing UI/UX design workflows.</li>
            <li>Achieved documented client outcomes including up to a <strong>46% increase in operational productivity</strong> and a <strong>66% reduction in monthly infrastructure</strong> and operational overhead.</li>
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
            <li>Oversaw full-stack development, UI/UX systems, and technical product direction for Colombia’s leading dropshipping and e-commerce platform.</li>
            <li>Designed and optimized complex digital advertising architectures, social media acquisition pipelines, and transactional backend workflows.</li>
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
            <li>Managed technical delivery, web architecture, and custom WordPress development for enterprise brands including <strong>Grupo Herdez</strong> and <strong>El Corte Inglés</strong>.</li>
            <li>Led cross-functional teams across three countries, managing digital product design, UI/UX engineering, and client transformation roadmaps.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Project Director</span> <span class="company">- 2W Agencia Digital</span></td>
                <td class="date-location">Nov 2012 – Jan 2014 | Bogotá, Colombia</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Digital project director, key accounts director, digital strategist, and digital marketing specialist.</li>
        </ul>
    </div>

    <div class="entry">
        <table class="entry-header-table">
            <tr>
                <td><span class="job-title">Co-founder & Project Manager</span> <span class="company">- La Quinta P Digital Agency</span></td>
                <td class="date-location">Aug 2009 – Oct 2012 | Bogotá, Colombia</td>
            </tr>
        </table>
        <ul class="entry-bullets">
            <li>Digital project director, digital marketing specialist, web designer, and custom WordPress developer.</li>
        </ul>
    </div>

    <h2>Education & Certifications</h2>
    <table class="education-table">
        <tr>
            <td>
                <span class="degree-title">Generative AI for Business: Driving Growth and Competitive Advantage</span><br>
                <span class="institution-name">University of Toronto</span><br>
                <span class="edu-focus">Focus: AI strategy, innovation, ethics, decision-making, governance, and organizational transformation, with case studies from major companies.</span>
            </td>
            <td class="edu-meta">Dec 2022 – Feb 2023<br>Certified Diploma (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Prompt Engineer with Emphasis on ChatGPT</span><br>
                <span class="institution-name">Platzi</span><br>
                <span class="edu-focus">Focus: Advanced prompt structures, extension and plugin integrations, business use cases, and ethical LLM constraints.</span>
            </td>
            <td class="edu-meta">Feb 2023 – Apr 2023<br>Certified Course (Remote)</td>
        </tr>
        <tr>
            <td>
                <span class="degree-title">Social Network Analysis: Digital Communication & Contents</span><br>
                <span class="institution-name">University of Michigan</span><br>
                <span class="edu-focus">Skills: Digital Marketing, Content Strategy.</span>
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
        <strong>Interests:</strong> Golf, Reading, Film, Music, Blogging, Writing, Technical Consulting, and Teaching.
    </div>

    <div class="portfolio-box">
        To view my full portfolio of work, featured projects, case studies, and services, please visit:<br>
        <strong><a href="https://juanjaramillo.tech">juanjaramillo.tech</a></strong>
    </div>

</body>
</html>
"""

# Optimized Cover Letter HTML (targeting exactly 1 page)
cover_letter_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Juan Miguel Jaramillo Gaviria - Master Cover Letter</title>
<style>
    @page {
        size: letter;
        margin: 10mm 15mm 10mm 15mm;
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2d3748;
        line-height: 1.35;
        font-size: 8.8pt;
    }
    a {
        color: #1e3a8a;
        text-decoration: none;
    }
    .header {
        text-align: center;
        margin-bottom: 8px;
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
    .letter-date {
        margin-bottom: 6px;
        font-size: 8.8pt;
        font-weight: bold;
        color: #1a202c;
    }
    .recipient {
        margin-bottom: 8px;
        font-size: 8.8pt;
        line-height: 1.3;
    }
    .salutation {
        margin-bottom: 6px;
        font-weight: bold;
    }
    p {
        text-align: justify;
        margin-top: 0;
        margin-bottom: 8px;
    }
    .section-title {
        font-weight: bold;
        color: #1e3a8a;
        margin-top: 8px;
        margin-bottom: 3px;
        font-size: 9pt;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-left: 2px solid #1e3a8a;
        padding-left: 6px;
    }
    .closing {
        margin-top: 10px;
        margin-bottom: 12px;
    }
    .signature-block {
        line-height: 1.3;
        font-size: 8.5pt;
    }
</style>
</head>
<body>

    <div class="header">
        <div class="name">Juan Miguel Jaramillo Gaviria</div>
        <div class="tagline">AI-Native Full-Stack Architect | AI Development Lead | Tech Entrepreneur</div>
        <div class="contact-info">
            Bogotá, Colombia <span class="contact-sep">|</span> 
            <a href="mailto:juanamillo@proton.me">juanamillo@proton.me</a> <span class="contact-sep">|</span> 
            +57 305 420 6139 <span class="contact-sep">|</span> 
            <a href="https://juanjaramillo.tech">juanjaramillo.tech</a> <span class="contact-sep">|</span> 
            <a href="https://www.linkedin.com/in/juan-jaramillo-ai">LinkedIn</a>
        </div>
    </div>

    <div class="letter-date">July 8, 2026</div>

    <div class="recipient">
        <strong>To:</strong> Hiring Team / Talent Acquisition<br>
        <strong>Re:</strong> Application for AI Engineering Leadership / Full-Stack Architect Role
    </div>

    <div class="salutation">Dear Hiring Team,</div>

    <p>I am writing to express my strong interest in joining your team as an AI Engineering leader. Bringing over 17 years of technical execution and entrepreneurial leadership, I specialize in navigating the space between abstract generative AI concepts and scalable, production-grade architectures. I offer your organization a rare combination of strategic vision and full-stack engineering depth.</p>

    <div class="section-title">A Career Built Around AI-Native Thinking</div>
    <p>My career has been defined by an early adoption of emerging technology paradigms. Well before generative AI reshaped the global tech landscape, I founded and scaled multiple successful digital and technology ventures—including LaQuintaP, FreshWorks Digital Agency across Europe and LATAM, and TRADEBOG, an industry-leading dropshipping platform in Colombia. This deep entrepreneurial foundation ensures that every AI system I architect is engineered to solve a concrete business problem and drive measurable bottom-line value.</p>

    <div class="section-title">Deep, Production-Proven AI Expertise</div>
    <p>Since 2022, I have focused exclusively on enterprise-grade generative AI development, LLM fine-tuning (PEFT, RLHF), advanced prompt engineering, and agentic product design. As the AI Development Lead for TopNetworks Inc., I personally designed, built, and shipped a highly profitable internal SaaS ecosystem:
        <strong>EmailGenius</strong> (high-throughput AI email generation utilizing Vertex AI and PostgreSQL),
        <strong>TrafficGenius</strong> (real-time invalid traffic detection using Google BigQuery and Cloud Armor),
        <strong>RouteGenius</strong> (probabilistic web traffic distribution running on Supabase infrastructure), and
        <strong>Social Media Genius</strong> (an AI-native social content generator complete with an interactive canvas editor).
        These systems are not experimental prototypes; they are highly scalable, revenue-generating platforms built on Next.js 15/16, React 19, Astro 5, TypeScript, and the Gemini 2.5 Flash model deployed on Google Cloud Platform.
    </p>

    <div class="section-title">Advisory Reach and Measurable Impact</div>
    <p>Beyond internal product execution, my technical advisory work for organizations like the Telefónica Movistar Foundation, Universidad Francisco Marroquín, and Wundermann Thompson Miami has delivered definitive operational impacts. My AI implementations have consistently driven up to a 46% increase in team productivity while securing up to a 66% reduction in monthly infrastructure and operational costs.</p>

    <div class="section-title">Advanced Tooling and Agentic Systems</div>
    <p>I possess advanced, production-proven mastery of LangChain, LangGraph, CrewAI, and Vertex AI Agent-to-Agent (A2A) frameworks. Backed by academic credentials in generative AI strategy and ethics from the University of Toronto and applied prompt engineering from Platzi, I write clean, production-grade code across Python, JavaScript/TypeScript, and SQL.</p>

    <p>I view artificial intelligence not as a human replacement, but as an exponential leverage tool. I am eager to bring this exact philosophy, along with my full-stack execution capabilities, to your organization. Thank you for your time and consideration; I welcome the opportunity for a technical interview.</p>

    <div class="closing">
        Warm regards,
    </div>

    <div class="signature-block">
        <strong>Juan Miguel Jaramillo Gaviria</strong><br>
        AI Development Lead | Full-Stack Architect | Generative AI Specialist<br>
        <a href="mailto:juanamillo@proton.me">juanamillo@proton.me</a> | +57 305 420 6139 | <a href="https://juanjaramillo.tech">juanjaramillo.tech</a>
    </div>

</body>
</html>
"""

# Compile and check pages
resume_path = os.path.join(working_dir, "Juan_Jaramillo_Master_Resume.pdf")
cover_letter_path = os.path.join(working_dir, "Juan_Jaramillo_Master_Cover_Letter.pdf")

generate_pdf(resume_html, resume_path)
generate_pdf(cover_letter_html, cover_letter_path)

reader_r = pypdf.PdfReader(resume_path)
reader_cl = pypdf.PdfReader(cover_letter_path)

print(f"RESUME: {len(reader_r.pages)} pages")
for i, page in enumerate(reader_r.pages):
    print(f"  Page {i+1} size: {len(page.extract_text())} chars")

print(f"COVER LETTER: {len(reader_cl.pages)} pages")
for i, page in enumerate(reader_cl.pages):
    print(f"  Page {i+1} size: {len(page.extract_text())} chars")
