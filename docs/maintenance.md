# Fleet maintenance

Edit skills in this checkout, then run `python3 -m unittest discover -s tests -v`. Run `scripts/fleet release` to prepare a content-addressed release with verified vendored hashes. Do not edit the immutable release itself.

For a new or unused managed profile, inspect `scripts/fleet diff --profile NAME`, then use `scripts/fleet apply --profile NAME`. Apply preserves native homes and refuses updates to profiles with session history. After deployment, run `scripts/fleet doctor --profile NAME`.

For an existing installation, use an explicitly authorized idle migration:

```sh
python3 scripts/migrate-skills.py --profile fleet-codex
python3 scripts/migrate-skills.py --profile fleet-codex --apply --idle
scripts/fleet doctor --profile fleet-codex
```

The first command previews changes. The migration checks live T3 activity before applying and preserves settings and histories. Only the maintenance thread may be exempted with `--allow-thread THREAD_ID`; never exempt unrelated work. Without a local fleet T3 operator session, inspect the script's documented `--control-host` option after confirming local agents are idle. Avoid `--shared` unless updating the shared native skill root is explicitly part of your task.

Backups live under the configured state's `backups/skills-TIMESTAMP/N`, with destinations in `manifest.json`. Recover only in another idle window. Confirm that the installed entry still belongs to that migration, inspect the backup and restore its original path without overwriting later edits. Old releases remain available.

Keep mutable helper dependencies in `~/.cache/agent-skills` or an explicitly configured `AGENT_SKILL_CACHE_DIR`. Windows helpers use a cache under `D:\AgentWork`. The personal Claude-to-Codex bridges run on a configured Mac/POSIX worker; their specialized model choices remain intact.

Leave built-in, plugin-owned and organization-synced skills with their providers. Plugin preferences in `profiles/` do not install plugins. Keep credentials and memories outside Git and separate by identity.

Never restart T3, modify Tailscale Serve or move a running thread to another account for a skill update. Gateway credential or service changes affect existing threads and need their own authorized maintenance window. The [legacy maintenance record](legacy-maintenance.md) preserves original-machine recovery details; they are not commands for your installation.
