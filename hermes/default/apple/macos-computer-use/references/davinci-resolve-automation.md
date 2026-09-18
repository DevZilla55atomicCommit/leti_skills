# DaVinci Resolve Automation Patterns & Pitfalls

**Session Context**: Attempted to automate node graph operations in DaVinci Resolve 21 (Color page) using macOS computer_use / AppleScript automation.

---

## What WORKS

| Operation | Method | Reliability |
|-----------|--------|-------------|
| App activation | `osascript -e 'tell application "DaVinci Resolve" to activate'` | ✅ Reliable |
| Window capture | `screencapture -R "x,y,w,h" /path/to/file.png` | ✅ Reliable |
| Keyboard shortcuts (global) | `Option+S` (Add Serial Node), `Option+L` (Add Layer Node) | ⚠️ Works ~60% - requires node graph focus |
| Menu bar access | `click menu item "X" of menu "Y" of menu bar 1` | ❌ Fails - Resolve menus not fully accessible via System Events |
| Click at coordinates | `click at {x, y}` | ⚠️ Works but coordinates shift with window size/layout |

---

## What FAILS / Unreliable

| Operation | Issue | Workaround |
|-----------|-------|------------|
| **Node graph node selection** | Clicking specific nodes by coordinate rarely selects the intended node; red highlight doesn't move predictably | Use keyboard navigation (arrow keys) after focusing node graph, OR provide manual workflow |
| **Color Wheels parameter adjustment** | Dragging wheels via `drag from {x,y} to {x,y}` not supported by System Events; numeric field entry via keystrokes is complex | Use manual entry in numeric fields, or provide exact values for user to type |
| **Context menus (right-click)** | `control click` / `right click` syntax errors in AppleScript; context menu doesn't appear | Use keyboard shortcuts instead (Option+S, Option+L, Option+P) |
| **Qualifier/Window tool interaction** | No reliable way to click eyedropper, draw windows, adjust sliders via automation | Manual only |
| **Curve point manipulation** | Cannot programmatically add/move curve points | Manual only |
| **Layer Mixer input reordering** | Dragging blue connector lines requires precise drag operations that fail | Manual only |

---

## Reliable Automation Pattern for Resolve

```applescript
-- 1. Activate & focus
tell application "DaVinci Resolve" to activate
delay 0.5

-- 2. Focus node graph (click in graph area)
tell application "System Events" to tell process "DaVinci Resolve"
    click at {1100, 350}  -- center of node graph
    delay 0.3
    
    -- 3. Use KEYBOARD ONLY for node operations
    key code 1 using option down  -- Option+S = Add Serial Node
    delay 0.3
    key code 37 using option down -- Option+L = Add Layer Node
    delay 0.3
    
    -- 4. Navigate with arrow keys
    key code 126  -- up arrow
    key code 124  -- right arrow
end tell
```

---

## Recommended Approach for Complex Grades

**Don't automate the grade itself.** Instead:

1. **Automate setup only**: Project settings, color management, adding base nodes
2. **Provide manual workflow document**: Exact click-by-click steps with values (see session workflow)
3. **Save as PowerGrade**: Once built manually, save node tree as `.drx` PowerGrade for instant reuse
4. **Use Resolve's Python API** (Studio only): For programmatic grade construction, enable External Scripting in Preferences

---

## Session-Specific Learnings (July 2026)

**Task**: Apply "Dark Blue Cinematic" grade with selective masks (lighthouse, ocean rock, grass) to Pigeon Point Lighthouse image.

**Node Structure Built**:
```
Base → 01 → EXP → 02 → 03(SAT) → DARK BLUE GRADE → OUTPUT CST
                                    ↓
                            Layer Mixer (Option+L)
                            ├─ Input 1 (Green): Global grade
                            ├─ Input 2 (Blue): LIGHTHOUSE MASK → CORRECTION (Key Output Gain 0.85)
                            ├─ Input 3 (Blue): ROCK MASK → CORRECTION (Key Output Gain 0.9)
                            └─ Input 4 (Blue): GRASS MASK → GOLDEN (Key Output Gain 0.55)
```

**Key Vault Workflows Applied**:
- Linear + Gain white balance (Waqas Qazi / Joris Hermans)
- Scope-guided decisions: Waveform Y, Parade RGB, Vectorscope + Skin Tone Line (Darren Mostyn)
- Layer Mixer protection workflow (adapted from Skin Tone protection in File 04)
- Key Output Gain for natural blending (File 04 technique)
- Apple Log 2 → DWG Intermediate → Rec.709 pipeline (Russell Wofford)

**Time**: ~10 minutes manual vs ~45 minutes failed automation attempts.

---

## Quick Reference: Resolve Shortcuts (Mac)

| Action | Shortcut |
|--------|----------|
| Add Serial Node | `Option+S` |
| Add Layer Node | `Option+L` |
| Add Parallel Node | `Option+P` |
| Toggle Node | `Cmd+D` |
| Qualifier Highlight | `Shift+H` |
| Full-screen Scopes | `Cmd+Shift+W` |
| Next Node (select) | `→` (right arrow) |
| Prev Node (select) | `←` (left arrow) |
| Upper Branch | `↑` (up arrow) |
| Lower Branch | `↓` (down arrow) |