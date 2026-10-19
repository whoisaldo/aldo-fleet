# Job apply, shareable copy

A workflow for tailoring a resume to one posting, filling the application as a
saved draft, and handing over an HTML screenshot review before anything is
submitted. This folder is a redacted export. It does not sign in, submit
applications, or include anyone's answers.

## Contents

- `SKILL.md`: the workflow, with personal paths, employers and machine details
  replaced by references to your profile.
- `references/profile.md`: a blank profile template for your own answers.
- `references/portals.md`: observed Workday failure modes and how to avoid them.
- `scripts/review_gallery.py`: builds a self-contained HTML review gallery from
  a JSON manifest. Standard library only.
- `agents/openai.yaml`: Codex display metadata.

## Setup

1. Fill in `references/profile.md` in your own private copy. Leave fields blank
   to have the agent ask.
2. Point the profile at your own resume workspace or repository.
3. Use a browser tool your agent can drive, such as T3 preview tools.
4. Install the `resume-craft` skill too if you want its tailoring guidance.

## Redactions

Removed the original user's name, contact details, work-authorization and
demographic answers, education dates, school, employers, project names, a
collaborator's name, local paths, machine names and a specific employer's
application. The profile is now a blank template. The gallery helper and Codex
metadata are unchanged. No credentials, application records or resumes are
included.
