# T3 Code

Choose this for a desktop workspace around coding providers, collaborative previews and delegated build/review work. Skip it if your terminal or IDE is enough.

1. Install the Stable or Nightly desktop build from [T3 Code downloads](https://t3.codes/download) for your platform. Stable is a reasonable starting point; the source owner uses Nightly.
2. Authenticate your chosen provider on the machine running the agent. Add your repository as a project and start one short test thread.
3. Check the available provider/model picker rather than copying the original owner's instance IDs.
4. Add portable skills to the appropriate agent or project location. The optional `orchestrate-trifecta` skill uses the live T3 catalog for child tasks and independent review.
5. For remote workers, first make SSH and private network access work. Keep an ownership note for the existing backend, its home and port.

A delegated task is child work, not a new top-level conversation. Retain task IDs, and make a new delegated task for each review round. Starting a thread does not authorize publishing its work.

The source setup uses desktop-owned T3 on 3773, with a separate phone forwarder on 3774. These are reference port choices, not ports this bank opens. Never start another server against an existing live T3 home, restart a user's instance or replace its providers during setup. `scripts/t3-api.mjs` and `scripts/check-t3.py` are optional helpers for a configured installation; inspect their help and local session requirements before use.

For friends reviewing an app, expose the app preview rather than your coding-agent control server. Use the Tailscale or Cloudflare recipe for that preview.

Source checked October 14, 2026: [official desktop and terminal downloads](https://t3.codes/download).
