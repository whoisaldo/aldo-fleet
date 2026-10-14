---
name: resume-craft
description: Research-backed resume writing, rewriting, tailoring, and review. Use this skill whenever the user mentions a resume or CV in any form — writing one from scratch, updating an old one, tailoring to a job description, reviewing/critiquing, rewriting bullet points, "making it ATS-friendly", checking length, or asking what recruiters look for. Also trigger for LinkedIn experience sections, job-application materials, or when a user pastes a job posting and their background together, even if they don't say the word "resume". Built on the Cultivated Culture 125k-resume dataset, Gergely Orosz's The Tech Resume Inside Out, Ladders eye-tracking, ResumeGo callback studies, and 2025–2026 recruiter surveys on AI-written applications.
---

# Resume Craft

A resume has exactly one job: get the candidate to a first conversation. It is not a work history, not an autobiography, and not a list of duties. Every decision below serves that one job.

The guidance here is grounded in measured data rather than folk wisdom. `references/research.md` holds the numbers and sources; read it once so you can explain *why* you're making a change when the user asks. The short version:

- Recruiters make a keep/toss decision in **~7 seconds** on the first pass (Ladders eye-tracking; Orosz puts it at 5–20s). They scan in an F-pattern: top-left, headers, first words of bullets.
- **36% of resumes contain zero metrics** and only 26% contain five or more (Cultivated Culture, n=125,484). Numbers are the single biggest differentiator available.
- Candidates match only **51% of the keywords** in their target job description — 60% of hard skills, **28% of soft skills**.
- The interview-rate sweet spot is **475–600 words**; 77% of resumes fall outside it (TalentWorks via Cultivated Culture).
- In 2026, recruiters are drowning in AI-written applications. **78% specifically look for personalized details; 62% say generic AI resumes get rejected.** Sameness is the new failure mode. Specificity is the cure.

## Workflow

### 1. Intake — get the raw material before writing anything

Collect, in this order of importance:

1. **The target job description** (or at minimum: title, company, seniority). Without a target, you can only produce a generic resume, and generic is what gets rejected. If the user has none, ask what roles they're aiming at and work from a representative posting.
2. **The current resume** (any format) or, for a from-scratch build, their career history: roles, dates, what they built, and any numbers they remember.
3. **Seniority and situation**: student/new grad, early career (<5 yrs), mid (5–10), senior/staff, manager/exec, or career changer. This drives section order and length.
4. **Constraints**: page limit, region (US resume vs. EU CV conventions), work authorization if relocating, links they want included.

Read uploaded files with whatever file-reading tools the environment provides (docx/pdf skills, `pdftotext`, `python-docx`). Never guess at contents you can't read.

**Do not fabricate.** If a bullet needs a number and the user hasn't supplied one, ask ("roughly how many users hit that service?" / "how much faster was the build after?"). Scope numbers — team size, request volume, number of services, dataset size — are almost always recoverable even when outcome numbers aren't. An honest scope metric beats an invented outcome metric every time; invented metrics get caught in interviews and end careers.

### 2. Diagnose — run the audit before editing

Run the deterministic checks first so your review is grounded in measurement, not vibes:

```bash
python scripts/resume_audit.py <resume.txt|md|docx|pdf|tex> [--jd <job_description.txt>] [--json]
```

It reports word count vs. the 475–600 target, metric density per bullet, buzzword/pronoun hits, contact-info completeness (email, phone, LinkedIn, GitHub), weak bullet openers, overlong bullets, and JD keyword coverage (hard vs. soft skills, ranked missing terms). Read `references/review-rubric.md` to turn the audit into a scored, prioritized critique. Lead your review with the two or three changes that move the score most — usually metrics, JD alignment, and fluff removal, in that order.

Feed it the source file when one exists (Markdown, .docx, or LaTeX). PDF extraction splits every bullet at its line breaks, so words-per-bullet and numbers-per-bullet come out wrong from a PDF. Use the PDF only as the final round-trip check that contact details and section headers survive extraction.

When the user only wants a review (not a rewrite), deliver the rubric score, the top fixes with before/after examples for 2–3 bullets, and stop. Don't rewrite the whole document unasked.

### 3. Structure for the 7-second scan

The recruiter's first glance hunts for five things (Orosz): years of relevant experience, relevant technologies, evidence of measured impact, work authorization when it matters, and anything rare (award, PhD, core OSS contributor, notable company). Put all five where an F-pattern scan lands: top of page one, left-aligned, in headers and bullet openers.

Layout rules that the eye-tracking data supports:

- **Single column.** Multi-column layouts and sidebars lost recruiter attention in the study and break ATS parsers.
- **Standard section headers** in this order for experienced candidates: Contact → (optional Summary) → Experience → Skills/Technologies → Education → Projects → Other. For students and new grads: Contact → Education → Experience/Internships → Projects → Skills. Move Skills up under Summary only for roles where stack match is the primary filter.
- **Bullets, never paragraphs.** Bold job titles and company names; nothing else bold. Consistent date format, right-aligned, months dropped for roles more than a few years old.
- **White space is not wasted space.** Cluttered pages scored worst.
- **Make promotions visible** — stack titles under one company header rather than repeating the company. Progression is a signal recruiters explicitly look for.
- **Summary is optional and rarely read on the first scan.** Include one only if it can carry a specific, rare, or job-matching claim in two lines. Cut it if it would read as generic.
- **No photo, date of birth, gender, marital status, or full street address** (US/UK/CA/AU). City + country is enough. Some EU/Asian markets expect a photo; follow the user's region.

Full formatting spec, including ATS parseability rules and file naming, is in `references/ats-formatting.md`.

### 4. Rewrite bullets — the core of the work

Every bullet should answer: *what changed because this person was there, and how do we know?*

Use the X-Y-Z pattern (Google's Laszlo Bock; adopted by Cultivated Culture): **Accomplished [X] as measured by [Y], by doing [Z].** In practice for tech resumes, Orosz's ordering reads better: lead with the result, then the mechanism, then the specific technologies at the end.

> Reduced p99 checkout latency 40% (1.2s → 720ms) by moving cart validation to an async worker and adding a Redis read-through cache; served 2M daily orders. (Go, Redis, Kafka)

Rules, each with a reason:

- **Start with a strong past-tense verb** (present tense for the current role only). "Responsible for" and "Helped" are the two most common weak openers; the audit flags them. The verb is the first word the F-pattern scan reads.
- **At least one number per bullet, target 5+ across the document.** Metric categories when revenue isn't available: *scope* (users, requests/sec, team size, services owned, budget), *efficiency* (time saved, cost cut, build time, incident MTTR), *quantity* (PRs shipped, tests written, endpoints migrated), *leverage* (how many teams or people used the thing you built). If a bullet truly has no number, it's probably a duty, not an achievement — cut or merge it.
- **Specifics over adjectives.** "Robust", "scalable", "cutting-edge", "passionate", "results-driven" are the exact phrases recruiters report seeing forty times an afternoon in AI-written resumes. Replace every adjective with the concrete thing it was standing in for.
- **Technologies at the end of the bullet, in parentheses or after a semicolon.** The scan reads the outcome first; the ATS and hiring manager still find the stack.
- **Say "I", show "we".** No pronouns at all in the text, but the bullet must describe *this person's* contribution, not the team's. "Led a team of 4 to ship X" is fine; "The team shipped X" is not.
- **More detail for recent roles, less for older ones.** Recent role: 4–6 bullets. Roles older than ~8 years: 1–2 bullets or a single line.
- **Prune the irrelevant.** A bullet that doesn't support the target role costs scan time and word budget. Tailoring means removal as much as addition.
- **No internal jargon or unexpanded acronyms** the reader can't be expected to know.

`references/bullet-writing.md` has the verb list, the fluff blacklist, metric-mining questions to ask the user, and twelve before/after rewrites across seniority levels.

### 5. Align to the job description — naturally

The average JD contains ~43 keywords (median 39). The audit tells you which ones the resume is missing, split into hard and soft skills. Work through them like this:

1. **Hard skills the candidate actually has but didn't name:** add them where they were used — inside the relevant bullet, not just in the skills list. This is the highest-value, lowest-risk edit.
2. **Soft skills** (the 28%-match category): never list them as adjectives. Demonstrate them inside a bullet: "mentored 3 interns to first production deploy" *is* mentorship; "strong mentor" is fluff.
3. **Title mirroring:** if the JD says "Backend Engineer" and the candidate's title was "Software Engineer II (Backend)", make sure the JD's phrasing appears somewhere truthful — a summary line, a parenthetical, or the skills header.
4. **Synonyms:** modern ATS and AI screeners do semantic matching, so "Kubernetes" covers "K8s" and "container orchestration". Use the JD's exact term once, naturally, and don't repeat it for density.
5. **Never** add a skill the candidate doesn't have, hide white-on-white text, or shrink keywords to 1pt. Hidden-text stuffing is now actively detected and flagged as manipulation.

Cultivated Culture's own caution applies: chase natural fit, not a perfect scanner score. A resume that reads like a keyword list gets tossed by the human who reads it next.

### 6. Length and format

- **Word count target: 475–600** for non-executive resumes. This range showed roughly double the interview rate. Over 600 usually means duties and old roles that should be cut; under 475 usually means missing metrics and specifics.
- **Pages:** one page for students and anyone under ~5 years of experience. Two pages is fine and often preferred beyond that (ResumeGo: recruiters chose two-page resumes 2.3× as often for mid/senior roles), *provided page one stands alone* — the 7-second scan never reaches page two. Never exceed two pages except for academic CVs, federal applications, or executive roles.
- **File:** PDF, single column, real text (not an image), named `Firstname_Lastname_Resume.pdf`. Contact info in the body, not in a header/footer field (many parsers skip those). Clickable links with display text, not raw URLs. Remove links to stale profiles.
- **Fonts:** one clean font, 10–12pt body, 0.5–1" margins. No icons, graphics, skill bars, or star ratings — they parse as garbage and read as decoration.

### 7. Final QA before handing it back

Re-run the audit on the finished text. Then check, in this order:

1. Every bullet starts with a verb and contains a number or a concrete specific.
2. No entries from the fluff blacklist; no first-person pronouns.
3. Email, phone, LinkedIn present; GitHub/portfolio present for engineering roles.
4. Word count in range; page count matches the seniority rule; page one is self-sufficient.
5. Dates consistent and reverse-chronological; no unexplained gaps that a one-line entry could resolve.
6. Nothing on the page that the candidate couldn't defend in detail in an interview.
7. Read it cold, once, as a recruiter: within seven seconds, is it obvious what role this person is applying for and why they're plausible?

## Output

Default to returning the resume as clean Markdown the user can paste anywhere, plus a short change log explaining the three highest-impact edits and the audit score before/after. If the user asks for a file — or the environment has document-creation tools and the user needs to submit somewhere — produce a PDF or .docx following `references/ats-formatting.md`, and use `assets/resume-template.md` as the structural starting point. Never deliver a resume as an image or a multi-column design template.

When reviewing rather than rewriting, keep it to: score, top three fixes, two or three worked before/after bullets, and an offer to do the full pass.

## Guardrails

- **Truth over polish.** Never invent employers, titles, dates, degrees, or metrics. Ask for real numbers; use scope metrics when outcomes are unknown; leave a `[NEEDS NUMBER]` placeholder rather than a plausible-sounding fake. Flag any existing claim that looks inflated.
- **Preserve the person's voice.** Recruiters in 2026 are pattern-matching against AI sameness. Keep unusual, specific, human details — the odd project, the concrete domain term, the number only they would know. Uniform, polished, adjective-heavy prose is the tell.
- **No manipulation techniques**: no hidden text, no keyword walls, no fake certifications, no title inflation.
- **Respect regional norms** the user states (photo, DOB, and "CV" length conventions differ outside North America).
- **Don't moralize about AI use.** Using an assistant to write a resume is normal; the failure is generic output, not the tool.
- **No em dashes anywhere in the resume text.** They are the most recognizable AI tell on a page that is already being read for AI tells. A colon, a full stop, or a pair of commas does the same work.
- **A repo's own rules win.** When the resume lives in a repository with an `AGENTS.md` or `CLAUDE.md`, its formatting, length, and claim-provenance rules override the defaults in this skill and its references.

## Reference files

| File | Read when |
|---|---|
| `references/research.md` | You need the data or source behind a recommendation, or the user asks "why?" |
| `references/review-rubric.md` | Scoring a resume, prioritizing fixes, or explaining a grade |
| `references/bullet-writing.md` | Rewriting bullets: verbs, fluff blacklist, metric-mining questions, before/after examples |
| `references/ats-formatting.md` | Producing a file, or the user asks about ATS, parsing, fonts, layout |
| `references/tech-resume.md` | Software engineering roles specifically: section order by seniority, projects/OSS, skills section design, new-grad and career-changer variants |
| `assets/resume-template.md` | Building from scratch or restructuring a messy document |
| `scripts/resume_audit.py` | Always — before and after editing |
