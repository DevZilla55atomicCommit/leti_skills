#!/usr/bin/env bash
#
# api-retry - Shell alias/function for easy retry wrapper usage
# Add to your ~/.bashrc, ~/.zshrc, or ~/.config/fish/config.fish
#
# Usage:
#   api-retry claude-code "your prompt"
#   api-retry --max-retries 10 --base-delay 30 -- claude-code "complex task"
#   api-retry --stdin -- claude-code --stdin "prompt"

# Configuration (can be overridden by env vars)
API_RETRY_MAX_RETRIES="${API_RETRY_MAX_RETRIES:-5}"
API_RETRY_BASE_DELAY="${API_RETRY_BASE_DELAY:-10}"
API_RETRY_MAX_DELAY="${API_RETRY_MAX_DELAY:-160}"
API_RETRY_JITTER="${API_RETRY_JITTER:-0.2}"
API_RETRY_ON="${API_RETRY_ON:-429,500,502,503,504}"
API_RETRY_CONTINUE_PROMPT="${API_RETRY_CONTINUE_PROMPT:-continue}"
API_RETRY_MAX_CONTINUE="${API_RETRY_MAX_CONTINUE:-3}"
API_RETRY_LOG="${API_RETRY_LOG:-$HOME/.hermes/logs/api-retry.log}"

# Path to the wrapper script
API_RETRY_WRAPPER="$HOME/.hermes/skills/software-development/api-retry-handler/scripts/api-retry-wrapper.sh"

api_retry() {
    local wrapper="$API_RETRY_WRAPPER"
    
    if [[ ! -f "$wrapper" ]]; then
        # Fallback to Python version
        wrapper="$HOME/.hermes/skills/software-development/api-retry-handler/scripts/retry_wrapper.py"
        if [[ ! -f "$wrapper" ]]; then
            echo "Error: api-retry-handler skill not installed" >&2
            return 1
        fi
        python3 "$wrapper" "$@"
        return $?
    fi
    
    "$wrapper" "$@"
}

# Quick aliases for common tools
alias api-retry-claude='api-retry --stdin-prompt -- claude-code --stdin'
alias api-retry-codex='api-retry -- codex'
alias api-retry-opencode='api-retry -- opencode'
alias api-retry-curl='api-retry -- curl'

# For fish shell users:
# function api_retry
#     set -l wrapper "$HOME/.hermes/skills/software-development/api-retry-handler/scripts/api-retry-wrapper.sh"
#     if not test -f "$wrapper"
#         set wrapper "$HOME/.hermes/skills/software-development/api-retry-handler/scripts/retry_wrapper.py"
#         if not test -f "$wrapper"
#             echo "Error: api-retry-handler skill not installed" >&2
#             return 1
#         end
#         python3 $wrapper $argv
#         return
#     end
#     $wrapper $argv
# end

# Export for subprocesses
export -f api_retry 2>/dev/null || true