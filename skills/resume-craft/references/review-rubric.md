# Review Rubric

Score out of 100. Weights reflect what the data says moves interview rates most (Cultivated Culture, TalentWorks, Orosz), not what's easiest to check. Use `scripts/resume_audit.py` output for the measurable parts, then judge the rest by reading as a recruiter would.

Report the score, then the top three fixes in order of points recoverable. Don't list every deduction — the user needs priorities, not an inventory.

## A. Evidence of impact — 30 points

| Criterion | Points |
|---|---|
| ≥70% of experience bullets contain a number or concrete measurable | 15 |
| ≥5 distinct metrics across the document | 5 |
| Bullets describe outcomes, not duties (mechanism + result present) | 5 |
| Claims are personal ("led", "built"), not team-attributed | 5 |

Partial credit: 40–69% of bullets with numbers → 8; 20–39% → 4; under 20% → 0.

## B. Fit to the target role — 25 points

| Criterion | Points |
|---|---|
| JD hard-skill coverage ≥75% (audit `hard_skill_coverage`) | 10 (≥60%: 6; ≥40%: 3) |
| JD soft skills demonstrated inside bullets, not listed as adjectives | 5 |
| Target title or its exact phrasing appears truthfully somewhere | 3 |
| Irrelevant roles/skills pruned or compressed | 4 |
| Section order matches seniority (education up for students; experience up otherwise) | 3 |

No JD supplied: score B out of 10 using only the last three rows, and tell the user the review is capped without a target.

## C. Scannability — 20 points

| Criterion | Points |
|---|---|
| Single column, standard headers, bullets not paragraphs | 6 |
| Every bullet opens with a strong verb (audit `weak_openers` = 0) | 5 |
| Bold limited to names/titles/companies; consistent dates; white space present | 4 |
| Page one answers "what role, why plausible" in one glance; promotions visible | 5 |

## D. Concision and language — 15 points

| Criterion | Points |
|---|---|
| Word count 475–600 (non-exec) | 6 (400–700: 3) |
| Zero fluff-blacklist hits and zero pronouns | 5 (1–2 hits: 3) |
| No bullet over ~30 words; no jargon or unexpanded acronyms | 4 |

## E. Completeness and hygiene — 10 points

| Criterion | Points |
|---|---|
| Email, phone, LinkedIn present; GitHub/portfolio for engineering roles | 4 |
| Reverse-chronological, consistent date format, no unexplained multi-year gaps | 3 |
| PDF-ready: no tables/columns/images/headers-footers; links clickable; sensible filename | 3 |

## Interpreting the total

- **85–100** — Submit-ready. Offer role-specific tailoring only.
- **70–84** — Solid foundation; usually missing metrics or JD alignment. One focused pass.
- **50–69** — Typical unoptimized resume (this is where most of the 125k dataset sits). Full rewrite of bullets, restructure, prune.
- **Below 50** — Rebuild from `assets/resume-template.md` using the user's raw history; don't try to patch.

## Automatic red flags (call out regardless of score)

- Any metric that looks invented or unverifiable ("improved efficiency by 500%")
- Title inflation (reported title differs from what a background check would show)
- Photo, DOB, marital status, or full street address on a North American resume
- Hidden text, white-on-white keywords, microscopic fonts
- Multi-column template, skill bars, icons, or an image-based PDF
- "References available upon request", an "Objective" line, or a summary with no specific claim
- Stale or broken links
