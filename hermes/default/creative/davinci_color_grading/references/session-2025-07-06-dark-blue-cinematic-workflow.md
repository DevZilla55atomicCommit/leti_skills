# Dark Blue Cinematic Landscape Workflow — Session 2025-07-06

**Context:** User wanted to apply a dark blue cinematic look (reference: Icelandic moody grade) to a Pigeon Point Lighthouse photo, with selective masks to protect lighthouse, ocean rock, and keep grass golden but subtle.

## Key Learnings

### macOS Automation Limitation for Resolve Node Graph
**Problem:** The `macos-computer-use` skill (via `computer_use` tool / AppleScript) cannot reliably:
- Add serial nodes via `Option+S` shortcut
- Navigate node graph with arrow keys
- Open context menus on nodes
- Access menu bar items (`Node > Add Serial Node`)

**Root Cause:** DaVinci Resolve's node graph is a custom Canvas view that doesn't fully expose AX elements or respond to simulated keystrokes the same way native Cocoa controls do.

**Workarounds (in order of preference):**
1. **Manual step-by-step workflow** — Provided as click-by-click instructions with shortcuts
2. **PowerGrade `.drx` template** — Drag & drop onto any clip, instant full node tree
3. **MCP Integration** — Use `mcp_davinci_resolve_timeline_item_color` with `safe_apply_drx` or `propose_grade` (requires Resolve restart after config)

---

## Complete Dark Blue Cinematic Node Tree

### Phase 1: Primary Correction (Vault Linear + Gain Method)
```
NODE 01: BALANCE (Linear)
├── Gamma: Linear
├── Key Panel → Luma Mix: 0.0
├── Gain Pivot: 0.335 (locks 18% middle gray)
├── Vectorscope: Display Qualifier Focus ON + Skin Tone Line ON
├── Action: Hover WHITE (lighthouse) → Pull GAIN to center crosshair
└── Label: "BALANCE - Linear"

NODE 02: EXPOSURE
├── Gain/Lift/Gamma/Contrast (Waveform Y guided)
├── Target: Midtones ~35-40 IRE for dark mood
└── Label: "EXPOSURE"
```

### Phase 2: Global Dark Blue Grade (Node 07)
```
NODE 07: DARK BLUE GRADE
├── Log Wheels:
│   ├── Lift:     Hue 200° / Sat 45 / Lum -15  (deep teal shadows)
│   ├── Gamma:    Hue 195° / Sat 30 / Lum -8   (cyan midtones)
│   ├── Gain:     Hue 210° / Sat 15 / Lum -5   (blue-grey highlights)
│   └── Offset:   Hue 205° / Sat 10 / Lum -10  (global cold push)
├── Curves:
│   ├── Master: S-curve (0.3, 0.18) → (0.7, 0.82)
│   ├── Blue:   Lift shadows +0.08, pull highlights -0.05
│   ├── Red:    Pull shadows -0.02, highlights -0.03
│   ├── Hue vs Sat: Green -40, Yellow -25, Orange -15, Cyan +5, Blue +10
│   └── Hue vs Hue:  60°→42° (yellow→olive), 120°→155° (green→teal)
└── Label: "DARK BLUE LOOK"
```

### Phase 3: Layer Mixer for Selective Masks
```
LAYER MIXER: "SELECTIVE MASKS"
├── Input 1 (Green):  NODE 07 output (Global Grade) — BASE
├── Input 2 (Blue):   GRASS MASK → GRASS GOLDEN (Priority 1 - subtle)
├── Input 3 (Blue):   ROCK MASK → ROCK NATURAL (Priority 2)
└── Input 4 (Blue):   LIGHTHOUSE MASK → LIGHTHOUSE CLEAN (Priority 3 - HERO)

MASK SPECIFICATIONS:

GRASS MASK (Subtle Golden)
├── Qualifier: H 0.08-0.16, S 0.25-0.6, L 0.25-0.7
├── Window: Linear Gradient bottom 0%→40%, Feather 20
├── Correction: Log Gamma Hue 45° / Sat 28 / Lum +4
├── Hue vs Sat: 45° +18, 30° +12
└── Key Output Gain: 0.55  ← CRITICAL for subtlety

ROCK MASK (Natural Texture)
├── Qualifier: H 0.52-0.68, S 0.1-0.35, L 0.2-0.55
├── Window: Oval on rock, Feather 10
├── Correction: Log Lift Hue 30°/Sat 8/Lum +5, Gamma Hue 350°/Sat 5
└── Key Output Gain: 0.9

LIGHTHOUSE MASK (Hero - Bright White)
├── Qualifier: H 0.95-1.05, S 0-0.15, L 0.7-1.0
├── Window: Circle on tower + base, Feather 8
├── Correction: Linear + Gain WB only (Offset Hue 50°/Sat 5/Lum +3)
└── Key Output Gain: 0.85  ← Blends slight grade atmosphere
```

### Phase 4: Output & Polish
```
NODE 08: OUTPUT CST
├── Color Space Transform: DWG Intermediate → Rec.709 Gamma 2.4

NODE 09: FINISH
├── Vignette: Circle, Size 1.3, Softness 1.0, Gain -0.12
├── Film Grain: 35mm, Strength 0.12
├── Glow: Threshold 0.92, Radius 15, Intensity 0.04 (lighthouse only via qualifier)
└── Label: "FINISH"
```

---

## Scope Verification Checklist for Future Sessions
- [ ] Clean up existing node tree before building
- [ ] Set up 4-scope layout (Waveform Y, Parade RGB, Vectorscope, Histogram)
- [ ] Enable Video Level Scopes (64-940) for broadcast
- [ ] Enable Display Qualifier Focus on Vectorscope
- [ ] Apply Linear + Gain primary correction first
- [ ] Build global creative grade second
- [ ] Use Layer Mixer for selective protection
- [ ] Order Layer Mixer inputs: Base → Lowest priority → Highest priority
- [ ] Verify on all scopes before export
- [ ] Save PowerGrade templates for reuse

---

## Keyboard Shortcuts Reference (Mac)
| Action | Shortcut |
|--------|----------|
| Add Serial Node | `Option+S` |
| Add Layer Node | `Option+L` (on selected node) |
| Add Parallel Node | `Option+P` |
| Toggle Node | `Cmd+D` |
| Qualifier Highlight | `Shift+H` |
| Full-screen Scopes | `Cmd+Shift+W` |
| Label Node | `Tab` (customize in Keyboard Customization) |

---

## Integration with Vault Workflows
- **Primary Correction**: Uses `02-Primary-Color-Correction-Workflow-Linear-Printer-Lights.md` Linear + Gain method
- **Skin Tone Protection**: Adapted from `04-Skin-Tone-Correction-Using-Scopes-Vectorscope.md` Layer Mixer workflow
- **Color Management**: Follows `Apple-Log2_Russell-Wofford_CST-DWG-Workflow.md` DWG Intermediate grading space
- **Scopes**: Per `01-Scopes-Waveform-Vectorscope-Parade-Fundamentals-Darren-Mostyn.md` Video Legal (64-940)

---

## Related Session Files
- `references/session-2025-07-06-color-correction-fundamentals.md` — Complete Linear + Gain workflow from vault
- `references/mcp-vlm-grading-session-2025-07-06.md` — MCP integration attempts