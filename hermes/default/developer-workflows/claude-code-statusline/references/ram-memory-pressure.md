# RAM Memory Pressure Monitoring — macOS Implementation

## Problem
Status line needs to show real-time RAM usage pressure so developers can see memory pressure while working. Must be fast (runs every ~1s status line refresh).

## Solution
Use macOS `memory_pressure` command (preferred) with `vm_stat` fallback. Calculate USED % = 100 - free %.

## Implementation
```bash
get_ram_usage() {
    if command -v memory_pressure >/dev/null 2>&1; then
        # memory_pressure reports "System-wide memory free percentage: XX%"
        # We want USED percentage = 100 - free
        local free_pct=$(memory_pressure 2>/dev/null | \
            grep -oE 'System-wide memory free percentage: [0-9]+%' | \
            grep -oE '[0-9]+' || echo "50")
        echo $((100 - free_pct))
    else
        # Fallback: parse vm_stat
        local pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
        local pages_active=$(vm_stat | grep "Pages active" | awk '{print $3}' | tr -d '.')
        local pages_inactive=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | tr -d '.')
        local pages_speculative=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | tr -d '.')
        local pages_wired=$(vm_stat | grep "Pages wired down" | awk '{print $4}' | tr -d '.')
        local pages_compressed=$(vm_stat | grep "Pages occupied by compressor" | awk '{print $5}' | tr -d '.')
        
        local total_pages=$((pages_free + pages_active + pages_inactive + pages_speculative + pages_wired + pages_compressed))
        local used_pages=$((pages_active + pages_inactive + pages_speculative + pages_wired + pages_compressed))
        
        if [ "$total_pages" -gt 0 ]; then
            echo $((used_pages * 100 / total_pages))
        else
            echo "0"
        fi
    fi
}

get_ram_color() {
    local pct=$1
    if [ "$pct" -ge 90 ]; then
        echo "$RED"
    elif [ "$pct" -ge 75 ]; then
        echo "$YELLOW"
    elif [ "$pct" -ge 60 ]; then
        echo "$MAGENTA"
    else
        echo "$GREEN"
    fi
}
```

## Color Thresholds
| RAM Usage | Color | ANSI | Meaning |
|-----------|-------|------|---------|
| 0-59% | Green | `\033[32m` | Comfortable |
| 60-74% | Magenta | `\033[35m` | Moderate pressure |
| 75-89% | Yellow | `\033[33m` | High pressure |
| 90%+ | Red | `\033[31m` | Critical |

## Output Format
```
🧠 83%
```
Prepended to line 1 after operations counter.

## Performance Notes
- `memory_pressure` is fast (~5-10ms)
- Runs on every status line refresh (~1s)
- No caching needed (unlike git status)
- Fallback `vm_stat` parsing is slightly slower but reliable

## Testing
```bash
# Check memory_pressure output
memory_pressure

# Test function directly
get_ram_usage
get_ram_color 83
```