# Orchestrate trifecta, shareable copy

A T3 workflow that splits coordination, building, and review across three
accounts. This folder is a redacted export. It does not install or change
any account, gateway, or running workflow.

## Contents

- `SKILL.md`: the workflow, with provider IDs replaced by placeholders.
- `scripts/usage.py`: the usage helper, with local paths and addresses removed.
- `.claude-only`: the original empty skill marker.

## Setup

1. Use your own T3 environment with `delegate_task` and
   `orchestrator_capabilities`. These tools are not included in this archive.
2. Map the provider placeholders in SKILL.md to your own selected accounts.
   Choose available model IDs from the live catalog.
3. Install the skill folder under your own Claude skills directory if desired.
4. Configure the usage helper only if your gateway supports the same
   `/v0/management/auth-files` API and quota fields. Otherwise adapt the helper
   to your own provider's usage interface before relying on it.

The helper reads these environment variables:

- Coordinator: `TRIFECTA_COORDINATOR_GATEWAY_URL`, `TRIFECTA_COORDINATOR_KEY_FILE`
- Builder: `TRIFECTA_BUILDER_GATEWAY_URL`, `TRIFECTA_BUILDER_KEY_FILE`
- Reviewer: `TRIFECTA_REVIEWER_GATEWAY_URL`, `TRIFECTA_REVIEWER_KEY_FILE`

Each URL is your own gateway endpoint. Each key-file variable points to your
own local JSON file with a `management_key` field. No key files are included.
Use the documented header mappings as a starting point, and verify that the
5-hour and weekly windows match your accounts.

Without configuration, `python3 scripts/usage.py --json` reports the missing
variables and does not make network requests. With configuration, it reads
usage only. It does not sign in, switch accounts, or start agent tasks.

## Redactions

Removed the original user's name, school and employer names, private provider
IDs, machine address, runtime-directory paths, and local fleet instructions.
No embedded API keys were found in the original two files. The original
helper loaded a management key from a private local file at runtime. That
file and all other credentials, tokens, and account state are excluded.
