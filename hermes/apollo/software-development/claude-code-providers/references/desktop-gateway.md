# Claude Desktop app: third-party inference gateway

When the Claude Desktop app (not the CLI) must serve a local model instead of api.anthropic.com: Developer menu → Configure Third-Party Inference → provider Gateway, base URL, placeholder API key, Bearer auth, exact model id in the model list.

## Where the config lives

- Active file is `~/Library/Application Support/Claude-3p/configLibrary/<id>.json` (the `3p` deployment-mode profile; the active `<id>` is `appliedId` in `_meta.json`). Back it up before hand-editing.
- Load-bearing fields: `inferenceGatewayBaseUrl`, `inferenceGatewayApiKey`, `inferenceProvider: gateway`, `inferenceCredentialKind: static`, and `inferenceModels` — family-tier slots (`name` Sonnet/Opus/Haiku plus `anthropicFamilyTier`) with `labelOverride` carrying the display name / model id.
- Prefer the Developer-menu UI for edits; a full quit + reopen is required after any change regardless of which path wrote it.

## Procedure

1. Probe before wiring: `GET /v1/models` on the candidate base URL, then `POST /v1/messages` with `max_tokens: 10` and the EXACT model id. A structured unknown-model error proves the protocol path but disproves servability of that id on that port — move ports, not goalposts.
2. Set Gateway base URL to the Ollama-app proxy (`http://127.0.0.1:11435`), key to any placeholder (e.g. `ollama`), auth to Bearer — current Desktop versions send Claude-named model ids (e.g. `claude-sonnet`) and validate the Model ID field as an Anthropic route, so raw Ollama on :11434 answers 404 `model 'claude-sonnet' not found` for Desktop traffic.
3. In the Ollama app, switch Claude ON (it writes the gateway config itself) and map each tier under Settings → APPS → Claude: one popup per tier (Fable 5, Opus 5, Sonnet 5, Haiku 4.5, Sonnet 4.6), each defaulting to a `:cloud` model. Open the tier's popup, use its Find field to filter, and pick the local model (local entries list without a `:latest` tag, e.g. `qwen3.5-32k`). Set every tier Desktop will request — the Sonnet slot resolves to the proxy's family-default `sonnet` route, so map both Sonnet popups when in doubt. Then re-probe `:11435/v1/models` and use the exposed `claude-*` route id as the Model ID — typing a raw Ollama id fails validation (`expected a gateway model route referencing an Anthropic model`). Keep at least one `inferenceModels` entry: an empty list with `modelDiscoveryEnabled: false` yields an empty picker, and re-applying the config can wipe entries, so re-verify the list after every change.
4. Relaunch the app completely, choose Continue with Gateway, and send one test message in a Code/Cowork tab.

## Pitfalls

- Two local servers share the Ollama name with different catalogs: `ollama serve` on :11434 exposes raw Ollama ids (right for the CLI, wrong for Desktop), while the Ollama Desktop app on :11435 serves a Claude-aliased catalog (right for Desktop) — a gateway pointed at :11434 fails Desktop chats with 404 because Desktop sends Claude-named ids, so verify the port serves the id you configured with step 1 before debugging anything else.
- `ollama cp <model> <claude-style-name>` presents a model under a validator-acceptable name at zero disk cost (shared blob) — useful for raw endpoints and the CLI, but it does not fix Desktop traffic, which still arrives with Desktop's own Claude names and needs the :11435 proxy to translate.
- `ollama launch claude-desktop` is restore-only from the CLI (`--restore`); it cannot set the tier-to-model mapping — that mapping is GUI-only in the Ollama app, so do not offer the CLI as an alternative path for it.
- Gateway mode yields Cowork and Code tabs only; the Chat tab, Connectors, and web search are unavailable on this path — that is the mode's ceiling, not a misconfiguration. Claude Design (sidebar Design / claude.ai/design, Pro-or-higher plan) is likewise Anthropic-server-side with its own allowance and never runs on local models — to use it, toggle Claude OFF in the Ollama app and relaunch Desktop onto the normal Anthropic path, then toggle back ON to restore local routing.
- After changing any tier mapping, click Restart Claude in the Ollama app's Claude section so the :11435 proxy serves the new catalog, then fully quit and reopen Claude Desktop — the proxy and the app each cache the old mapping otherwise.
- Plugin skills (prompt methodology) keep working in gateway mode, including on small local models; plugin connectors (Drive, Slack, Gmail) reach services through Anthropic's cloud and stay dead until Desktop is back on the Anthropic path. Judge a plugin in gateway mode by its skills, not its connectors.
