---
name: remote-handoff
description: Prepare and verify a development task on a configured remote Mac or Windows worker. Use when work needs another machine or native Windows display testing.
---

Read the target in the fleet checkout's `fleet.json` and machine notes. Verify SSH with a bounded noninteractive read before changing it. If offline, prepare the handoff and report deployment as pending.

Use the target's configured work root and inspect any existing persistent launcher's documented arguments. Do not assume the original owner's jobs, profiles or scheduled tasks exist. GPU/display tests must run in the user's logged-in interactive Windows session; SSH cannot validate that display.

Record the selected account, repository origin, commit or worktree, task instructions and completion criteria. Keep employer tasks on employer-approved hosts and providers. Distinguish native jobs from T3 threads and confirm visibility before claiming it.

Return the host, job or thread identifier, artifact location and checks. Preserve unrelated processes and reuse the existing T3 instance without switching running threads' accounts.
