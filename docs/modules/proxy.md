# Inference proxy / CLIProxyAPI

Choose this for gateway-backed isolated profiles, shared model access across your own machines and observable request/cache usage. Skip it when native CLIs already meet your needs. An inference proxy is separate from a Cloudflare preview tunnel and from OpenClaw's assistant Gateway.

The bank retains the source CLIProxyAPI installer, pinned version/checksum, profile renderer, release/archive tooling and cache-check helpers. Upstream [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) documents the service's current behavior. This repo reproduces a specific tested configuration, not every latest upstream feature.

The included gateway installer targets Apple Silicon macOS. Configure fleet.json with your own Tailscale listener, runtime directory and expected sign-in email before using it. Keep its service label unless you also review the installer's allowlist. Inspect any existing service using that label first; never reuse another installation's runtime.

```sh
python3 scripts/gateway.py init --identity personal
python3 scripts/gateway.py login --identity personal --provider claude
python3 scripts/gateway.py login --identity personal --provider codex
scripts/fleet release
scripts/fleet diff --profile fleet-codex
scripts/fleet apply --profile fleet-codex
scripts/fleet diff --profile fleet-claude
scripts/fleet apply --profile fleet-claude
scripts/fleet doctor --profile fleet-codex --profile fleet-claude
```

Use fresh sign-ins. The gateway must own its refresh grant; never copy live native refresh credentials into it. Client and management keys are separate. Other machines receive client keys only through a private channel. Do not place either key in Git, the bank catalog, a preview URL or an exported config.

Native ChatGPT connectors/computer-use features may still require native authentication. The personal bridges deliberately use the native personal Codex home. A proxy endpoint does not supply a provider-native feature or school/work SSO.

The legacy reference preserves the optional secondary SSO setup, but it is not selected by the default profiles. The helper only implements its supported personal and secondary login paths. Do not rename the secondary SSO gateway to a friend's employer and assume it implements that company's authentication. Keep identities separate and report quotas without silent fallback.

Configure T3 providers separately through the supported settings API if using T3. Confirm each model works on your account with an explicitly chosen short test; catalog presence alone is insufficient. Relevant offline deployment tests do not prove your live account access.
