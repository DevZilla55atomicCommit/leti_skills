# Quick Check for Ollama Processes

## List Processes
- `ps -ef | grep -i ollama`

## Kill Daemon
- `killall ollama` or `pkill -f ollama`

## Verify No Processes Remain
- Run `ps -ef | grep -i ollama` again; ensure no output.

## Check Model List
- `ollama list`

## Test Model Serving
- `ollama serve`
- In another terminal: `curl -X POST http://127.0.0.1:11434/api/generate -d '{"model":"qwen3.5","prompt":"Hello"}'`