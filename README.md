# Ali's shared fleet bank

Take what fits your setup. This repo collects portable skills, tools and optional integration ideas, including T3 Code, OpenClaw, Tailscale, Cloudflare preview tunnels, the inference proxy, both Canvas features and older workflows.

Start with the tools that fit your needs and skip the rest. Canvas is optional, as are extra workers and multiple providers. “You” here means the person who cloned this repo.

## Pick a starting point

You need Python 3.11+ to use the selector. Listing and planning make no changes. Pulling copies a reviewed selection into a new folder and writes a manifest; it does not install tools or services, sign in, expose ports or enable jobs.

```sh
python3 scripts/bank.py list
python3 scripts/bank.py plan --preset personal-code
python3 scripts/bank.py pull --preset personal-code --output ../my-fleet-kit
```

| Preset | A useful start for | Leaves out |
| --- | --- | --- |
| minimal | Portable UI and writing skills | All services and account setup |
| personal-code | Local coding with T3 and build/review workflows | School, OpenClaw, proxy and tunnels |
| work-code | Coding in your employer-approved environment | Personal bridges, proxy and school workflows |
| student | OpenClaw, general Canvas planning and document review | Coding proxy, video and tunnels |
| remote | T3, private networking, friend previews and proxy profiles | School, assistant and video |
| creative | Design, video, resume and personal specialized bridges | School and remote networking |
| everything | The whole bank for reference | Nothing, but nothing is enabled |

Add modules or individual skills, or start without a preset:

```sh
# Coding with private remote access and a friend-preview recipe.
python3 scripts/bank.py plan --preset personal-code --module tailscale --module cloudflare

# Both kinds of Canvas, with only their required assistant setup.
python3 scripts/bank.py pull --module canvas-lms --module openclaw-canvas --output ../canvas-kit

# Just writing and resume help.
python3 scripts/bank.py pull --skill unslop --skill resume-craft --output ../writing-kit

# Skip a preset skill you do not want.
python3 scripts/bank.py plan --preset personal-code --skip-skill baseline-ui
```

Repeat `--module` or `--skill` for more choices. `--without MODULE` removes a module if no retained choice requires it. The selector reports conflicting exclusions rather than silently dropping a requirement. Dependencies are shown in the plan, including external tools you still need to install yourself.

## What's in the bank

Every recipe says when it helps, when to skip it, what setup is needed and how to verify it.

| Module | Why you might want it |
| --- | --- |
| [Coding agents](docs/modules/coding-agents.md) | Codex/Claude sessions in your repositories |
| [T3 Code](docs/modules/t3-code.md) | Desktop workspace, previews, delegated builds and reviews |
| [OpenClaw](docs/modules/openclaw.md) | Persistent assistant, browser work, channels and schedules |
| [Tailscale](docs/modules/tailscale.md) | Private remote workers, SSH and previews |
| [Cloudflare Tunnel](docs/modules/cloudflare.md) | Let friends open a preview without joining your tailnet |
| [Inference proxy](docs/modules/proxy.md) | Isolated gateway profiles and clients on several machines |
| [Fleet tools](docs/modules/fleet-tools.md) | Worktrees, build leases, immutable releases and profiles |
| [Canvas LMS](docs/modules/canvas-lms.md) | Explore schedules, reminders and organization through your own supported integration |
| [OpenClaw visual canvas](docs/modules/openclaw-canvas.md) | Visual documents, widgets and session dashboards |
| [Document/form reviews](docs/modules/document-reviews.md) | Review shared guides and form requirements |
| [Video](docs/modules/video.md) | Brag and HyperFrames launch-video/animation workflows |
| [Personal bridges](docs/modules/personal-bridges.md) | Image, 3D and visual browser QA through native personal Codex |
| [Provider skills](docs/modules/provider-skills.md) | Documents, research, browser, calendar, plugins and upstream discovery |
| [Assistant extras](docs/modules/assistant-extras.md) | Channels, memory, calendar, local models and glasses integration notes |
| [Legacy](docs/modules/legacy.md) | Deprecated setup examples and older multi-account references |

There are 22 bundled skills: 19 base fleet skills and three general assistant skills. [The skill catalog](docs/skills.md) describes them. Built-ins, synced organization skills and plugin-owned capabilities remain with their providers; the bank records how to discover them without copying private runtime directories.

The [full trifecta workflow](skills/orchestrate-trifecta/README.md) includes
redacted instructions and a configurable usage helper for three-account T3
builds and reviews. Map its provider placeholders and configure your own
usage gateways before running it. No account credentials are included.

## Ask your agent to help choose

You can open this clone in your coding agent and say:

> Read this repo's bank catalog and help me choose a small setup. I use [OS], want [coding / assistant / school agenda / friend previews], and already have [tools]. Keep personal and work accounts separate. Tell me what I can skip, preview the selection, and export only those pieces. Then help set up the modules I choose and verify each one.

The agent instructions support this workflow. It should reuse what you have, keep unrelated services intact and explain missing prerequisites. [HANDOFF.md](HANDOFF.md) is a longer prompt you can adapt.

## Set up your selection

Open the exported README and follow only the selected recipes. [Skill installation](docs/install-skills.md) explains destination choices. Some tools are external installs; some modules are reference recipes rather than bundled applications. No account, subscription, school login or hardware pairing comes with a clone.

If you choose fleet/proxy tooling, configure fleet.json with your own owner, addresses, accounts, SSH aliases, paths and protected services first. Starter values are examples. The proxy installer is a pinned Apple Silicon Mac workflow; other platforms need their documented client setup. Check model access on your own account.

Personal and employer code, memory and credentials stay separate. A work identity does not imply approval to use a personal proxy or Claude-to-personal-Codex bridge. Use your employer's approved environment for its work. Friends receive their own setup, never Ali's login state.

Cloudflare recipes are for sharing the intended app preview. Keep agent control interfaces, inference management and authenticated browser sessions private. Tailscale access and web-preview access are separate choices.

## Keep the bank shareable

Credentials, sessions, OAuth state, private memory, device grants, personalized Canvas config and generated agenda state stay outside Git. The selector exports only inventoried files and verifies their hashes, so ignored local files do not accidentally enter a kit. It refuses to replace an existing output.

For a source change, review it, stage the intended shareable files, refresh `bank/files.json` with `python3 scripts/index-bank.py`, then run the checks. The inventory is a reviewed-file list, not permission to include credentials. See [provenance](docs/provenance.md) for imported sources and verification limits.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check-public.py --history --secrets
```

These checks use offline fixtures and temporary homes. A friend's live T3, OpenClaw, model, school, tunnel and Windows setup still needs the selected recipe's own verification. Run fleet doctor after actual fleet profile setup, not on an unconfigured clone.

The public source check requires Gitleaks and checks history as well as current files. CI runs it on pushes and pull requests. See [public release checks](docs/public-release.md) for the review process and its limits.

The full Git checkout is the bank; an exported kit contains only the selection. To share a history-free snapshot after a reviewed commit:

```sh
(set -C; git archive --format=zip --prefix=shared-fleet/ HEAD > ../shared-fleet.zip)
shasum -a 256 ../shared-fleet.zip > ../shared-fleet.zip.sha256
```
