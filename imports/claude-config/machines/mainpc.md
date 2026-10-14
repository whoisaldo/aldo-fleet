# Example Windows worker

Configure your worker's user, SSH alias, address and work root in fleet.json. Resolve its home from $env:USERPROFILE. Use D:\AgentWork for new projects, dependencies, caches and build output.

Native GPU, capture and display tests require the worker's logged-in interactive session. An SSH shell is a different session; record when a physical test cannot run. Do not substitute a synthetic check for a real display test.

Keep work and personal profiles separate. Preserve existing T3 services, provider entries, databases and Tailscale Serve. Do not start another backend against a live home. For remote previews use the configured trusted interface and report a verified URL; save screenshots and give their paths.

Author commits using the repository's configured human identity, without co-author trailers or agent attribution.
