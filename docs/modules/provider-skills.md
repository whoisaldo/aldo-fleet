# Provider-owned and external skills

The bank includes custom reusable source and keeps provider-owned capabilities in their original distribution. A friend discovers or installs these through their own provider, with their own account. Do not copy the original owner's `.system`, synced organization directories, plugin caches or connector grants.

Observed Codex built-ins include imagegen, openai-docs, skill-creator, skill-installer and review-agent. Availability depends on the installed provider version. Observed Claude synced capabilities include morning, deep-research, xlsx, pdf, docs, docx, pptx, import-memory, google-workspace, chrome-browser, built-in-browser, computer-use, web-artifacts-builder and skill-creator. These names describe a source account's inventory, not an entitlement supplied by the bank.

Claude plugin preferences retained under profiles include Vercel, Swift LSP, Rust analyzer and brag. Review/remove preferences you do not want before applying a personal profile. Install plugins through the provider's plugin manager.

`bank/openclaw-source-catalog.json` lists examples of optional assistant capabilities. Use `openclaw skills list` and `openclaw skills check` on your own installation to discover available tools and missing dependencies.

Notion/Calendar, Discord, browser and document tools are useful independently of Canvas. Install the official [Notion companion](https://github.com/makenotion/skills) or your provider's calendar connector if wanted. Broader [Anthropic skills](https://github.com/anthropics/skills), [HyperFrames](https://github.com/heygen-com/hyperframes) and [brag](https://github.com/latent-spaces/brag) remain upstream sources with their own licenses and installers.

Legacy third-party Discord skill copies remain upstream-owned rather than being imported from a private backup. Use OpenClaw's supported channel/plugin distribution for your installed version.
