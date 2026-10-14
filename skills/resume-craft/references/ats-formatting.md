# ATS and Formatting Spec

## What an ATS actually does

It parses the file into fields (name, contact, titles, employers, dates, skills, education), stores it, and lets recruiters search and sort. 92% of recruiters report their ATS does not auto-reject on formatting or content; the ~8% who configure filters use thresholds like minimum years or required-skill counts. Newer systems add an LLM layer that summarizes and ranks parsed resumes and does semantic keyword matching.

So the two ways to actually lose at the ATS stage are:

1. **Parse failure** — the layout produced empty or garbled fields, so the resume can't be found in a search or the recruiter sees a mess in the ATS preview.
2. **Knockout questions** — authorization, location, minimum years. Nothing on the resume fixes these.

Everything below exists to prevent #1 while keeping the document pleasant for the human who reads it next.

## Layout rules

| Do | Don't |
|---|---|
| Single column, top-to-bottom flow | Two columns, sidebars, text boxes |
| Standard section names: Experience, Education, Skills, Projects, Certifications | Creative names ("My Journey", "Toolbox", "Where I've Been") |
| Contact info as plain text in the body, at the top | Contact info inside the document header/footer region |
| One font, 10–12pt body, 0.5–1" margins | Multiple fonts, icons, skill bars, star ratings, photos, logos |
| Real text in the PDF (selectable) | Image-based PDF, Canva exports flattened to PNG |
| Simple bullet character (•, -, or the app's default) | Custom glyphs, emoji, checkmarks |
| Dates in one consistent format: `Jun 2024 – Aug 2025` or `2024 – 2025` | Mixed formats, dates in separate columns/tables |
| Company, title, location, dates on one or two lines | Tables to align them |
| Clickable links with short display text: `linkedin.com/in/handle`, `github.com/handle` | Raw `https://www.linkedin.com/in/...` strings, or link text that hides the destination |

Tables are the most common parse-breaker in otherwise good resumes. If you need alignment (dates right-aligned), use a right tab stop, not a table.

## File

- **Format:** PDF unless the application explicitly asks for .docx. Some older ATS prefer .docx; if the portal says so, send .docx.
- **Filename:** `Firstname_Lastname_Resume.pdf`. Recruiters see the filename in the ATS list; `resume_final_v3 (2).pdf` is a bad first impression.
- **Size:** under 1 MB; no embedded fonts problems — export from the word processor, don't "print to PDF" from a browser.
- **Metadata:** set the PDF title to the candidate's name if the tool allows.

## Sections

**Contact** — Name (largest text on the page), city + state/country, email, phone, LinkedIn, GitHub/portfolio for technical roles. Nothing else. No full street address, no photo, no DOB, no marital status in North America, UK, Australia. Follow the user's regional norm otherwise.

**Summary (optional)** — Two lines maximum, only if it makes a specific, rare, or role-matching claim. Omit for most early-career candidates.

**Experience** — Reverse chronological. `Title` bold; `Company` bold or small caps; location and dates on the same line. Promotions: one company header, titles stacked under it with their own dates. 3–6 bullets for recent roles, 1–2 for older ones.

**Skills / Technologies** — Grouped, comma-separated, no proficiency percentages: `Languages: Go, Python, TypeScript · Infra: AWS, Kubernetes, Terraform · Data: Postgres, Kafka`. List only what the candidate can be interviewed on. This section supports the experience section; it doesn't replace it.

**Education** — Degree, school, graduation year (expected year for students), GPA only if ≥3.5 and within ~3 years of graduation. Relevant coursework only for students.

**Projects** — Same bullet rules as experience: outcome, mechanism, stack, link. Essential for students and career changers; optional for experienced engineers unless the project is notable.

**Other** — Awards, certifications relevant to the role, publications, talks, OSS maintainer roles, volunteering adjacent to the field. One line each. Interests only if they're a genuine conversation hook and there's room.

## Length

| Situation | Pages | Words |
|---|---|---|
| Student, new grad, <5 years | 1 | 400–550 |
| 5–10 years | 1–2 | 475–600 |
| 10+ years, senior/staff, manager | 2 | 500–700 |
| Executive | 2–3 | 700–1,000 |
| Academic CV, federal | as required | — |

Page one must stand alone. The 7-second scan never reaches page two.

## Producing the file

**Markdown** is the default hand-back format: portable, editable, and the user can paste it into any builder.

**When a file is requested**, use the environment's document tools:
- `.docx`: use the docx skill or `python-docx`. Single column, built-in heading styles for section names (the parser reads them), bullet lists via list styles, right tab stop for dates. Then export to PDF.
- PDF direct: `reportlab` or `weasyprint` from HTML. Keep the HTML single-column, semantic (`h1` name, `h2` sections, `ul` bullets), and embed a standard font.
- Never rasterize. Never use a designed template with columns "because it looks better" — it loses on both the eye-tracking data and the parser.

After generating, extract the text back out (`pdftotext` or the docx skill's reader) and confirm the section order, dates, and contact info survive round-trip. That is exactly what the ATS will see.

## Regional notes

- **US / Canada:** "resume", 1–2 pages, no photo/DOB, no references section.
- **UK / Ireland / Australia:** "CV", 2 pages standard, no photo, "personal profile" summary is common.
- **Germany / Austria / Switzerland:** photo, DOB, and sometimes nationality still expected in traditional firms; tech companies increasingly follow US norms — ask.
- **India:** 1–2 pages; DOB sometimes requested by portals; skip the photo.
- **Academic:** full CV, publications list, no length limit.

When the user doesn't state a region, infer from the JD's location and confirm in one line.
