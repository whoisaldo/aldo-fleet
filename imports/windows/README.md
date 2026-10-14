# Historical Windows helpers

These optional scripts show patterns for putting tools and build output under D:\AgentWork, separating profiles and launching interactive tasks. Adapt paths, SDK versions and task names to your worker before use. They are not part of the current bootstrap.

The example application is ExampleApp. Its build and hardware scripts require that application's code, toolchain and interactive display; they are templates rather than runnable sample projects. Confirm every command and prerequisite before using them.

Use the current [Windows deployment guide](../../docs/windows-deployment.md) for fleet setup and [T3 recipe](../../docs/modules/t3-code.md) for the app. Preserve live services and provider entries. Session records, device fingerprints, pairing links, authentication, logs and test evidence belong outside Git.

Verify SSH host keys through a trusted channel. For GPU/display tests, confirm an interactive login; SSH command success does not establish access to a physical display. Return saved screenshots and reachable preview URLs to a remote operator.
