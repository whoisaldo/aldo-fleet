# Tech Resume Specifics

Software engineering roles have their own screening conventions. Most of this is drawn from Orosz's *The Tech Resume Inside Out* and the Pragmatic Engineer resume template, cross-checked against the general data in `research.md`.

## What the tech recruiter is pattern-matching in the first glance

1. **Years of experience** — computed from the dates. Make the math trivial: consistent date format, no gaps that require guessing.
2. **Relevant technologies** — they're looking for the stack in the JD. It should appear in bullets *and* the skills section. Missing stack on page one = "Maybe" pile at best.
3. **Measured impact** — numbers on users, scale, latency, reliability, cost, team size.
4. **Work authorization** — only when the role involves relocation or visa sponsorship. One line in contact or summary if it's a plus ("US citizen", "EU work permit"); omit if it's neutral.
5. **Something rare** — notable company, core OSS contributor, patent, award, competition placement, PhD, a product with real users. If the candidate has one, it goes on page one, high up.

## Section order by situation

**Experienced engineer (2+ real roles):**
Contact → Experience → Skills → Education → Projects/OSS → Other

**Student or new grad:**
Contact → Education (with expected grad date, relevant coursework if space) → Experience (internships, co-ops, part-time) → Projects → Skills → Other

**Bootcamp or career changer:**
Contact → Summary (two lines: what you're moving into, the strongest proof you can do it) → Projects → Technical Experience (if any) → Skills → Prior Experience (compressed, transferable numbers kept) → Education

**Skills-first variant:** when the role is a hard stack filter (e.g., "5+ years Rust", "Kubernetes platform engineer"), move Skills directly under Contact so the match is visible before the recruiter reads a single bullet. Orosz explicitly endorses this depending on target companies.

## The Skills section

- Grouped and comma-separated. Groups that work for most SWE roles: `Languages`, `Frameworks`, `Infrastructure / Cloud`, `Data`, `Tools`. Adapt to the role (e.g., `Mobile`, `ML`, `Embedded`).
- Only skills the candidate can be interviewed on. A skill listed but absent from any bullet invites the question "where did you use this?" — have an answer or remove it.
- No proficiency bars, percentages, or "Expert / Intermediate / Beginner" labels. Recruiters don't trust self-ratings and parsers choke on the graphics.
- Order within a group by relevance to the JD, not alphabetically.
- Match the JD's spelling and casing for named technologies (`PostgreSQL` vs `Postgres` — pick the JD's).

## Experience bullets for engineers

Everything in `bullet-writing.md` applies. Engineering-specific additions:

- **Scale numbers are almost always available**: requests/second, daily active users, records, services, regions, clusters, repos, data volume. Ask.
- **Reliability numbers**: uptime, SLO attainment, incident count, MTTR, on-call load.
- **Performance numbers**: latency percentiles (say which — p50/p95/p99), throughput, build/CI time, cold start, bundle size.
- **Cost numbers**: cloud spend, instance count reductions, licensing.
- **Delivery numbers**: features shipped, release cadence change, migration counts.
- Put the stack at the end of the bullet in parentheses. This lets the bullet read as prose while still surfacing every technology to a keyword search.
- Show progression: promotions stacked under one company header; scope growth visible ("owned 1 service" → "owned the platform team's 6 services").
- Team credit vs. personal credit: "on a team of 5 that…" is fine when true and the personal part follows.

## Projects and open source

For students, new grads, and career changers, projects are the experience section. Treat them with the same rigor:

- Name, one-line description, link (repo or live URL — must be current and clickable).
- Bullets with outcomes: users/installs/stars/downloads, what problem it solved, what was technically hard, stack at the end.
- Prefer 2–3 substantial projects over 6 trivial ones. A tutorial follow-along is not a project.
- **Open-source contributions**: name the project, what you contributed (feature, fix, docs), scale of the project (stars/users) so the reader can gauge it, and whether you're a maintainer.
- **Shipped products with real users** are the single strongest signal a junior candidate can show. Put the number of users/installs in the first line.

For experienced engineers, keep Projects only if something is notable (real usage, a known OSS role, a talk, a publication). Otherwise the space belongs to Experience.

## Education for engineers

- Degree, school, year. GPA if ≥3.5 and recent. Honors if any.
- Relevant coursework: students only, only courses the JD would care about (Distributed Systems, Databases, ML), one line.
- Bootcamp: list it under Education with dates; don't present it as employment.
- Self-taught with no degree: skip the section or list relevant certifications; let Projects and Experience carry the weight. Don't apologize for it on the page.

## Things that read badly to engineering hiring managers

- A skills list with 40 technologies. Signals breadth-without-depth or padding.
- "Familiar with" / "Exposure to" — either you can be interviewed on it or it shouldn't be there.
- Bullets that describe the *product* instead of the *contribution* ("The app allows users to…").
- Company boilerplate ("Acme is a leading provider of…").
- Describing a tutorial or coursework as a project without saying so.
- LeetCode counts, typing speed, "Python (Expert)".
- Claiming architecture ownership at a junior level without the scope to back it.
- Any metric an interviewer could disprove in 30 seconds.

## Cover letters (if asked)

Orosz's guidance: company first, yourself second. Show you understand the role and read the company's site or engineering blog; state briefly why you're a fit; be specific and short; PDF it. A personalized half-page beats a templated full page. Most tech companies don't require one; when optional, write it only if there's a specific reason to (referral, career change, unusual situation).
