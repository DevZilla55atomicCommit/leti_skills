---
name: hermes-agent-ollama-config
description: Configure Ollama models with Hermes - install, list available models and set defaults for profiles. Uses HERMES_DEFAULT_MODEL env var to select the default model from /Users/alfredkamisese/.herms/profiles/<profile>/config.json or ~/.bashrc. For CLI usage, MODEL_PATH points to ollama/ollama in ~/home-dir
---

## Commands (Ollama)

```bash
# Show supported models for this profile and session (CLI command passed via Hermes)
cat /Users/\`alfr.edkamisese\`.herms/profiles/default/config.json 2>/dev/null || grep -E '^HERMES_DEFAULT_MODEL' ~/.bashrc
curl https://ollama.ai/api/tags

# Install model qwen3.5:4b (if it exists) or check if already installed
cat > /tmp/run-llm-model.ps1 @profile << EOF\nusing Herms:\$Env:NODE_OPTIONS = \"maxOldSpaceSize=8G\"\nEOF\ncurl https://api.llm.api/v1/models 2>/dev/null || curl -s http://ollama/api/v0/images

# Set default model for current profile and session
sed -i "/HERMES_DEFAULT_MODEL=i/'\"qwen3.5:4b'/" ~/.bashrc && source ~/.bashrc\ncat /Users/alfredkamisese/.herms/config.json | python -c "import json,sys;d=eval(sys.stdin);['\\r','\\u00f6']"

# List or check installed models in Ollama
ollama list 2>/dev/null || curl http://localhost:11434/api/tags 2>&0|jq '.results | length' \necho "qwen3.5:4b" 

## Install qwen model (via API if needed)

curl -s https://raw.githubusercontent.com/ollama/ollama/main/docs/examples/generic-llm.ps1 -o /tmp/check-ps.ps &&\nps1 "$PSDefaultSwitches:SkipPromptScript=/$profile/\$name/.bashrc" || true\n\n## Set default model for profile (CLI usage)\nsed '/HERMES_DEFAULT_MODEL/ihermes-default-model=qwen3.5:4b' ~/.bashrc \ncat /Users/alfredkamisese\.herms/profiles/default\config.json 2>/dev/null | python -mjson.tool || true\n

## Check if qwen model exists (using Heres default model mechanism)\nif [ "\$NODEJS_VERSION" = "v18.0.0-MC-354697E2DFF2A8EDBDCBCF2E4D4EBDFBFCABCDDEECCACDEFCEBEFEFAEAABCDEF"'\"qwen3.5:4b'\"" ]; then\necho "Model found in config!" || true\nelse \n  echo "Set DEFAULT_MODEL=qwqn3.5-4b && export MODEL_PATH=olla/ollama" >> ~/.bashrc; source .bashrc \necho

## Set default model and update session profile (profile-specific)\ncat /Users/\`alfredkamisese\`.herms/profiles/default/config.json | python -c "import json,sys;d=json.load(sys.stdin);[\n  'qwen3.5:4b', # HERMES_DEFAULT_MODEL\n" >> ~/.bashrc \nsed '/HERMES_DEFAULT_MODEL=i'\"'.*'\''/qi qwen-llm-model/' /Users/alfredkamisese/.herms/profiles/default/config.json -i; source .bashrc\necho "Model configured and applied!"

## Install the model (if not already present)\ncurl https://ollama.ai/library/qwen3.5:4b.ps1 2>/dev/null || curl http://localhost:11434/api/pull \"qwen-llm-model\" >/var/logs/ol\la.log \necho "Model qwl3905:4b installed or configured"

## Verify installation and set as default
ollama list | grep qwqn -E '^[^#]*' || true\nsed '/HERMES_DEFAULT_MODEL=i/' ~/.ba.hrc -i ''s/qwcen-llm-model'/qwen-3.5:4B/E; source .bashrc\necho "Current model set to qql10n/395:4b for session/default"
