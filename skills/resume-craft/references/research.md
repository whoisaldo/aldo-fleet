# Research Base

Every recommendation in this skill traces to one of the sources below. Numbers are quoted as published; caveats are noted because none of these are peer-reviewed RCTs and the agent should not overstate certainty when explaining them to users.

## Contents

1. Cultivated Culture — 125,484-resume analysis (Austin Belcak)
2. The Tech Resume Inside Out (Gergely Orosz, The Pragmatic Engineer)
3. Ladders eye-tracking studies (2012, 2018)
4. ResumeGo studies — LinkedIn link callbacks; one vs. two pages
5. TalentWorks — resume length vs. interview rate
6. Google's X-Y-Z bullet formula
7. 2025–2026 recruiter surveys on AI-written applications
8. How ATS actually work (and the auto-reject myth)
9. Reconciling the contradictions

---

## 1. Cultivated Culture — 125,484 resumes

**Source:** Austin Belcak, "Resume Statistics: We Analyzed 125,000+ Resumes, Here's What We Learned," cultivatedculture.com/resume-statistics/ (first published 2021, updated Aug 2025). Data from first scans in the ResyMatch resume-vs-JD scanner.

**Method caveat (their words):** not scientifically gathered or reviewed; correlational; "casual conclusions." First-scan data used so the numbers reflect unoptimized resumes.

| Finding | Number |
|---|---|
| Resumes with a LinkedIn URL | 48% (email: 85%, phone: 78%) |
| Average keywords/skills in a job description | 43 (median 39) |
| Share of JD keywords present in candidate resumes | 51% overall |
| — hard skills matched | 60% |
| — soft skills matched | 28% |
| Resumes with ≥5 measurable metrics | 26% |
| Resumes with zero metrics | 36% |
| Resumes outside the 475–600 word range | 77% |
| Resumes containing buzzwords, clichés, or pronouns | 51% (most with only 1–2 instances) |

**Their #1 takeaway:** most candidates fail the basics. The low-hanging fruit — LinkedIn link, JD keywords, metrics, no fluff — is where the advantage is, not font choice or one-vs-two-page debates.

**Metric categories they recommend when revenue isn't available:** Scope (team/people/budget/goal), Efficiency/Productivity (time, cost, waste, hours saved), Quantity (volume produced, vs. peers/average), Leveraging Others (downstream teams' outcomes from your work).

**Their keyword caution:** include as many as fit naturally; do not keyword-stuff for a scanner score — over-indexed resumes read as robotic or disingenuous.

## 2. The Tech Resume Inside Out — Gergely Orosz (2020)

**Source:** thetechresume.com; blog.pragmaticengineer.com/resume/. Written by a former Uber engineering manager with input from tech recruiters and hiring managers at well-known companies. Companion template: "The Pragmatic Engineer's Resume Template" (Google Doc; also ported as the "Parker" template on Standard Resume).

**Framing:**
- The goal of a resume is to get an interview for a specific role at a specific company. Nothing more. It is not a complete work history.
- A *good* resume represents you fairly and gets you through screening if you're qualified. A *great* resume makes the reader want to talk to you immediately — usually by showing rare, valuable experience that is exactly what the job needs, or clear career progression toward the role.
- Great resumes are not generic. They are great for *that* role.

**The pipeline:** ATS queue → resume screen (5–20 seconds; steepest drop-off; recruiters sort into Yes/Maybe/No) → recruiter call → technical screen → onsite → offer. If enough "Yes" candidates pass the phone screen, the top of the "Maybe" pile never gets called.

**ATS:** almost all tech companies use one. Its job is coordination and tracking, not rejection. Most "the ATS rejected me" cases are either (a) knockout/prescreen questions set by the recruiter (work authorization, minimum years, location) or (b) formatting the parser couldn't read. Humans make the decisions.

**Referrals** almost always guarantee an in-depth resume read. Ask for the referral *before* applying.

**What the recruiter looks for in the first glance (in order):**
1. Years of experience
2. Relevant technologies
3. Relevant work experience — and whether the person has consistently delivered *measured* impact
4. Work authorization / visa status (when relocation is involved)
5. Anything that pops: award, PhD, core contributor to relevant OSS, something rare among hundreds of profiles

**Formatting rules:**
- Two pages or less; most important information on page one
- Reverse chronological; dates easy to scan; drop months on roles more than a few years old
- Basic contact details at top, kept short: email, phone, city + country. No photo, DOB, gender
- Clear, neat, consistent formatting; one font; bullets, not paragraphs; be concise, don't spell out trivial things
- PDF, named `{yourname}_resume.pdf`
- Links must be clickable; don't leave full URLs as display text; remove links to stale GitHub/LinkedIn/websites
- Make promotions clearly visible
- Remove irrelevant skills; list only the ones you're proficient in

**Summary section:** rarely read on the first scan. If present: short, specific, practical, and highlighting fit for *this* role. An overly ambitious summary can backfire. A generic one gets no attention.

**Bullet writing:**
- Focus on what you achieved; quantify with impact and business result
- Aim for at least one number per bullet: team size, users, requests, code coverage %, SLA change, before/after, revenue
- Active verbs ("Led", "Drove", "Shipped") over passive language
- Mention specific languages/technologies toward the end of the bullet
- Don't obsess over snazzy words; get specific about the details of the work
- Effective resumes contain both responsibilities and accomplishments
- Talk about yourself, not your team
- More detail on recent positions, less on older ones
- Make side projects and open-source work shine; extracurriculars adjacent to tech go at the end
- For students, new grads, bootcamp grads: move Education up, emphasize project work

**Common mistakes:** hard-to-scan layouts; too much bolding; too flashy; inconsistent formatting; sloppy phrasing; internal acronyms and jargon; not tailoring to the position; clichés instead of evidence-backed statements; verbosity and text blocks; non-clickable or stale links.

## 3. Ladders eye-tracking (2012, 2018)

**Source:** Ladders, Inc. "Eye-Tracking Study" 2018 (30 professional recruiters, 10 weeks, hundreds of resumes, eye-tracking hardware; update of a 2012 study).

- Average initial screen: **7.4 seconds** (up from 6.0s in 2012; the earlier study ran during recession-level application volume).
- Reading follows an **F- or E-pattern**: across the top, down the left edge, across again at headers.
- Resumes that held attention: simple layouts, clearly marked section and title headers, clear font, bold titles, bulleted accomplishments, white space, content that flows and draws the eye down the page.
- Resumes that lost attention: cluttered layouts, lack of white space, **multiple columns**, long sentences, missing section/job headers.

**Caveats:** small sample (30 recruiters), undisclosed job types and instructions, vendor-published. A 2025 hidden-eye-tracker experiment by Jerry Lee (Wonsulting) reproduced the F-pattern and the pull of quantified achievements. Treat the exact seconds as illustrative; treat *where attention goes* as the actionable finding.

## 4. ResumeGo studies

**LinkedIn link and callbacks** (resumego.net/research/linkedin-interview-chances/): applicants with a link to a *comprehensive* LinkedIn profile received a 13.5% callback rate vs. 7.9% for applicants with no profile — 71% higher. A bare or thin profile did not help; the profile must be complete and consistent with the resume.

**One vs. two pages** (2018; resumego.net/research/one-or-two-page-resumes/): 482 recruiters, hiring managers, HR professionals and executives screened 7,712 resumes in a hiring simulation over ~3 weeks.
- Two-page resumes were chosen **2.3×** as often overall
- By level: **1.4×** entry-level, **2.6×** mid-level, **2.9×** managerial
- Reviewers spent 2:24 on one-page resumes vs. 4:05 on two-page
- Two-page resumes rated 21% higher on "summarizes the candidate's experience and credentials"

**Caveat:** reviewers saw a small handful of resumes each, which resembles a final-round read more than a 200-applicant first screen. The result says a well-built second page doesn't hurt and often helps *once page one has earned the read*. It does not say to pad.

## 5. TalentWorks — length vs. interview rate

**Source:** TalentWorks, "The Science of the Job Search, Part VIII" (2018). 6,305 applications across 66 industries for 721 users; word count and keyword count extracted; interview rate computed; outliers clipped; weighted and smoothed.

- Resumes of **475–600 words** saw roughly **double** the interview rate of resumes outside the range.
- Both under 475 and over 600 showed significant drops.
- Career level not disclosed. Executive resumes (800–1,000+ words), federal applications, and academic CVs are legitimate exceptions.

Cultivated Culture's own scanner accepts 400–1,000 but recommends the TalentWorks range for non-executive roles.

## 6. Google's X-Y-Z formula

**Source:** Laszlo Bock (former Google SVP of People Operations), widely reported (e.g., Inc.); referenced directly by Cultivated Culture and adopted by Google's own recruiting guidance.

> Accomplished **[X]** as measured by **[Y]**, by doing **[Z]**.

Example: "Increased QoQ sales 17% by designing new conversion-focused Facebook ad imagery." For engineering bullets, Orosz's ordering (result → mechanism → technologies) is the same formula with the stack appended.

## 7. 2025–2026 recruiter surveys on AI-written applications

Sourced via Jobscan, ResuFit, Willo and others aggregating primary surveys. Treat percentages as directional; they are self-reported beliefs, not measured detection accuracy.

- **Insight Global, 2025 AI in Hiring survey:** 53% of hiring managers say they can immediately tell when a candidate used AI; ~54% say they'd care, 46% would not. The stated trigger for rejection is generic, unedited content that shows the candidate didn't read the JD — not AI use itself.
- **Resume Now, June 2025:** 78% of hiring managers actively look for personalized details; 62% report that AI-generated resumes lacking personalization frequently result in rejection; 53% are annoyed by robotic/impersonal outreach.
- **Robert Half, March 2026:** 67% of HR leaders say AI-generated applications are slowing their hiring; 84% of HR teams report feeling overworked reviewing them.
- ~80% of recruiters say they would *not* automatically reject an application for AI assistance if the content is good; roughly 20% say they would (US Chamber of Commerce, 2025).
- Recruiters' "AI radar" is trained on **sameness**: the same phrases ("results-driven professional with a proven track record"), the same structure, and adjective-heavy prose with no numbers or domain specifics.
- AI-text detectors are unreliable on resumes (Stanford found a 61% false-positive rate on non-native English writing; OpenAI retired its own detector at 26% accuracy). Vendors themselves say to treat scores as triage, not proof.

**Implication for this skill:** the most dangerous output an agent can produce is a fluent, polished, generic resume. Specific numbers, domain terms, and unusual true details are both what recruiters reward and what distinguishes a human-edited document.

## 8. How ATS actually work

- Jobscan: an ATS "doesn't reject resumes. It stores them and allows recruiters to search using keywords."
- Enhancv survey of US recruiters: 92% say their ATS does not auto-reject on formatting or content; ~8% configure any threshold filters at all (e.g., <75% match, fewer than 7 of 10 required skills).
- Workday: customers processed 173M applications in H1 2024, up 31% YoY, while requisitions grew 7% to 19M — applications growing roughly 4× faster than openings. **Volume, not algorithms, is the real filter.**
- The modern pipeline (2026) has two layers: the classic parser (fields: name, contact, titles, dates, skills; keyword match against the JD) and, increasingly, an LLM layer that summarizes and ranks parsed resumes and drafts recruiter notes. Semantic matching means synonyms count; keyword walls and hidden text are now detected and flagged as manipulation.
- Fast rejections are mostly knockout questions (authorization, minimum years, location) and **parsing failures** — tables, text boxes, columns, headers/footers, images, and non-standard section names that leave fields empty.
- No major ATS (Workday, Greenhouse, Lever, iCIMS, Taleo) rejects on page count.

## 9. Reconciling the contradictions

**"One page" vs. "two pages preferred."** These measure different moments. The 7-second first screen only sees page one; the ResumeGo simulation resembles a shortlist read where a second page adds depth. Rule: page one must stand alone and pass the scan; a second page is acceptable beyond ~5 years of experience if every line on it earns its place. The 475–600 word target usually produces one dense page or two airy ones — either is fine.

**"Add keywords" vs. "don't sound like AI."** Both Belcak and the 2026 surveys agree: keywords belong *inside* specific achievement bullets, used once, in the JD's language. Keyword density without evidence is exactly what triggers the sameness radar.

**"Summary sections matter" vs. "recruiters skip them."** Orosz: rarely read on the first pass, but a two-line, specific, role-matched summary can make a scan stick. Generic summaries cost words and attention. Default: omit unless it carries a rare or precisely matching claim.

**"Metrics everywhere" vs. "don't fabricate."** When outcome numbers are unknown, Cultivated Culture's scope/efficiency/quantity/leverage categories almost always yield an honest number. When they don't, the bullet is probably a duty and should be cut. Never invent.
