#!/usr/bin/env bash
#
# api-retry-wrapper - Shell wrapper for automatic retry on API rate limits
#
# Usage:
#   api-retry-wrapper -- claude-code "your prompt"
#   api-retry-wrapper --base-delay 10 --max-retries 5 -- curl -X POST ...
#   api-retry-wrapper --stdin-prompt -- claude-code --stdin "prompt"
#
# Environment variables:
#   API_RETRY_MAX_RETRIES=5
#   API_RETRY_BASE_DELAY=10
#   API_RETRY_MAX_DELAY=160
#   API_RETRY_JITTER=0.2
#   API_RETRY_ON="429,500,502,503,504"
#   API_RETRY_CONTINUE_PROMPT="continue"
#   API_RETRY_MAX_CONTINUE=3
#   API_RETRY_LOG=~/.hermes/logs/api-retry.log

set -euo pipefail

# Default configuration
MAX_RETRIES="${API_RETRY_MAX_RETRIES:-5}"
BASE_DELAY="${API_RETRY_BASE_DELAY:-10}"
MAX_DELAY="${API_RETRY_MAX_DELAY:-160}"
JITTER="${API_RETRY_JITTER:-0.2}"
RETRY_CODES="${API_RETRY_ON:-429,500,502,503,504}"
CONTINUE_PROMPT="${API_RETRY_CONTINUE_PROMPT:-continue}"
MAX_CONTINUE="${API_RETRY_MAX_CONTINUE:-3}"
LOG_FILE="${API_RETRY_LOG:-$HOME/.hermes/logs/api-retry.log}"

# Parse retry codes into array
IFS=',' read -ra RETRY_CODE_ARRAY <<< "$RETRY_CODES"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_entry() {
    local level="$1"
    shift
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$timestamp | $level | $*" >> "$LOG_FILE"
}

# Extract HTTP status codes from text
extract_codes() {
    local text="$1"
    local codes=()
    
    # Match various patterns
    while IFS= read -r line; do
        # HTTP 429
        if [[ $line =~ HTTP[[:space:]]+([0-9]{3}) ]]; then
            codes+=("${BASH_REMATCH[1]}")
        fi
        # status: 429
        if [[ $line =~ [Ss]tatus[:[:space:]]+([0-9]{3}) ]]; then
            codes+=("${BASH_REMATCH[1]}")
        fi
        # "status":429
        if [[ $line =~ \"status\"[[:space:]]*:[[:space:]]*([0-9]{3}) ]]; then
            codes+=("${BASH_REMATCH[1]}")
        fi
        # 429 Too Many Requests
        if [[ $line =~ ([0-9]{3})[[:space:]]+(Too[[:space:]]Many|Rate[[:space:]]Limit|Internal|Bad[[:space:]]Gateway|Service[[:space:]]Unavailable|Gateway[[:space:]]Timeout) ]]; then
            codes+=("${BASH_REMATCH[1]}")
        fi
    done <<< "$text"
    
    printf '%s\n' "${codes[@]}" | sort -u
}

# Check if any code matches retry criteria
should_retry() {
    local codes=("$@")
    local code
    
    for code in "${codes[@]}"; do
        for retry_code in "${RETRY_CODE_ARRAY[@]}"; do
            if [[ "$code" == "$retry_code" ]]; then
                return 0
            fi
        done
    done
    return 1
}

# Calculate exponential backoff with jitter
calculate_delay() {
    local attempt="$1"
    local delay
    
    # Exponential backoff: base * 2^attempt
    delay=$(echo "$BASE_DELAY * (2 ^ $attempt)" | bc -l)
    
    # Cap at max delay
    if (( $(echo "$delay > $MAX_DELAY" | bc -l) )); then
        delay="$MAX_DELAY"
    fi
    
    # Add jitter
    local jitter_amount
    jitter_amount=$(echo "$delay * $JITTER" | bc -l)
    local jitter_value
    jitter_value=$(awk -v j="$jitter_amount" 'BEGIN { srand(); print (rand() * 2 - 1) * j }')
    delay=$(echo "$delay + $jitter_value" | bc -l)
    
    # Round to 1 decimal
    printf "%.1f" "$delay"
}

# Main retry logic
run_with_retry() {
    local cmd=("$@")
    local attempt=0
    local continue_count=0
    local last_stdout=""
    local last_stderr=""
    local exit_code=0
    
    log_entry "START" "cmd=$(printf '%q ' "${cmd[@]}")" "max_retries=$MAX_RETRIES" "base_delay=$BASE_DELAY"
    
    while (( attempt <= MAX_RETRIES )); do
        log_entry "ATTEMPT" "attempt=$((attempt + 1))" "total=$((MAX_RETRIES + 1))"
        
        # Prepare stdin if we need to send continue prompt
        local stdin_data=""
        if (( attempt > 0 && continue_count < MAX_CONTINUE )); then
            stdin_data="$CONTINUE_PROMPT"
            ((continue_count++))
            log_entry "CONTINUE_PROMPT_SENT" "prompt=$CONTINUE_PROMPT" "count=$continue_count"
        fi
        
        # Run command with timeout
        local stdout stderr
        local start_time
        start_time=$(date +%s)
        
        if [[ -n "$stdin_data" ]]; then
            # Run with stdin input
            {
                stdout=$(echo "$stdin_data" | timeout 300 "${cmd[@]}" 2>&1)
                exit_code=$?
            } || {
                exit_code=$?
                stdout=$(cat)
            }
        else
            stdout=$(timeout 300 "${cmd[@]}" 2>&1)
            exit_code=$?
        fi
        
        local end_time
        end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        last_stdout="$stdout"
        last_stderr=""
        
        # Extract HTTP codes from output
        local codes
        mapfile -t codes < <(extract_codes "$stdout")
        
        log_entry "OUTPUT" "attempt=$((attempt + 1))" "exit_code=$exit_code" "duration=${duration}s" "codes=${codes[*]}"
        
        # Check if we should retry
        if (( exit_code != 0 || ${#codes[@]} > 0 )); then
            if should_retry "${codes[@]}" && (( attempt < MAX_RETRIES )); then
                local delay
                delay=$(calculate_delay "$attempt")
                
                log_entry "RETRY" "attempt=$((attempt + 1))" "total=$((MAX_RETRIES + 1))" "delay=$delay" "codes=${codes[*]}"
                
                echo ""
                echo "[api-retry] Rate limit detected (codes: ${codes[*]}). Waiting ${delay}s before retry $((attempt + 2))/$((MAX_RETRIES + 1))..."
                echo ""
                
                sleep "$delay"
                ((attempt++))
                continue
            fi
        fi
        
        # Success or non-retryable error
        if (( exit_code == 0 )); then
            log_entry "SUCCESS" "attempt=$((attempt + 1))" "cmd=$(printf '%q ' "${cmd[@]}")"
        else
            log_entry "FAILURE" "attempt=$((attempt + 1))" "exit_code=$exit_code" "codes=${codes[*]}"
        fi
        
        echo "$stdout"
        return "$exit_code"
    done
    
    # Max retries exhausted
    log_entry "MAX_RETRIES_EXHAUSTED" "cmd=$(printf '%q ' "${cmd[@]}")"
    echo "$last_stdout"
    return 1
}

# Print usage
usage() {
    cat <<'EOF'
api-retry-wrapper - Automatic retry wrapper for API rate limits

USAGE:
    api-retry-wrapper [OPTIONS] -- COMMAND [ARGS...]

OPTIONS:
    -r, --max-retries N       Max retry attempts (default: 5, env: API_RETRY_MAX_RETRIES)
    -b, --base-delay SEC      Base delay in seconds (default: 10, env: API_RETRY_BASE_DELAY)
    -m, --max-delay SEC       Max delay cap in seconds (default: 160, env: API_RETRY_MAX_DELAY)
    -j, --jitter FACTOR       Jitter factor 0-1 (default: 0.2, env: API_RETRY_JITTER)
    -c, --retry-codes CODES   Comma-separated HTTP codes to retry (default: 429,500,502,503,504)
    -p, --continue-prompt STR Prompt to send via stdin after backoff (default: "continue")
    -n, --max-continues N     Max continue prompts to send (default: 3)
    -s, --stdin-prompt        Send continue prompt via stdin to subprocess
    -l, --log-file PATH       Log file path (default: ~/.hermes/logs/api-retry.log)
    -h, --help                Show this help

EXAMPLES:
    # Basic usage with claude-code
    api-retry-wrapper -- claude-code "write a function"
    
    # Custom retry config
    api-retry-wrapper --max-retries 10 --base-delay 30 -- claude-code "complex task"
    
    # Send continue via stdin (for tools that support it)
    api-retry-wrapper --stdin-prompt -- claude-code --stdin "your prompt"
    
    # With curl
    api-retry-wrapper -- curl -X POST https://api.example.com/endpoint
    
    # Environment variable configuration
    export API_RETRY_MAX_RETRIES=10
    export API_RETRY_BASE_DELAY=30
    api-retry-wrapper -- your-command

EOF
}

# Parse arguments
SEND_STDIN_PROMPT=false
ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--max-retries)
            MAX_RETRIES="$2"
            shift 2
            ;;
        -b|--base-delay)
            BASE_DELAY="$2"
            shift 2
            ;;
        -m|--max-delay)
            MAX_DELAY="$2"
            shift 2
            ;;
        -j|--jitter)
            JITTER="$2"
            shift 2
            ;;
        -c|--retry-codes)
            RETRY_CODES="$2"
            IFS=',' read -ra RETRY_CODE_ARRAY <<< "$RETRY_CODES"
            shift 2
            ;;
        -p|--continue-prompt)
            CONTINUE_PROMPT="$2"
            shift 2
            ;;
        -n|--max-continues)
            MAX_CONTINUE="$2"
            shift 2
            ;;
        -s|--stdin-prompt)
            SEND_STDIN_PROMPT=true
            shift
            ;;
        -l|--log-file)
            LOG_FILE="$2"
            mkdir -p "$(dirname "$LOG_FILE")"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            ARGS=("$@")
            break
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# If no -- separator, check if first arg is --
if [[ ${#ARGS[@]} -gt 0 && "${ARGS[0]}" == "--" ]]; then
    ARGS=("${ARGS[@]:1}")
fi

if [[ ${#ARGS[@]} -eq 0 ]]; then
    echo "Error: No command provided. Use -- to separate options from command." >&2
    usage
    exit 1
fi

# Run with retry
if [[ "$SEND_STDIN_PROMPT" == true ]]; then
    # We'll handle stdin in the function
    export API_RETRY_SEND_STDIN=1
fi

run_with_retry "${ARGS[@]}"