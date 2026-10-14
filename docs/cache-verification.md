# Check prompt caching

Use a fresh two-turn conversation on the intended identity. Ask the provider to read a harmless local test marker, then repeat it without tools. Inspect the provider's request usage for cache reads and writes. Keep the test transcript outside Git.

```sh
python3 scripts/check-cache.py --profile fleet-codex
python3 scripts/check-cache.py --profile fleet-claude
```

For an optional second gateway, select its configured profile explicitly. Never change identity because another account reached its quota.

Claude input accounting includes cache reads, cache writes and uncached input. Codex completion usage can be cumulative across resumed sessions; the helper reads `last_token_usage` for the individual request. Tests cover this distinction. A short conversation's hit rate does not promise the same rate for every task.

Gateway session affinity keeps related requests on the same account. Its routing TTL does not extend the provider's cache lifetime. Keep one refresh owner per fresh OAuth sign-in; separate identity pools prevent accidental cross-account fallback. Check key isolation with `fleet doctor`, which does not invoke an agent.

Keep request/debug logs disabled unless troubleshooting calls for them. Model catalog presence does not establish subscription entitlement: verify a chosen model using that account before depending on it. Reports belong in the configured private fleet state directory.
