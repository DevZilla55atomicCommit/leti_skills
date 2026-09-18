#!/usr/bin/env bash
# macOS Storage Scan Script
# Quick audit of common space hogs on creative/developer Macs
# Usage: ./scan-storage.sh [--json] [--top N]

set -euo pipefail

JSON_OUTPUT=false
TOP_N=20

while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift ;;
        --top) TOP_N="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper: format bytes to human readable
hr() {
    local bytes=$1
    if [[ $bytes -gt 1099511627776 ]]; then
        echo "$(bc <<< "scale=1; $bytes/1099511627776") TB"
    elif [[ $bytes -gt 1073741824 ]]; then
        echo "$(bc <<< "scale=1; $bytes/1073741824") GB"
    elif [[ $bytes -gt 1048576 ]]; then
        echo "$(bc <<< "scale=1; $bytes/1048576") MB"
    elif [[ $bytes -gt 1024 ]]; then
        echo "$(bc <<< "scale=1; $bytes/1024") KB"
    else
        echo "${bytes} B"
    fi
}

# Helper: get size in bytes
get_size_bytes() {
    local path="$1"
    if [[ -e "$path" ]]; then
        du -s "$path" 2>/dev/null | awk '{print $1 * 1024}' || echo 0
    else
        echo 0
    fi
}

# Helper: get size human
get_size_hr() {
    hr $(get_size_bytes "$1")
}

# Collect results as JSON array
results=()

add_result() {
    local category="$1"
    local path="$2"
    local size_bytes="$3"
    local status="$4"  # ok, warning, critical
    local notes="$5"
    
    if [[ "$JSON_OUTPUT" == true ]]; then
        results+=("{\"category\":\"$category\",\"path\":\"$path\",\"size_bytes\":$size_bytes,\"size_hr\":\"$(hr $size_bytes)\",\"status\":\"$status\",\"notes\":\"$notes\"}")
    else
        local color=$NC
        case $status in
            critical) color=$RED ;;
            warning) color=$YELLOW ;;
            ok) color=$GREEN ;;
        esac
        printf "${color}%-30s %10s  %s${NC}\n" "[$category]" "$(hr $size_bytes)" "$path"
        [[ -n "$notes" ]] && echo "  └─ $notes"
    fi
}

echo -e "${BLUE}=== macOS Storage Scan ===${NC}"
echo "Timestamp: $(date)"
echo

# 1. System volumes
echo -e "${BLUE}--- System Volumes ---${NC}"
df -h / /System/Volumes/Data 2>/dev/null | tail -n +2 | while read line; do
    echo "  $line"
done
echo

# 2. AI/ML Models
echo -e "${BLUE}--- AI/ML Model Caches ---${NC}"

# Ollama
ollama_size=$(get_size_bytes "$HOME/.ollama/models")
ollama_models=0
if [[ -d "$HOME/.ollama/models/manifests/registry.ollama.ai/library" ]]; then
    ollama_models=$(find "$HOME/.ollama/models/manifests/registry.ollama.ai/library" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
fi
add_result "ollama" "$HOME/.ollama/models" "$ollama_size" \
    $([ $ollama_size -gt 10737418240 ] && echo critical || echo warning) \
    "$ollama_models models installed"

# LM Studio
lmstudio_size=$(get_size_bytes "$HOME/.lmstudio")
add_result "lmstudio" "$HOME/.lmstudio" "$lmstudio_size" \
    $([ $lmstudio_size -gt 5368709120 ] && echo critical || echo warning) \
    "Models + extensions"

# Hugging Face
hf_size=$(get_size_bytes "$HOME/.cache/huggingface")
add_result "huggingface" "$HOME/.cache/huggingface" "$hf_size" \
    $([ $hf_size -gt 5368709120 ] && echo critical || echo ok) \
    "HF Hub cache"

# PyTorch
torch_size=$(get_size_bytes "$HOME/.cache/torch")
add_result "pytorch" "$HOME/.cache/torch" "$torch_size" ok "Compiled kernels"

# uv
uv_size=$(get_size_bytes "$HOME/.cache/uv")
add_result "uv" "$HOME/.cache/uv" "$uv_size" \
    $([ $uv_size -gt 5368709120 ] && echo warning || echo ok) "uv package cache"

echo

# 3. Video/Creative
echo -e "${BLUE}--- Video/Creative Media ---${NC}"

# Desktop video folders
if [[ -d "$HOME/Desktop" ]]; then
    find "$HOME/Desktop" -maxdepth 2 -type f \( -iname "*.mov" -o -iname "*.mp4" -o -iname "*.mxf" -o -iname "*.r3d" -o -iname "*.braw" \) 2>/dev/null | while read f; do
        size=$(get_size_bytes "$f")
        if [[ $size -gt 1073741824 ]]; then
            add_result "desktop-video" "$f" "$size" critical "Large video on Desktop"
        elif [[ $size -gt 104857600 ]]; then
            add_result "desktop-video" "$f" "$size" warning "Video on Desktop"
        fi
    done
fi

# Movies folder
movies_size=$(get_size_bytes "$HOME/Movies")
add_result "movies" "$HOME/Movies" "$movies_size" ok "DaVinci/FCP projects, render cache"

# DaVinci installers on Desktop
find "$HOME/Desktop" -maxdepth 3 -type f \( -iname "DaVinci_Resolve_*.dmg" -o -iname "DaVinci_Resolve_*.zip" \) 2>/dev/null | while read f; do
    size=$(get_size_bytes "$f")
    add_result "davinci-installer" "$f" "$size" critical "Installer - already installed?"
done

echo

# 4. Developer Caches
echo -e "${BLUE}--- Developer Tool Caches ---${NC}"

# npm
npm_size=$(get_size_bytes "$HOME/.npm")
add_result "npm" "$HOME/.npm" "$npm_size" ok "npm cache"

# pnpm
pnpm_size=$(get_size_bytes "$HOME/.pnpm-store")
add_result "pnpm" "$HOME/.pnpm-store" "$pnpm_size" ok "pnpm global store"

# Docker
docker_raw="$HOME/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw"
docker_size=$(get_size_bytes "$docker_raw")
add_result "docker" "$docker_raw" "$docker_size" \
    $([ $docker_size -gt 53687091200 ] && echo critical || echo warning) "Docker VM disk (grows, never shrinks)"

# Go
go_size=$(get_size_bytes "$HOME/go/pkg/mod")
add_result "go" "$HOME/go/pkg/mod" "$go_size" ok "Go module cache"

# Cargo
cargo_size=$(get_size_bytes "$HOME/.cargo/registry/cache")
add_result "cargo" "$HOME/.cargo/registry/cache" "$cargo_size" ok "Rust crate cache"

echo

# 5. Browser Caches
echo -e "${BLUE}--- Browser & Electron Caches ---${NC}"

# Chrome OptGuide
chrome_ml="$HOME/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel"
chrome_ml_size=$(get_size_bytes "$chrome_ml")
add_result "chrome-ml" "$chrome_ml" "$chrome_ml_size" \
    $([ $chrome_ml_size -gt 1073741824 ] && echo warning || echo ok) "Chrome on-device ML models"

# Spotify
spotify_size=$(get_size_bytes "$HOME/Library/Caches/com.spotify.client")
add_result "spotify" "$HOME/Library/Caches/com.spotify.client" "$spotify_size" ok "Offline playback cache"

# VS Code
vscode_size=$(get_size_bytes "$HOME/Library/Application Support/Code")
add_result "vscode" "$HOME/Library/Application Support/Code" "$vscode_size" ok "Extensions, workspace storage"

# Codex
codex_size=$(get_size_bytes "$HOME/.codex")
add_result "codex" "$HOME/.codex" "$codex_size" ok "Codex runtimes"

echo

# 6. System Caches (user-writable only)
echo -e "${BLUE}--- User Caches (~/Library/Caches) ---${NC}"
du -sh "$HOME/Library/Caches"/* 2>/dev/null | sort -hr | head -$TOP_N | while read line; do
    size_str=$(echo "$line" | awk '{print $1}')
    path=$(echo "$line" | cut -f2-)
    # Convert to bytes for status
    size_bytes=$(get_size_bytes "$path")
    status="ok"
    if [[ $size_bytes -gt 1073741824 ]]; then status="warning"; fi
    if [[ $size_bytes -gt 5368709120 ]]; then status="critical"; fi
    add_result "cache" "$path" "$size_bytes" "$status" "User cache"
done

echo

# 7. Downloads
echo -e "${BLUE}--- Downloads Folder ---${NC}"
dl_size=$(get_size_bytes "$HOME/Downloads")
add_result "downloads" "$HOME/Downloads" "$dl_size" \
    $([ $dl_size -gt 5368709120 ] && echo warning || echo ok) "Review manually"

# Large files in Downloads
find "$HOME/Downloads" -type f -size +100M 2>/dev/null | head -10 | while read f; do
    size=$(get_size_bytes "$f")
    add_result "downloads-large" "$f" "$size" warning "Large file in Downloads"
done

echo

# 8. Trash
trash_size=$(get_size_bytes "$HOME/.Trash")
add_result "trash" "$HOME/.Trash" "$trash_size" ok "Empty to reclaim"

# 9. Time Machine local snapshots
echo -e "${BLUE}--- Time Machine Local Snapshots ---${NC}"
snapshots=$(tmutil listlocalsnapshots / 2>/dev/null | wc -l | tr -d ' ')
if [[ $snapshots -gt 0 ]]; then
    add_result "tm-snapshots" "/" 0 warning "$snapshots local snapshots (run: tmutil thinlocalsnapshots / 10000000000 4)"
else
    add_result "tm-snapshots" "/" 0 ok "No local snapshots"
fi

# Output JSON if requested
if [[ "$JSON_OUTPUT" == true ]]; then
    echo "["
    for i in "${!results[@]}"; do
        if [[ $i -eq $((${#results[@]} - 1)) ]]; then
            echo "  ${results[$i]}"
        else
            echo "  ${results[$i]},"
        fi
    done
    echo "]"
fi

echo -e "${BLUE}=== Scan Complete ===${NC}"