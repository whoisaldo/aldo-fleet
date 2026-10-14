---
name: fleet-operate
description: Inspect or configure the user's fleet machines, profiles, shared skills or gateway. Use for fleet maintenance and machine routing, not ordinary application edits.
---

Find the fleet checkout from the current project and read its `fleet.json`, `AGENTS.md` and `README.md`. Resolve actual hosts and account homes there; never assume the starter addresses are live.

Preserve unrelated agents, native profiles, existing T3 sessions and provider entries. Do not restart T3 or change Tailscale Serve as a side effect. Route by required OS and selected account. Employer work stays in the approved employer environment; quota exhaustion is reported without switching identities.

Change source in fleet and run deployment tests. Preview a profile with `scripts/fleet diff --profile NAME`. Publish a content-addressed local release and apply only to a new or unused managed home. For an authorized idle migration, follow `docs/maintenance.md`, preserve histories and settings, and back up changes. Credentials stay outside Git; gateway sign-ins are fresh.

Return the affected host, exact files or services changed, validation and any remaining setup. Do not claim an untested remote deployment succeeded.
