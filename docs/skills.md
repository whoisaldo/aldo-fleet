# Skill bank

The bank keeps 19 base fleet skills and three general assistant skills, for 22 bundled skills. Canvas LMS is an optional planning capability guide. OpenClaw visual canvas/widgets are a separate recipe.

Use `python3 scripts/bank.py list` to see selectable modules, skills and presets. Base sources remain in `skills/` and `vendor/skills/`; optional assistant sources live in `bank/skills/`. Provider-owned skills are cataloged rather than copied.

| Skill | What it does | Setup notes |
| --- | --- | --- |
| baseline-ui | Applies UI conventions | No fleet service required |
| frontend-design | Builds and styles web UI | Uses the project's tools |
| fixing-accessibility | Finds and fixes accessibility issues | Uses the project's tools |
| fixing-motion-performance | Fixes animation performance | Uses the project's tools |
| unslop | Edits writing into plain language | No fleet service required |
| resume-craft | Writes and reviews resumes and application material | Kept for future job changes, even with a full-time role |
| task-to-review | Takes code work through checks and a reviewable result | Optional fleet task and lease helpers |
| fleet-operate | Maintains configured fleet profiles and machines | Read your own fleet.json |
| remote-handoff | Prepares work for another configured worker | Optional SSH worker; Windows display needs interactive login |
| orchestrate-trifecta | Delegates builds and independent reviews | T3 orchestration tools and authorized providers |
| codex-image | Generates and edits raster images through Codex | Older Claude-only personal bridge, Mac/POSIX and native Codex |
| codex-3d | Creates 3D artifacts through Codex | Older Claude-only personal bridge; Blender for relevant modes |
| codex-computer-use | Runs visual browser QA through Codex | Older Claude-only personal bridge; browser dependencies |
| brag | Turns a project into a launch video | HyperFrames and its documented media dependencies |
| hyperframes-core | Defines renderable compositions | HyperFrames |
| hyperframes-creative | Plans video design, audio and beats | HyperFrames |
| hyperframes-animation | Builds seek-safe animation | HyperFrames |
| hyperframes-keyframes | Adds camera moves and keyframes | HyperFrames |
| hyperframes-cli | Runs validation, preview and render workflows | HyperFrames CLI; optional cloud services require your own accounts |

The six video skills are vendored with their assets and original notices. `skills/external.lock.json` pins their unchanged content. The bridge skills retain their scripts, examples and explicit specialized model choices. Their old standalone installers are reference material, not required for fleet setup.

Built-in, plugin and organization-managed skills are intentionally left with their providers. The legacy coding checkouts contained the same nine imported custom skills. Optional assistant skills cover Canvas planning, shared resources and form review.

| Optional OpenClaw skill | What it does |
| --- | --- |
| canvas-planning | General planning and organization options through your own supported Canvas integration |
| shared-resource-review | Reads embedded guides and checks deliverables |
| survey-requirements-review | Reviews form requirements and prepares an offline checklist |

See [provider skills](modules/provider-skills.md) for built-ins, synced tools, plugins and the general OpenClaw capability catalog. Older bridge helpers and deprecated setup records remain available.
