# mainpc

Optional Windows worker. Set the actual host and user in `fleet.json`. The Windows bootstrap currently expects `D:\AgentWork`; inspect that workflow before using another drive. Native GPU/display tests require the logged-in interactive session. Inspect existing job launchers rather than assuming the original owner's scheduled tasks exist.
