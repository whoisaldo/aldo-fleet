# Legacy Windows deployment reference

Follow the current [Windows deployment guide](windows-deployment.md). The legacy module retains older script shapes for inspection.

Use `D:\AgentWork` for new checkouts, tools, caches and build output, with private profile state in a separate directory. Transfer a reviewed skill release archive and verify its SHA256 before importing it. Keep archives outside the repository.

Transfer only the selected gateway's inference client key through an authenticated private channel. Never copy management keys, gateway OAuth state or native credentials to another worker. Keep deploy keys outside Git and scope them to the intended repository.

Installers must preserve existing global CLIs, native profiles, launchers and scheduled tasks. Confirm the ordinary interactive Windows user can read new state; an elevated SSH installation may otherwise create unusable ACLs. Verify a fresh conversation and follow-up after setup.

Add T3 providers through its supported authenticated settings API and preserve existing entries exactly. Native GPU/display tests require the worker's interactive session. Installing workflow files does not authorize restarting T3 or changing Tailscale Serve.
