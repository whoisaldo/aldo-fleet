# Assistant extras

These are optional assistant capabilities, available as recipes. Pick each independently after OpenClaw works locally.

## Channels and schedules

Discord and other messaging channels use your own bot credentials, recipient allowlist and pairing. Configure one test channel before adding recurring jobs. Review delivery destinations so a personal assistant never sends work data into a personal channel. The bank's daily-brief template remains disabled; review timezone, recipient and model costs before creating a real schedule.

## Memory and calendar

Keep durable memory and indexes outside Git, separated by identity. Enable the memory/search features supported by your installed version, and check retrieval with a harmless example. Never import the source owner's conversation memory. Calendar access is a connector grant, not a skill file; connect your own calendar and verify one read before allowing edits.

## Local models and Blender

Ollama/local embeddings are optional services, independent of the inference proxy. Verify the installed model and whether the selected task supports it. A configured Blender MCP should identify the intended instance; do not attach an agent to a shared Blender accidentally. Specialized bridge model requirements still apply.

## Even G2 glasses / Evenband

An optional custom Evenband bridge can display calendar/tasks and short notes on Even G2 glasses, with an optional assistant handoff. This bank does not ship the separate bridge application, device keys or pairing. If you own that hardware, deploy the bridge's own source through its documented project workflow, set a private endpoint and pair your device. Verify a harmless status read and one user-requested note. An installed glasses skill without that bridge is not a working glasses connection.

Remote assistant access should use a supported private route, for example the [OpenClaw Tailscale guide](https://docs.openclaw.ai/gateway/tailscale). Do not copy stale account-failover instructions from personal memory; select authorized identities and report quota exhaustion.
