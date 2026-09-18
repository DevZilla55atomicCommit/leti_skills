# Free-tier gateways (Anthropic-compatible proxies)

Method for exposing free-tier models (e.g. OpenCode Zen behind a localhost translating proxy) to Claude Code. Catalogs and quotas change; the verification pattern below does not.

## Procedure

1. Confirm the gateway speaks Anthropic before wiring anything: `POST /v1/messages` with `max_tokens: 10` on a free model. A structured model error (400 unknown-model) still proves the protocol path; a 500 twice, in both dialects, means unservable — report that plainly instead of reframing it.
2. Catalog membership does not equal servability: list `/v1/models`, then probe the EXACT model id through the gateway. Hard allowlist rejects (e.g. a proxy serving 5 of 70 catalog models) are final for that path — do not present the rejected model as available.
3. Run a bill-path audit before wiring: the picker must expose ONLY free-suffixed ids, and requests must authenticate as the shared free pool rather than the user's personal key. Confirm the personal key is unused and say so explicitly.
4. Set context numbers from documented values where known (mark the source); otherwise conservative undershoot (e.g. 128k) labeled unverified in the picker description — undershoot only compacts early, overshoot breaks sessions.
5. Treat 429 / "model unavailable" as upstream capacity, never as config — retry later, fall back to local models, and say which one it is. A retry that succeeds proves transience; persistent failure across models and time proves outage.
6. Daemonize translating proxies (LaunchAgent with KeepAlive + RunAtLoad on macOS; kill the manual foreground process first to avoid port conflicts) and add a pre-launch `/health` guard in the switcher that prints the restart command instead of failing mysteriously.
