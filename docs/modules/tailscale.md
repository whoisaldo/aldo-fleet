# Tailscale

Choose this when your own computers need a private route for SSH, agents or previews. Friends can use a shared node or an explicitly allowed tailnet route; they do not need access to all your machines.

Install Tailscale from [the quickstart](https://tailscale.com/docs/how-to/quickstart) on each selected device and sign into your own tailnet. Confirm device names and addresses in the admin console. On a host with the CLI, `tailscale status` and `tailscale ip -4` identify the actual network state. Put those addresses and your own SSH aliases in fleet.json if using fleet tooling.

First verify ordinary SSH with your own user and key. Tailscale SSH is a separate optional access choice, not assumed by this repo. Test a disposable preview from the receiving device, not only from the host itself.

For a friend, [share the specific machine](https://tailscale.com/kb/1084/sharing) and review applicable grants/ACLs for the preview port. A shared device is not the same as sharing a single page. Give the friend a restricted app or preview, not a broad coding-agent/admin interface.

You can bind a preview to the actual tailnet address or use a local reverse proxy. Binding `0.0.0.0` also listens on other interfaces; review host firewall/access before doing that. Use the real address in the returned URL. A loopback-only server cannot be reached directly at its Tailscale IP.

Tailscale Serve is optional. Inspect `tailscale serve status` before configuring it and follow [Serve documentation](https://tailscale.com/kb/1312/serve) for an unused route. Do not reset an existing user's Serve mapping. Stop only the preview and route this task owns when finished.

Sources checked October 14, 2026: the official quickstart, node-sharing and Serve guides linked above.
