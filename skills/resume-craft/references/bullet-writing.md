# Bullet Writing

## The pattern

**[Verb] [result with number] by [specific mechanism]; [scope]. ([technologies])**

X-Y-Z reordered for tech: outcome first because that's what the F-pattern scan reads, mechanism second because that's what the hiring manager reads, stack last because that's what the parser and the keyword search read.

Length: 1–2 lines. Over ~30 words, split it or cut it.

## Verb bank

Pick the verb that is *true*, not the strongest-sounding one. "Led" when you weren't the lead is a mismatch that surfaces in the first interview.

| Built / shipped | Improved | Led / owned | Analyzed / found | Enabled others |
|---|---|---|---|---|
| Built, Shipped, Launched, Implemented, Designed, Architected, Migrated, Deployed, Automated, Integrated, Prototyped | Reduced, Cut, Increased, Accelerated, Optimized, Scaled, Eliminated, Consolidated, Stabilized, Hardened | Led, Owned, Drove, Coordinated, Mentored, Onboarded, Ran, Founded, Managed | Diagnosed, Identified, Profiled, Benchmarked, Investigated, Modeled, Measured | Enabled, Unblocked, Standardized, Documented, Open-sourced, Templated |

Present tense only for the current role's ongoing duties; everything completed is past tense, including in the current role.

## Fluff blacklist

These are the phrases recruiters report seeing dozens of times a day. The audit script flags them. Each one is standing in for a specific thing — find the thing and write that instead.

**Self-descriptors (delete outright):** results-driven, detail-oriented, self-starter, go-getter, team player, hard worker, passionate, motivated, highly motivated, dynamic, proactive, strategic thinker, thought leader, guru, ninja, rockstar, wizard, synergy, synergistic, best-of-breed, value-add, go-to person, think outside the box, proven track record, track record of success, excellent communication skills, strong work ethic, fast learner, quick learner, hit the ground running, wear many hats

**Weak openers (rewrite the bullet):** Responsible for, Duties included, Helped, Assisted with, Worked on, Participated in, Involved in, Tasked with, Was part of, Contributed to (without saying what), Utilized (just say "used", or better, name the outcome)

**Adjectives with no referent (replace with the specific):** robust, scalable, cutting-edge, state-of-the-art, innovative, seamless, world-class, best-in-class, leverage (as a verb), impactful, various, numerous, several, many

**Pronouns:** I, me, my, we, our, he, she, they (as subject of a bullet). Resumes are written in implied first person with the pronoun dropped.

**Dead sections:** "References available upon request", "Objective: seeking a challenging position…"

## Metric-mining questions

When the user says "I don't have numbers," ask these. They almost always do.

**Scope**
- How many users / customers / requests per day / records did this touch?
- How big was the team? How many teams depended on it?
- How many services, repos, endpoints, pipelines, environments?
- What was the budget, or the size of the contract or deal?

**Efficiency**
- What did the number look like before, and after? (latency, build time, deploy time, error rate, cost, hours per week)
- How long did the task take manually, and how long after you automated it?
- How many incidents / pages / support tickets went away?

**Quantity**
- How many PRs, features, tests, migrations, integrations did you ship over the period?
- How does that compare to the team average, if you know?

**Leverage**
- Who else used the thing you built? How many people or teams? Did it become a standard?
- Did anyone downstream report a number because of it (conversion, revenue, retention)?

**Recognition**
- Were you promoted, given a scope increase, chosen for something, or awarded anything?

If a bullet truly has no number after these questions, ask whether it's an achievement at all. Duties can be summarized in a single bullet ("Owned on-call rotation for the payments API; 4 services, ~6 pages/week") or cut.

## Before / after

Each pair shows the diagnosis, then the rewrite. Rewrites contain only details the (hypothetical) candidate supplied; the pattern is what to copy, not the numbers.

**1. Duty → outcome (backend, mid-level)**
- Before: *Responsible for maintaining and improving the order processing service.*
- Diagnosis: weak opener, no metric, no mechanism, no stack.
- After: *Cut order-processing p95 latency 38% (2.1s → 1.3s) by batching inventory checks and adding a read replica; service handles ~400k orders/day. (Java, Spring, Postgres)*

**2. Adjective → specific (frontend, early career)**
- Before: *Built a robust, scalable, user-friendly dashboard using modern web technologies.*
- Diagnosis: four adjectives, zero facts.
- After: *Built the internal ops dashboard used daily by 60+ support agents, replacing a 4-tab spreadsheet workflow; reduced average ticket lookup from ~90s to under 10s. (React, TypeScript, GraphQL)*

**3. Team credit → personal contribution (infra)**
- Before: *Our team migrated the platform to Kubernetes.*
- Diagnosis: pronoun, team-level claim, no scope.
- After: *Migrated 14 of the team's 22 services from EC2 to Kubernetes, writing the Helm charts and the zero-downtime cutover runbook adopted for the remaining 8. (Kubernetes, Helm, Terraform, AWS)*

**4. Soft skill as adjective → soft skill as evidence**
- Before: *Strong mentor and communicator.*
- Diagnosis: pure fluff; the 28%-match category done wrong.
- After: *Mentored 3 interns through first production deploys; 2 converted to full-time. Wrote the team's onboarding guide, cutting new-hire ramp from ~6 weeks to ~3.*

**5. Student / internship with no outcome numbers**
- Before: *Worked on automated testing for a healthcare monitoring product.*
- Diagnosis: weak opener, no scope, no stack.
- After: *Automated the test-environment setup for a patient-monitoring platform, replacing a ~4-hour manual process with a 35-minute scripted one used by 12 QA engineers. (PowerShell, C#)*

**6. Project bullet (new grad)**
- Before: *Created a fitness app with AI features.*
- After: *Built and shipped a fitness-tracking app (iOS + web) with 300+ installs; integrated HealthKit sync and an LLM-based coaching feature that generates weekly plans from logged workouts. (SwiftUI, React, Node, Postgres)*

**7. Jargon → readable**
- Before: *Owned CFN registry RP onboarding and CCAPI conformance across 3 svc tiers.*
- Diagnosis: internal acronyms the reader can't decode.
- After: *Onboarded 9 third-party resource providers to the CloudFormation Registry and brought them to Cloud Control API conformance, fixing 40+ contract-test failures. (Java, AWS)*

**8. Overlong → split**
- Before: *Designed and implemented a new data pipeline that ingests events from multiple sources, transforms them, and loads them into the warehouse, while also improving monitoring and reducing costs and working with the analytics team to define new metrics and dashboards that leadership used for quarterly planning.*
- After:
  - *Built the event ingestion pipeline (Kafka → Spark → Snowflake) processing ~2B events/day; cut warehouse compute cost 27% by moving to incremental loads.*
  - *Defined 11 core product metrics with the analytics team; dashboards used in every quarterly planning review since Q2.*

**9. Manager-level: outcomes not activities**
- Before: *Managed a team of engineers and ran sprint planning.*
- After: *Managed 8 engineers across 2 squads; shipped the new billing system on schedule (Q3 target), cut open P1 incidents from ~5/month to <1, and promoted 2 engineers to senior.*

**10. Career changer: transferable, quantified**
- Before: *Previously worked in retail management before transitioning to software.*
- After: *Ran a 14-person retail team with $2.4M annual revenue; built the store's inventory-reorder spreadsheet model that became the regional standard for 9 locations — the project that led to a career move into software.*

**11. Old role: compress**
- Before: (six bullets for a 2015 role)
- After: *Junior Developer, Acme Corp, 2014–2016 — Shipped features for a Rails e-commerce app serving ~50k monthly customers.* (one line; save the word budget for recent roles)

**12. Keyword alignment done honestly**
- JD asks for: "distributed systems", "observability", "on-call"
- Before: *Improved reliability of backend services.*
- After: *Owned on-call for 6 distributed backend services; added tracing and SLO dashboards (OpenTelemetry, Grafana) that cut mean time-to-diagnose from ~45 min to ~12.*

## Checking your own rewrite

- Cover the verb: does the rest of the bullet still say something concrete?
- Cover the number: does the bullet collapse into a duty?
- Would a skeptical interviewer be able to ask "how did you measure that?" and get a real answer from the candidate?
- Could this exact bullet appear on a different person's resume? If yes, it isn't specific enough.
