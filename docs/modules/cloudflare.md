# Cloudflare Tunnel for friends

Choose this when someone needs an HTTPS preview without joining your tailnet. Tailscale handles private machine access; Cloudflare Tunnel gives a web service an external route. Neither grants your friend model credentials or access to your agent.

Install cloudflared using [Cloudflare's guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/). Start the intended app locally, for example on `http://127.0.0.1:3000`, and check that it works before tunneling it.

For a temporary preview, current Quick Tunnel documentation supports restricting the visitor by email:

```sh
cloudflared tunnel --url http://127.0.0.1:3000 --allowed-mail friend@example.com
```

Replace the sample email. Check your installed version's help for `--allowed-mail`; if unavailable, use a named Tunnel with Access instead of treating an unprotected URL as private. A plain `--url` tunnel can be opened by anyone with the generated URL. Stop the foreground tunnel with Ctrl+C when finished. No account/domain is needed for Quick Tunnels, but they have changing hostnames, no uptime guarantee and do not support SSE. This can make them unsuitable for streaming apps.

For a stable friend preview, create a named Tunnel in your own Cloudflare account, map a hostname you control to the local app, and create a self-hosted Access application allowing only your chosen visitors. Verify denied access in a signed-out browser and successful access as an allowed visitor. Keep application authentication where it exists. Test WebSocket/streaming behavior for the actual app.

`bank/examples/cloudflared.yml` is a local-management reference with placeholders and a final 404 rule. It is not automatically merged or run. A dashboard-managed tunnel uses its own configuration. Tunnel credentials and service tokens stay outside the repo.

Expose the app you intend to share. Keep inference proxy management, raw OpenClaw Gateway, Canvas browser sessions and T3 control services private. A coding-agent control interface can grant file and command access beyond the preview.

Sources checked October 14, 2026: [Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/), [Tunnel setup](https://developers.cloudflare.com/tunnel/get-started/), [self-hosted Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/).
