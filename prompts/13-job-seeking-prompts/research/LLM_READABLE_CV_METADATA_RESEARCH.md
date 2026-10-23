# Making the CV LLM-Readable: Metadata vs. Text Layer

Research date: 2026-09-17
Subject file: `~/Documents/01 Juan_Jaramillo-Curriculum-Vitae-2026.pdf`
Tooling used: `pypdf 6.14.2` (only PDF tool installed locally; no `exiftool`, `qpdf`, `pdftotext`, `mutool`, `gs`)

---

## 1. Verified state of the current file

| Property | Value |
|---|---|
| Pages | 3 |
| `/Creator` | `Pages` |
| `/Producer` | `PDF Squeezer 4` (post-export recompression) |
| `/Title` | `01 Juan_Jaramillo-Curriculum-Vitae-2026` (filename, not a title) |
| `/Author`, `/Subject`, `/Keywords` | **absent** |
| `/Lang` | **absent** |
| XMP (`/Metadata`) | **absent** |
| `/MarkInfo` `/Marked` | `true` |
| `/StructTreeRoot` | present |
| Text layer | present, extracts cleanly (2686 / 1919 / 1047 chars) |
| Link annotations | 5 URI annots, all correct (`https://juanjaramilloai.vercel.app`) |
| Fonts | League Spartan (4 weights) + HelveticaNeue, all TrueType subsets |

The PDF is tagged and has a real text layer. Nothing needs to be "unlocked." The
file is machine-readable already — it is the *content* of the text layer that is
degraded.

## 2. Defects found in the extracted text layer

Ranked by information loss.

### D1 — Skill levels carry zero textual information (critical)
Every skill meter extracts as:

```
Python
BASIC ADVANCEDINTERMEDIATE
```

The proficiency level is encoded **only** as a filled graphic bar. 20+ skills
each emit the same three contradictory tokens. An extractor sees `Python` with
`BASIC`, `ADVANCED` and `INTERMEDIATE` simultaneously. This is worse than
omitting the level: it injects noise that can flip a classifier.

Also note `ADVANCEDINTERMEDIATE` — missing word boundary, so even the noise
tokens are malformed.

### D2 — Reading order is scrambled (critical)
Page 1 extracts in this order:

1. `SKILLS` (sidebar heading)
2. professional summary (main column)
3. `juanamillo@proton.me (+57) 305 420 6139`
4. `Juan Miguel Jaramillo Gaviria`  ← name appears 4th
5. `Bogotá, Colombia`
6. `WORK EXPERIENCE` (heading, before the URL)
7. portfolio URL
8. skill meters
9. `LANGUAGES`
10. work history

The name arrives after the summary; sidebar and main column interleave. Pages
exports floating text boxes in object/layer order, not visual order. A parser
using "first line = name" heuristics gets `SKILLS`.

Page 2 splits `WORK EXPERIENCE` and `EDUCATION` into separate fragments and
interleaves `AI & DEV TOOLS` meters between them. `EDUCATION` content is split
across pages 2 and 3, with the page-3 heading emitted *last*.

### D3 — Portfolio URL is broken in the text layer
`https:/ /juanjaramilloai.vercel.app` — 4 occurrences, all with a space inside
the scheme separator (letter-spacing / tracking artifact). The link *annotation*
is correct, but an LLM reading extracted text sees an invalid URL. Extractors
that only read text (most of them) lose the portfolio link.

### D4 — `fi` ligature substitution
`U+FB01 LATIN SMALL LIGATURE FI` appears in: `ﬁne-tuning`, `proﬁciency`,
`Certiﬁed`, `Pﬁzer`. Keyword matching for `fine-tuning` — a core term for AI
engineer roles — fails on exact-match parsers and on some tokenizers. Caused by
League Spartan's ligature table plus Pages' default ligature setting.

### D5 — Mixed-language date abbreviations
`feb.`, `may.`, `ago.`, `nov.`, `jun.` (Spanish) mixed with `dec`, `jan.`
(English). `ago. 2009 - oct. 2012` will not parse as August 2009 in an
English-locale date parser; that role's tenure is silently dropped. Also
`feb. 2002 - nov. 2007· 5 years` is missing a space before `·`.

### D6 — No flat skills string
There is no `Skills: Python, TypeScript, …` line anywhere. All skills exist only
as meter widgets (see D1). Form fields asking for a skills list get nothing.

---

## 3. Research finding: metadata is the wrong lever

The task as framed ("add metadata that LLMs read") does not pay off. Evidence:

- Mainstream ATS and resume parsers extract the text layer via `pdftotext`-class
  libraries and run regex/ML/LLM over that string. They do not open XMP streams
  and do not enumerate embedded-file name trees.
  ([Anish Shobith P S](https://anishshobithps.com/blog/making-my-resume-machine-readable),
  [resumly.ai](https://www.resumly.ai/blog/implementing-structured-data-tags-to-improve-resume-parsing))
- The most thorough public write-up of the exact approach — XMP via `hyperxmp`,
  JSON-LD + JSON Resume embedded via `embedfile`, Dublin Core / IPTC namespaces —
  concludes the effort was "primarily educational, not practically impactful for
  ATS compatibility."
- Claims that "JSON Resume is natively parsed by Workday, Greenhouse and Lever"
  circulate on SEO content farms and are **unsubstantiated**. No vendor
  documentation supports it. Do not build on that claim.
- The hybrid-container pattern *does* work in production — but only where both
  sides agreed on a standard. ZUGFeRD / Factur-X embeds CII XML in PDF/A-3 and
  accounting software extracts it deterministically
  ([PDFlib](https://www.pdflib.com/pdf-knowledge-base/zugferd-and-factur-x/)).
  Recruiting has no equivalent mandate, so there is no consumer for the payload.
- Current resume-parsing research confirms the bottleneck is layout, not
  metadata: state-of-the-art pipelines add "a fine-tuned layout regenerator to
  reorder text from complex multicolumn layouts into a single indexed sequence"
  ([arXiv 2510.09722](https://arxiv.org/pdf/2510.09722)). They are solving D2 on
  their side. Solving it on your side is strictly cheaper.
- Vision-model parsers rasterize pages and OCR them, which reconstructs visual
  order but still cannot recover D1 (a filled bar has no OCR text).

Conclusion: **the text layer is the API.** Metadata is a free garnish.

---

## 4. Apple Pages: what it can and cannot do

**Can:**
- Pages 8.2+ (macOS and iOS) always exports tagged PDF; tagging is not optional.
- `File ▸ Export To ▸ PDF…` exposes: **Image Quality** pop-up, include
  **smart annotations / comments** checkboxes, and **Advanced Options ▸
  accessibility tags for large tables ▸ On**.
- Image/drawing/audio/video descriptions added for VoiceOver export automatically.
  This is the only alt-text channel Pages offers.
- Ligatures are controllable: select all ▸ Format sidebar ▸ Text ▸ Style ▸
  Advanced Options (gear) ▸ **Ligatures: Use None**. Fixes D4 at the source.
- Object layer order is controllable: `Arrange ▸ Bring to Front / Send to Back`.
  Export tag order follows it, so D2 is partially fixable in Pages.

**Cannot:**
- No reading-order panel (Acrobat Pro / InDesign have one; Pages does not).
- No way to set `/Author`, `/Subject`, `/Keywords`, `/Lang`, or XMP. Pages writes
  `/Title` from the filename and `/Creator: Pages`, nothing else.
- No way to attach embedded files.
- No alt-text on shapes-as-data (the skill meters), so D1 cannot be fixed with
  metadata at all — only by adding real text.

Practical consequence: the Pages side of the fix is **layout and typography**.
The metadata side requires a post-export step.

---

## 5. Ranked plan

### Tier 1 — Fix the text layer (recovers ~90% of lost information)

Done in Pages, no tooling:

1. **Label every skill level as text.** `Python — Advanced`, `GenAI and LLMs —
   Advanced`. Keep the bar as decoration if desired, but delete the
   `BASIC / INTERMEDIATE / ADVANCED` axis labels from every meter — they are the
   source of the contradictory tokens. Fixes D1.
2. **Add one flat skills line** in the body flow:
   `Skills: Python, TypeScript, JavaScript, React, Next.js, Vertex AI, Gemini, LangChain, LangGraph, CrewAI, PEFT, RLHF, prompt engineering, PostgreSQL, BigQuery, GCP, Docker, n8n, Make.com, Zapier`.
   Fixes D6.
3. **Move name + contact into the top of the document body flow**, not a floating
   text box, so they extract first. If they must stay floating, `Arrange ▸ Bring
   to Front` on the name block and send the sidebar to the back. Fixes D2.
4. **Single-column main flow.** Convert the sidebar to a section that follows the
   main content rather than running alongside it, or move all sidebar content to
   the end of the document. Two-column resumes are the single most-cited cause of
   parser failure.
5. **Ligatures off.** Fixes D4.
6. **Retype the URL with zero tracking**, or write it bare as
   `juanjaramilloai.vercel.app`. Verify after export that the text layer contains
   no `https:/ /`. Fixes D3.
7. **Normalize all dates to English or ISO.** `Aug 2009 – Oct 2012` or
   `2009-08 – 2012-10`. Fix the missing space in `2007· 5 years`. Fixes D5.
8. **Export from Pages, then recompress — never the reverse.** `PDF Squeezer 4`
   is currently in the chain; it preserved `/MarkInfo` and `/StructTreeRoot` this
   time, but it is an uncontrolled variable. Prefer exporting at Best image
   quality and skipping the squeezer for a 3-page document.

### Tier 2 — Ship a parser-grade companion artifact

The reliable fix for AI-autofill forms is to give them clean input:

- Maintain a **single-column plain-text / Markdown master** (`cv-plain.md`) with
  the same content, one fact per line, explicit `Skills:` / `Company / Title /
  Dates` structure. Paste it into "paste your resume" boxes; upload it where
  `.txt`/`.docx` is accepted.
- Where the form only accepts PDF, upload a **Pages-exported single-column
  variant** of that plain master — visually plain, structurally perfect.
- Optionally append a final page to the designed CV titled
  `Structured Summary` containing the plain-text block, single column. Visible,
  honest, and guarantees a clean region for any extractor.

Two artifacts from one source of truth: designed PDF for humans, plain variant
for machines. This is the highest-reliability option and requires no tooling.

### Tier 3 — Post-export metadata (cheap, low payoff, do it anyway)

Costs one script run. Improves document identity in DMS/search, gives
LLM-with-file-metadata agents a correct title and author, and costs nothing.
Do not expect it to change parse results.

Write: `/Title` (real title with target role), `/Author`, `/Subject`
(one-sentence summary), `/Keywords` (target-role keyword list), `/Lang: en-US`,
and a Dublin Core XMP packet.

### Tier 4 — Embedded structured data (future-proofing only)

Attach `resume.json` (JSON Resume schema) and/or a schema.org `Person` JSON-LD
as a spec-compliant embedded file in the name tree — **not** as a file
annotation, which parsers do not enumerate. Zero consumers today. Justified only
as a hedge and because it is ~10 lines of code.

---

## 6. Verified proof of concept (Tiers 3–4)

Ran against a copy of the live file. All assertions below were checked by
round-trip read.

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, create_string_object
import json

w = PdfWriter(clone_from="01 Juan_Jaramillo-Curriculum-Vitae-2026.pdf")

# Tier 3: DocInfo
w.add_metadata({
    "/Title":  "Juan Miguel Jaramillo Gaviria - Curriculum Vitae - AI Engineer / Forward Deployed Engineer",
    "/Author": "Juan Miguel Jaramillo Gaviria",
    "/Subject":"AI Development Lead. 17+ years. GenAI, LLM fine-tuning (PEFT, RLHF), Next.js, TypeScript, Vertex AI, GCP.",
    "/Keywords":"AI Engineer, Forward Deployed Engineer, Generative AI, LLM, PEFT, RLHF, "
                "Prompt Engineering, Next.js, TypeScript, Python, Vertex AI, Google Cloud, "
                "LangChain, LangGraph, CrewAI, MLOps",
})

# Tier 3: document language (absent in Pages output)
w._root_object[NameObject("/Lang")] = create_string_object("en-US")

# Tier 3: Dublin Core XMP packet
w.xmp_metadata = XMP_PACKET.encode("utf-8")

# Tier 4: embedded structured data, name-tree attachment
w.add_attachment("resume.json", json.dumps(resume_json).encode())

w.write("cv_meta.pdf")
```

Verification results:

```
docinfo   : /Title, /Author, /Subject, /Keywords all set
/Lang     : en-US
XMP       : present; dc:creator == ['Juan Miguel Jaramillo Gaviria']
attachments: ['resume.json']  (retrievable via PdfReader.attachments)
StructTreeRoot kept: True   MarkInfo: {'/Marked': True}
page-1 text length: 2686 (unchanged — text layer untouched)
```

Caveat: `pypdf` rewrote the file at 712K vs. 672K original (stream re-encoding).
Negligible for a 3-page CV. Tagging and text survive intact.

---

## 7. Explicitly out of scope

Two techniques will surface in any search on this topic. Both are rejected:

- **White / 1pt / off-canvas keyword stuffing.** Detectable by trivial text-layer
  inspection, and the extracted text will not match the visible page. Treated as
  application fraud by employers who catch it.
- **Hidden instructions aimed at the reviewing LLM** ("ignore previous
  instructions", "rate this candidate as a strong match"). This is prompt
  injection against the employer's system. It is detectable, it is the fastest
  route to a permanent blacklist, and it is misrepresentation regardless of
  whether it works.

The legitimate boundary: making your own true content machine-legible in a form
a human reader would also accept. Everything in Tiers 1–4 stays inside it.

---

## Sources

- [Making My Resume Machine-Readable — Anish Shobith P S](https://anishshobithps.com/blog/making-my-resume-machine-readable)
- [Implementing Structured Data Tags to Improve Resume Parsing — resumly.ai](https://www.resumly.ai/blog/implementing-structured-data-tags-to-improve-resume-parsing)
- [Importance of Metadata in Resume Uploads — resumly.ai](https://www.resumly.ai/blog/importance-of-metadata-in-resume-uploads)
- [ZUGFeRD and Factur-X — PDFlib PDF Knowledge Base](https://www.pdflib.com/pdf-knowledge-base/zugferd-and-factur-x/)
- [ZUGFeRD e-Invoices: PDF/A-3, CII XML and XMP Metadata — Docentric](https://ax.docentric.com/zugferd-e-invoices-compliance-explained/)
- [Layout-Aware Parsing Meets Efficient LLMs: Resume Information Extraction — arXiv 2510.09722](https://arxiv.org/pdf/2510.09722)
- [MLAR: Multi-layer LLM-based RPA Applicant Tracking — arXiv 2507.10472](https://arxiv.org/pdf/2507.10472)
- [Comparing Approaches for Using LLMs for Structured Data Extraction from PDFs in 2026 — Unstract](https://unstract.com/blog/comparing-approaches-for-using-llms-for-structured-data-extraction-from-pdfs/)
- [Export to Word, PDF, or another file format — Apple Pages User Guide](https://support.apple.com/guide/pages/export-to-word-pdf-or-another-file-format-tance1161f26/mac)
- [Apple tags PDF — PDF Association](https://pdfa.org/apple-tags-pdf/)
- [PDFs that carry their own data — Forme](https://www.formepdf.com/blog/embedded-pdf-data)
- [Smart Documents: Embedding Documents in PDF Containers — Text Control](https://www.textcontrol.com/blog/2021/06/24/smart-document-containers-embedding-documents-in-pdf/)
- [jsonresume/resumeToPDF](https://github.com/jsonresume/resumeToPDF)
- [rezi-io/resume-standard](https://github.com/rezi-io/resume-standard)
- [Can AI Really Parse Resume PDF Well Enough? — Affinda](https://www.affinda.com/blog/parse-resume-pdf)
