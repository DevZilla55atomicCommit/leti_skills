# Session: Color Correction Fundamentals from Vault (2025-07-06)

## Summary
User asked for step-by-step color correction help. Discovered comprehensive color correction workflows in the Obsidian vault at `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Color Grading & Looks/Color Correction Fundamentals/`.

## Key Files Referenced

### 1. Master Index (00-MASTER-INDEX.md)
Complete professional workflow combining 4 tutorials:
- **01**: Scopes Fundamentals (Darren Mostyn) - Waveform, Parade, Vectorscope, Histogram, CIE Graph, Video Level Scopes
- **02**: Primary Correction - Linear + Printer Lights (Waqas Qazi) - Lift/Gamma/Gain problems, Linear Color Space + Gain as Offset
- **03**: Cinematic Look via Linear + Gain (Joris Hermans) - 30-second correction workflow, Display Qualifier Focus
- **04**: Skin Tone Correction (Joris Hermans) - Qualifier, Vectorscope Skin Tone Line, Layer Nodes, Key Output Gain

### 2. Universal Linear + Gain Workflow (Primary Recommendation)

**Node 01: BALANCE (Linear)**
```
Right-click node → Gamma → Linear
Key Panel → Luma Mix = 0
Gain Pivot: 0.335 (18% middle gray lock)
Vectorscope: Display Qualifier Focus ON + Skin Tone Line ON
Action: Hover white object → Pull Gain to center trace on crosshair
Time: 5-15 seconds per shot
```

**Node 02: EXPOSURE (optional)**
```
Gain up/down with locked pivot = clean exposure
Waveform (Y) monitoring
```

**Node 03+: CREATIVE GRADE**
```
CST: Linear → DWG Log
Log Wheels / Curves / Color Warper / LUTs
```

**Node SKIN: Layer Node Protection**
```
Qualifier on skin → Vectorscope 2x zoom + Skin Tone Line
Hue vs Hue / Hue vs Sat
Key Output Gain blend (0.7-0.85)
```

**Node LAST: OUTPUT**
```
CST: Working → Display (Rec.709/P3/Rec.2020)
```

### 3. Scope Setup (Darren Mostyn)

**4-Scope Layout:**
- Waveform (Y only, Colorize OFF)
- Parade (RGB, Colorize ON)
- Vectorscope (Skin Tone Line ON, 2x Zoom for skin)
- Histogram (YRGB)

**Video Level Scopes (Broadcast):**
- Enable "Video Level Scopes" in scope menu
- Show Reference Levels: Low=64, High=940
- Grade keeping signal BETWEEN these lines

**Display Qualifier Focus:**
- Scope menu → "Display Qualifier Focus" ON
- Pull qualifier key → all 4 scopes show ONLY qualified region
- Essential for precise skin tone work

### 4. Skin Tone Line Rule (All Tutorials Agree)
- **Angle**: ~11° (Flesh Tone / Memory Color line)
- **Rule**: Skin trace ON or slightly CLOCKWISE of line
- Left of line = Green/Magenta shift (unhealthy)
- Right of line = Warm/healthy

### 5. Camera-Agnostic Linear Workflow

| Camera | Log Format | CST Input | CST Output (Linear) |
|--------|------------|-----------|---------------------|
| ARRI Alexa | LogC3/4 | Alexa LogC | Linear (Alexa Wide Gamut) |
| Sony | S-Log3 | Sony S-Log3 | Linear (S-Gamut3) |
| RED | Log3G10 | RED Log3G10 | Linear (RED Wide Gamut) |
| Blackmagic | BRAW Film | BM Film | Linear (BM Wide Gamut) |
| Canon | C-Log3 | Canon C-Log3 | Linear (Cinema Gamut) |
| Panasonic | V-Log | Panasonic V-Log | Linear (V-Gamut) |
| DJI | D-Log | DJI D-Log | Linear (D-Gamut) |
| iPhone | Apple Log 2 / HLG | Apple Log / HLG | Linear (P3 / Rec.2020) |

**Universal Method:**
```
Node 01: CST (Camera Log → Linear) + Luma Mix=0 + Gain Balance
```
All cameras behave identically in Linear space.

### 6. Shot Matching Workflow
1. Grade hero shot perfectly on Node 01 (Linear + Gain)
2. Copy Node 01 to all clips in scene
3. Minor Gain tweaks per clip (exposure only)
4. Perfect match in seconds

### 7. PowerGrade Templates to Create
- **"LINEAR BALANCE TEMPLATE"**: Node with Linear Gamma, Luma Mix=0, Pivot=0.335, labeled "BALANCE"
- **"LINEAR PRIMARY TEMPLATE"**: 3-node chain (Balance → Creative → Output)

### 8. Keyboard Shortcuts (Mac / Win)
| Action | Mac | Win |
|--------|-----|-----|
| Add Serial Node | Opt+S | Alt+S |
| Add Layer Node | Opt+L | Alt+L |
| Toggle Node | Cmd+D | Ctrl+D |
| Expand Scopes | Cmd+Shift+W | Ctrl+Shift+W |
| Qualifier Highlight | Shift+H | Shift+H |
| Printer Lights (Full) | Numpad 4,5,6,7,8,9 | Numpad 4,5,6,7,8,9 |
| Printer Lights (Half) | Shift+Numpad | Shift+Numpad |
| Printer Lights (Quarter) | Opt+Numpad | Alt+Numpad |

### 9. Common Mistakes Checklist
- [ ] **Luma Mix = 0** — Forgot? Lift/Gamma contaminate
- [ ] **Pivot = 0.335** — Forgot? Gain shifts middle gray
- [ ] **Creative grading in Linear** — Wrong! Convert to Log/DWG first
- [ ] **Gain for saturation** — No! Linear Gain = exposure only
- [ ] **Missing Output Transform** — Wrong display colors

### 10. Next Steps for User
1. Share the image to color correct
2. I'll guide through Linear + Gain workflow step-by-step
3. Set up scopes per above
4. Identify camera log format for proper CST input
5. Execute Node 01 balance in <30 seconds
6. Build out rest of node tree

---

*Source: Vault files 00-MASTER-INDEX.md, 01-Scopes..., 02-Primary..., 03-Cinematic..., 04-Skin-Tone..., plus Apple Log 2 workflows*