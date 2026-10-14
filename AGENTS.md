# Shared fleet

This is a selectable recipe and skill bank. Read `bank/catalog.json` and `README.md` before setup. Identify the user's OS, goal, selected personal/work identity, existing tools and whether they use either Canvas feature. Reuse known preferences; ask only for missing choices that affect setup. Suggest a small selection and explain why unrelated modules can be skipped. Use `scripts/bank.py plan` and export the selection with `pull` to a new folder. Selection/export is preparation, not authority to sign in, install services, expose endpoints, enable schedules or replace an existing setup. When the user requests setup of a chosen module, carry the authorized steps through its documented checks. Do not make them approve routine preparation twice.

Read `fleet.json` for the owner's configured machines, profiles and protected services. Read `README.md` for setup and commands. Addresses and usernames in the starter configuration are examples, not reachable hosts.

## Accounts and machines

Choose the machine and account at thread creation. Keep personal and employer identities, repositories, memory and artifacts separate. For employer work, use the user's approved work environment and provider. Do not route work through a personal gateway or the personal Claude-to-Codex bridges. Do not infer permission to access internal systems from the user's employer. Report account exhaustion without changing identity.

Use a configured Mac for macOS/iOS/browser work and a configured Windows worker for native Windows/GPU/display checks. Display checks require the owner's interactive login. A single Mac is enough to start; extra workers are optional.

## Existing work

Work in a separate task worktree. Touch only the task's files and processes. Never use process-name kill commands, restart T3, change Tailscale Serve, replace provider settings, or launch a second backend against a live T3 home. Additive provider changes use the supported settings API and preserve existing entries.

Define completion from the request, run the relevant checks, and provide a reviewable result. Remote previews bind to `0.0.0.0` only on a configured trusted network; return the actual reachable address. Save screenshots and give their paths. Do not assume the user sees an opened GUI.

Requests to prepare work do not authorize merging, publishing or messaging others. Keep questions for the user out of PR bodies and commit messages. Author commits as the repository's configured human owner, without agent attribution or co-author trailers.

## Configuration and validation

Fleet-owned source lives in `skills/`; vendored skills and hashes are in `vendor/skills` and `skills/external.lock.json`. Preserve built-in, plugin-owned and organization-managed skills under their providers' control. Credentials, sessions, OAuth state, private memory, backups and logs stay outside Git. Use fresh gateway sign-ins, never copied refresh credentials.

Run `scripts/fleet diff --profile NAME` before applying to a new managed home. Never replace native homes or update a profile with history through ordinary apply. Use the documented idle migration for an existing installation only when authorized. Preserve explicit model and reasoning choices in the image, 3D and computer-use skills.

Run `python3 -m unittest discover -s tests -v` after deployment changes. Tests use temporary homes and repositories. Run `scripts/fleet doctor` after actual local setup changes. Historical files under `imports/`, `examples/legacy-fleet.json` and `docs/legacy-reference.md` are reference material, not installation instructions.

For changes in the full bank source checkout, review all added files and media, stage the selected changes, refresh `bank/files.json`, and run `python3 scripts/check-public.py --history --secrets`. Selected kits use `bundle-manifest.json` and their module checks. Keep findings and private audit reports outside Git. Never treat a clean scan as permission to publish credentials or personal state. See `docs/public-release.md`.
