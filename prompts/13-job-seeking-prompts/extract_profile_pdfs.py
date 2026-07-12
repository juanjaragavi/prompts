from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit(f"pypdf is required: {exc}")

workspace = Path("/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts")
pdfs = [
    workspace / ".agent/skills/recruiter-outreach-response/01 Juan_Jaramillo-Curriculum-Vitae-2026.pdf",
    workspace / ".agent/skills/recruiter-outreach-response/01 Juan Jaramillo Cover Letter 2026.pdf",
    workspace / ".agent/skills/recruiter-outreach-response/01 JUAN JARAMILLO Corporate Presentation.pdf",
]
out_dir = workspace / "terminal_logs/profile_pdf_text"
out_dir.mkdir(parents=True, exist_ok=True)
for pdf in pdfs:
    reader = PdfReader(str(pdf))
    text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
    output = out_dir / f"{pdf.name}.txt"
    output.write_text(text, encoding="utf-8")
    print(f"{pdf.name}: {len(reader.pages)} pages, {len(text)} chars -> {output}")
