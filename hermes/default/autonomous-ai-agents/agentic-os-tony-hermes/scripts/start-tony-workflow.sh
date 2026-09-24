#!/usr/bin/env bash
# Start TONY Agentic OS gateway and open JARVIS dashboard in Chrome app mode
# Usage: ./start-tony-workflow.sh [stop|restart|status|logs]

set -euo pipefail

PROJECT_DIR="/Users/alfredkamisese/tony-ai-agent"
PORT=8787
API_TOKEN="tony-hermes-local-2026"
LOG_FILE="$PROJECT_DIR/tony-gateway.log"
PID_FILE="$PROJECT_DIR/tony-gateway.pid"
HERMES_NODE="/Users/alfredkamisese/.hermes/node/bin/node"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

kill_existing() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null || echo "")
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            log_info "Killing existing gateway (PID: $pid)"
            kill -9 "$pid" 2>/dev/null || true
        fi
    fi
    lsof -tiTCP:$PORT -sTCP:LISTEN 2>/dev/null | xargs -r kill -9 2>/dev/null || true
    sleep 1
}

wait_for_health() {
    local max_wait=30
    local waited=0
    log_info "Waiting for health endpoint..."
    while (( waited < max_wait )); do
        if curl -s -f "http://localhost:$PORT/health" -H "Authorization: Bearer $API_TOKEN" >/dev/null 2>&1; then
            log_info "Health check passed!"
            return 0
        fi
        sleep 1
        (( waited++ ))
    done
    log_error "Health check timed out after ${max_wait}s"
    log_error "Check log: $LOG_FILE"
    return 1
}

show_status() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null || echo "")
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}TONY gateway is RUNNING${NC} (PID: $pid, Port: $PORT)"
            curl -s "http://localhost:$PORT/health" -H "Authorization: Bearer $API_TOKEN" 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'  Chain: {\" -> \".join(d[\"llmChain\"][\"chain\"])}')
    print(f'  Model: {d[\"llm\"]}')
    print(f'  Online: {d[\"online\"]}')
    print(f'  Skills: {d.get(\"skills\",0)}')
    print(f'  Brain nodes: {d.get(\"mind\",{}).get(\"graphify\",{}).get(\"nodes\",0)}')
except: pass
" || echo "  (health check failed)"
            return 0
        fi
    fi
    if lsof -tiTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
        echo -e "${YELLOW}TONY gateway RUNNING (orphaned)${NC} on port $PORT"
        return 0
    fi
    echo -e "${RED}TONY gateway is STOPPED${NC}"
    return 1
}

start_gateway() {
    cd "$PROJECT_DIR"

    local NVIDIA_API_KEY=$(grep '^NVIDIA_API_KEY=' .env | cut -d= -f2)
    if [[ -z "$NVIDIA_API_KEY" ]]; then
        log_error "NVIDIA_API_KEY not found in .env"
        exit 1
    fi

    log_info "Starting TONY gateway on port $PORT..."
    log_info "Using NVIDIA_API_KEY: ${NVIDIA_API_KEY:0:12}..."

    NVIDIA_API_KEY="$NVIDIA_API_KEY" nohup "$HERMES_NODE" src/gateway/server.js >> "$LOG_FILE" 2>&1 &
    local pid=$!
    echo "$pid" > "$PID_FILE"

    log_info "Gateway started (PID: $pid)"
    log_info "Log: $LOG_FILE"
    log_info "PID file: $PID_FILE"
}

open_dashboard() {
    log_info "Opening JARVIS dashboard..."
    open -a "Google Chrome" --args \
        --app="http://localhost:$PORT/jarvis?token=$API_TOKEN" \
        --window-size=1400,900
}

case "${1:-start}" in
    start)
        if show_status >/dev/null 2>&1; then
            log_warn "TONY gateway already running"
            show_status
            open_dashboard
        else
            kill_existing
            start_gateway
            wait_for_health && show_status && open_dashboard
        fi
        ;;
    stop)
        log_info "Stopping TONY gateway..."
        kill_existing
        [[ -f "$PID_FILE" ]] && rm -f "$PID_FILE"
        log_info "Stopped."
        ;;
    restart)
        kill_existing
        start_gateway
        wait_for_health && show_status && open_dashboard
        ;;
    status)
        show_status
        ;;
    logs)
        tail -f "$LOG_FILE"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac