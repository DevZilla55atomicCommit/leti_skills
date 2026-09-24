#!/usr/bin/env bash
# Start TONY-AI-Agent gateway server
# Usage: ./start-tony.sh [stop|restart|status]

set -euo pipefail

PROJECT_DIR="/Users/alfredkamisese/TONY-AI-Agent"
PORT=8787
API_TOKEN="tony-hermes-local-2026"
LOG_FILE="$PROJECT_DIR/tony-gateway.log"
PID_FILE="$PROJECT_DIR/tony-gateway.pid"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
function log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
function log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

function kill_existing() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null || echo "")
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            log_info "Killing existing gateway (PID: $pid)"
            kill -9 "$pid" 2>/dev/null || true
        fi
    fi
    # Also kill anything on the port
    lsof -tiTCP:$PORT -sTCP:LISTEN 2>/dev/null | xargs -r kill -9 2>/dev/null || true
    sleep 1
}

function start_gateway() {
    cd "$PROJECT_DIR"
    
    # Load NVIDIA_API_KEY from .env to override inherited shell env
    local NVIDIA_API_KEY=$(grep '^NVIDIA_API_KEY=' .env | cut -d= -f2)
    if [[ -z "$NVIDIA_API_KEY" ]]; then
        log_error "NVIDIA_API_KEY not found in .env"
        exit 1
    fi
    
    log_info "Starting TONY gateway on port $PORT..."
    log_info "Using NVIDIA_API_KEY: ${NVIDIA_API_KEY:0:12}..."
    
    # Start with explicit NVIDIA_API_KEY to override any inherited env
    NVIDIA_API_KEY="$NVIDIA_API_KEY" nohup node src/gateway/server.js >> "$LOG_FILE" 2>&1 &
    local pid=$!
    echo "$pid" > "$PID_FILE"
    
    log_info "Gateway started (PID: $pid)"
    log_info "Log: $LOG_FILE"
    log_info "PID file: $PID_FILE"
}

function wait_for_health() {
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

function show_dashboard_url() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🌐 JARVIS DASHBOARD: http://localhost:$PORT/jarvis${NC}"
    echo -e "${GREEN}     (Copy this URL and open in your browser)${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

function show_status() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE" 2>/dev/null || echo "")
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}TONY gateway is RUNNING${NC} (PID: $pid, Port: $PORT)"
            curl -s "http://localhost:$PORT/health" -H "Authorization: Bearer $API_TOKEN" 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"  Chain: {d['llmChain']['chain']}\")
    print(f\"  Model: {d['llm']}\")
    print(f\"  Online: {d['online']}\")
except: pass
" || echo "  (health check failed)"
            return 0
        fi
    fi
    
    # Check port anyway
    if lsof -tiTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
        echo -e "${YELLOW}TONY gateway RUNNING (orphaned)${NC} on port $PORT"
        return 0
    fi
    
    echo -e "${RED}TONY gateway is STOPPED${NC}"
    return 1
}

function stop_gateway() {
    log_info "Stopping TONY gateway..."
    kill_existing
    [[ -f "$PID_FILE" ]] && rm -f "$PID_FILE"
    log_info "Stopped."
}

function restart_gateway() {
    stop_gateway
    start_gateway
    wait_for_health
}

# Main
case "${1:-start}" in
    start)
        if show_status >/dev/null 2>&1; then
            log_warn "TONY gateway already running"
            show_status
            show_dashboard_url
        else
            kill_existing
            start_gateway
            wait_for_health && show_status && show_dashboard_url
        fi
        ;;
    stop)
        stop_gateway
        ;;
    restart)
        restart_gateway && show_status && show_dashboard_url
        ;;
    status)
        show_status
        if show_status >/dev/null 2>&1; then
            show_dashboard_url
        fi
        ;;
    logs)
        tail -f "$LOG_FILE"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac