# Install only selected skills

A bank kit is source, not an installation. Use its selection.json and README to find the chosen folders. Keep full folders, including scripts, references, licenses and assets. Preserve existing customized destinations and provider-owned skills.

| Target | Destination choice |
| --- | --- |
| Codex | A supported project or personal skill root, such as project `.agents/skills/` |
| Claude Code | Project `.claude/skills/` or personal `~/.claude/skills/` |
| OpenClaw | Your configured workspace `skills/`, or its supported skill installer |

Confirm the actual locations in your installed provider. For Codex, `.claude-only` bridges are excluded; for employer work, exclude personal bridges entirely. The four optional skills under bank/skills are designed for OpenClaw/browser/Notion workflows, so do not assume they execute in another harness unchanged.

Example from a selected kit, for personal Claude:

```sh
mkdir -p ~/.claude/skills
# Existing files and symlinks are preserved.
test ! -e ~/.claude/skills/unslop && test ! -L ~/.claude/skills/unslop && cp -R skills/unslop ~/.claude/skills/unslop
```

For a vendor skill, use its selected vendor/skills/NAME directory. For an optional assistant skill, use bank/skills/NAME. For an OpenClaw custom skill, copy the selected folder into your configured custom skills location. For example:

```sh
mkdir -p ~/.openclaw/skills
test ! -e ~/.openclaw/skills/canvas-planning && test ! -L ~/.openclaw/skills/canvas-planning && cp -R bank/skills/canvas-planning ~/.openclaw/skills/canvas-planning
openclaw skills check
```

Inspect its output and start a fresh conversation. Do not force-overwrite a customized skill. Canvas planning is a capability guide. Connecting live services requires your own supported integration; keep any account configuration outside this checkout.

Fleet profiles are an alternative deployment route for selected base skills. Read the fleet-tools and proxy recipes before using apply. Built-in, synced and plugin skills are managed by their provider rather than copied from another account.

Sources checked October 14, 2026: [Codex skills](https://developers.openai.com/codex/skills), [Claude skills](https://code.claude.com/docs/en/skills), [OpenClaw skills](https://docs.openclaw.ai/tools/skills).
