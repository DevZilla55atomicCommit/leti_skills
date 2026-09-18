# DaVinci Color Grading — Tutorial Summaries (DaVinci Resolve 19-21)

> Quick reference for all tutorials extracted during session 2025-07-05. Full markdown files in vault under `Color Grading & Looks/`.

---

## S-Log3 (Sony) Tutorials

### 1. Kyle White — "How to Grade S-Log3 in DaVinci Resolve | Sony FX3" (8:34, 239K views)
**Video ID:** `udVtG5jD2H0`  
**File:** `S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md`

**Node Tree (7 Nodes):**
```
1. EXP (Exposure) — Lift down shadows, Gain down highlights → balanced histogram
2. WB (White Balance) — Eyedropper on neutral (white shirt), auto temp/tint
3. PW (Power Window) — Circular on face → Curves lift midtones → Track → Outside Node → Curves darken BG
4. SKIN — Qualifier → Refine H/S/L → Matte Finesse (Denoise, Clean Black, Blur) → Midtone Detail ~10
5. CST (end) — Input: S-Gamut3/S-Log3 → Output: Rec.709/Gamma 2.4
6. LUT (Creative) — Key Output Gain 0% → raise to taste (30-60%)
```

**Key Settings:**
- CST: S-Gamut3 / S-Log3 → Rec.709 / Gamma 2.4
- Skin Midtone Detail: ~10 (softens, "polished music video feel")
- Power Window + Outside Node = subject pop
- Creative LUT via Key Output Gain (not opacity)

---

### 2. Danny Gan — "FASTEST Way To Color Grade Sony S-Log3 | CST" (11:20, 287K views)
**Video ID:** `hFZDiXbFeJQ`  
**File:** `S-Log3_Danny-Gan_3-Node-CST-Workflow.md`

**Node Tree (3 Nodes, Left → Right):**
```
PRIMARIES → LOOK → CST
```

**Settings:**
- CST: Input S-Gamut3.Cine / S-Log3 → Output Rec.709 / Gamma 2.4
- Tone Mapping: DaVinci | Gamut: None
- PRIMARIES: Tiny corrections only (Tint +2 to +5 for green cast)
- LOOK: Lift→greens, Gamma→orange, Gain→lift, all UPSTREAM of CST
- **Philosophy:** All corrections in S-Gamut3.Cine space → single CST to delivery

---

### 3. Cullen Kelly — "How to Grade SLog Footage" (14:04, 25K views)
**Video ID:** `YT3Mn3mk9Rg`  
**File:** `S-Log3_Cullen-Kelly_Pro-Noise-Highlight-Management.md`

**Key Techniques:**
- **ETTR (Expose to Right):** Sony sensors noisy in shadows → overexpose 1-2 stops → pull down in grade
- **Lum vs Sat Highlight Desat:** Rightmost control point down → smooth highlight roll-off (pink clouds → white)
- **Conservative Noise Reduction:** Spatial Better / Medium / Threshold 20 (not 100!) → "solution worse than problem"
- **Toe-Down Curves:** Compress shadows → less noise contrast + film print look
- **Template Node Tree:** Exposure → Balance → Contrast → Secondaries (Lum vs Sat, Hue vs Hue, Qualifier) → NR (only when needed) → Look
- **Timeline Voyager LUTs:** 3 components for global color harmony/Hue shifts/density

---

### 4. Mehran Hadad — "Cinematic Portrait Workflow in Resolve 21" (13:23, 4.8K views)
**Video ID:** `AR9K-GqY4Eg`  
**File:** `S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md`

**17-Node DWG Intermediate Pipeline:**
```
1. CST IN: S-Log3 → DWG Intermediate (Tone Mapping: OFF)
2. EXPOSURE: HDR wheels (Dark/Shadow ↑, Highlight ↓ + Range ↑)
3. CONTRAST: Soft S-curve + Primary wheels (Lift↓, Gamma↑, Gain↑, Highlights↓)
4. WHITE BALANCE: HDR + Sat 100% trick → Warm + Magenta
5. SATURATION: HSV space (disable Ch 1&3) → Gain wheel = soft saturation
6. COLOR SLICE: Yellow→warm/env, Skin→Hair (warm/orange, density↓)
7. SKIN TONE: Power Window on face → Outside Node → Hue vs Hue (reduce red)
8. RETOUCH HEAL: Retouch Me Heal (Studio) — sensitivity adjustable
9. RETOUCH DODGE&BURN: Retouch Me D&B — evens shadows, preserves texture
10. LOOK: RGB bars (Gain: Blue↓ Green↓ Red↓; Gamma: Red↓; Lift: Green↓ Blue↓; Log: Red↓ Blue↓)
11. SHARPEN: Blur/Sharpen, Radius↓, AB Mask, Scaling↓ (eyes only)
12. HALATION: Resolve Halation → Sat/Threshold/Spread tuned, Global Blend↓
13. GLOW: Resolve Glow → Sat control → Shine/Threshold/Spread/Gain balanced
14. VIGNETTE: Large PW + Feather + Invert → Curves down edges
15. FINAL ADJUST: Color Boost↓ (natural vibrance), Log Shadows↓
16. FILM GRAIN: 35mm 400T preset → Size/Texture/Strength
17. CST OUT: DWG Intermediate → Rec.709/Gamma 2.4
```

**Key:** HSV + HSL tandem (Saturation + Density), Parallel Mixer for skin, HDR ¼-stop adjustments.

---

## Apple Log 2 (iPhone) Tutorials

### 5. Russell Wofford — "How to color grade iPhone Apple Log 2 the RIGHT way" (3:53, 63K views)
**Video ID:** `JMIfDOfo_nE`  
**File:** `Apple-Log2_Russell-Wofford_CST-DWG-Workflow.md`

**Group Pre/Post-Clip Pipeline:**
```
Pre-Clip CST: Apple Log 2 / Apple Log → DaVinci Wide Gamut / DaVinci Intermediate
Post-Clip CST: DWG Intermediate → Rec.709 A
```
**Benefit:** Batch conversion for multi-clip timelines, grade in massive DWG space.

---

### 6. CineMirage — "How to Color Grade - Apple LOG 2 in DaVinci Resolve" (9:39, 1.7K views)
**Video ID:** `a1ZVeTKDNLY`  
**File:** `Apple-Log2_CineMirage_LUT-And-Manual-Grade.md`

**Method 1: One-Click LUTs** (6 LUTs: 1 free Basic + 5 paid) — CST baked in
**Method 2: Manual 2-Node:**
```
Node 1: CST Apple Log 2 / Apple Log → Rec.709 / Rec.709
Node 2: Primaries (Sat~70, Gain↑, Lift↓, Gamma↑, Temp adjust)
```
**Natural look philosophy:** "What feels right, not scientifically perfect"

---

### 7. FujiCinema — "Struggling with Apple Log? Watch This!" (4:10, 51K views)
**Video ID:** `IzV3t7RxPi4`  
**File:** `Apple-Log2_FujiCinema_Basics-Kodak-Film-Look.md`

**Path A: Commercial (3 Nodes)**
```
CST: Rec.2020/Apple Log → Rec.709/Gamma 2.4
EXPOSURE: HDR (Rec.2020/Apple Log) → Offset/Gain center scopes
CONTRAST: 1.3 + Sat ↑
```

**Path B: Film Look (4 Nodes)**
```
CST: Rec.2020/Apple Log → ST2084 (PQ)
EXPOSURE: HDR
KODAK 2383 LUT (Built-in)
FINAL: Contrast ~1.2, Sat to taste
```
**Auto-WB assumed** from Apple Camera App.

---

## Kodak 2383 Film Emulation

### 8. Darren Mostyn — "Why Do My Film LUTs Look Bad? - KODAK 2383" (5:16, 199K views)
**Video ID:** `A2OLQNSIJgU`  
**File:** `Kodak-2383_Darren-Mostyn_Correct-Application.md`

**Correct Pipeline:**
```
Grade in Rec.709 → CST (Rec.709/2.4 → Cineon Film Log) → Kodak 2383 D65 LUT → Compound Node → Key Output Gain
```
**Key:** Built-in Film Looks expect Cineon Log. Direct LUT on Rec.709 = crushed/oversaturated. Compound Node = clean Key Output Gain blending.

---

### 9. Gabe Lomotey — "Kodak 2383 Film Look - DaVinci Resolve Tutorial" (13:53, 21K views)
**Video ID:** `Ug-ygRJqSzM`  
**File:** `Kodak-2383_Gabe-Lomotey_DWG-DCTL-Dehancer-Workflow.md`

**Free Path:**
```
DWG Intermediate Grade → Disable → CST DWG→Cineon → Kodak 2383 D55 → Fine-tune → Film Grain → Compound
```

**Paid Path (Dehancer OFX):**
```
Source: DWG Intermediate → Stock: Kodak Gold 200 → Print: Kodak 2383
→ Tonal Contrast → Color Density → Grain → Bloom → Gate (Horizontal)
```

**Free DCTLs:** Middle Gray (pivot 0.336), Desatch, Tetra, 3D Filmic Contrast

---

## Skin Tones

### 10. Darren Mostyn — "The Qualifier in DaVinci Resolve" (8:36)
**Video ID:** `azM7dQSR8To`  
**File:** `Skin-Tones_Qualifier-Vectorscope-Workflow.md`

**Workflow:**
```
1. Primary grade first (Nodes 1-3) → get skin ON vectorscope line
2. CST/LUT → Rec.709
3. Qualifier (Node 4+): Shift+H → Manual HSL (Sat Low removes hair) → Matte Finesse (Clean Black > Clean White > Blur 1-3)
4. Vectorscope + Skin Line ON → Gamma nudge to line → Sat pop
```
**Key:** Key in Rec.709 (not Log), Sat Low = hair removal, Clean Black > Clean White, Gamma = natural skin shifter.

---

### 11. Tutorial Channel — "Perfect Skin Tones EVERY TIME in DaVinci Resolve 17" (8:11, 364K views)
**Video ID:** `Bw14wqVbpOo`  
**File:** `Skin-Tones_Layer-Node-Teal-Orange-Protection.md`

**Layer Node Workflow:**
```
Node 3: Skin Tones (Qualifier + Vectorscope + Log Wheels + Hue vs Hue)
Node 5: Teal/Orange Grade
Option/Alt+L on Node 5 → Layer Mixer
Connect BLUE (Alpha) from Node 3 → BLUE input of Layer Mixer
If inverted: Key Panel → Invert Qualifier icon
Key Output Gain on Node 3 → Blend ~0.7-0.85
```
**Also covers:** Hue vs Hue (shift red→yellow), Power Window for vectorscope check, free version compatible.

---

## Color Correction Fundamentals (Sub-Agent Extraction)

### 12. Darren Mostyn — "How to use resolve SCOPES" 
**File:** `Color Correction Fundamentals/01-Scopes-Waveform-Vectorscope-Parade-Fundamentals-Darren-Mostyn.md`
- 5 scopes: Waveform, Parade, Vectorscope, Histogram, CIE
- GPU setup, Display Qualifier Focus, Video Level Scopes (64-940 vs 0-1023)

### 13. Waqas Qazi — "Primary Color Correction Workflow"
**File:** `Color Correction Fundamentals/02-Primary-Color-Correction-Workflow-Linear-Printer-Lights.md`
- Why Lift/Gamma/Gain fails, Printer Lights/Offset method
- Linear Color Space + Gain as Global Offset (pro workflow)

### 14. Joris Hermans — "Cinematic Look via Correction"
**File:** `Color Correction Fundamentals/03-Cinematic-Look-Through-Proper-Color-Correction-Linear-Gain.md`
- Correction ≠ Grading, Linear Node + Gain Only (3 clicks)

### 15. Waqas Qazi — "Skin Tone Correction Using Scopes"
**File:** `Color Correction Fundamentals/04-Skin-Tone-Correction-Using-Scopes-Vectorscope.md`
- Layer Node workflow: Grade → Skin protection → Creative grade

---

## File Structure in Vault

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Color Grading & Looks/
├── S-Log3/
│   ├── S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md
│   ├── S-Log3_Danny-Gan_3-Node-CST-Workflow.md
│   ├── S-Log3_Cullen-Kelly_Pro-Noise-Highlight-Management.md
│   └── S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md
├── Apple Log 2/
│   ├── Apple-Log2_Russell-Wofford_CST-DWG-Workflow.md
│   ├── Apple-Log2_CineMirage_LUT-And-Manual-Grade.md
│   └── Apple-Log2_FujiCinema_Basics-Kodak-Film-Look.md
├── Kodak 2383/
│   ├── Kodak-2383_Darren-Mostyn_Correct-Application.md
│   └── Kodak-2383_Gabe-Lomotey_DWG-DCTL-Dehancer-Workflow.md
├── Skin Tones/
│   ├── Skin-Tones_Qualifier-Vectorscope-Workflow.md
│   └── Skin-Tones_Layer-Node-Teal-Orange-Protection.md
├── Color Correction Fundamentals/
│   ├── 01-Scopes-Waveform-Vectorscope-Parade-Fundamentals-Darren-Mostyn.md
│   ├── 02-Primary-Color-Correction-Workflow-Linear-Printer-Lights.md
│   ├── 03-Cinematic-Look-Through-Proper-Color-Correction-Linear-Gain.md
│   └── 04-Skin-Tone-Correction-Using-Scopes-Vectorscope.md
└── Film-Emulation_Mediabee_Dehancer-Pro-Voyager-DCTLs.md (pending)
```

---

## Memory.md Quick Links (Append to DaVinci_Knowledge_Base/Memory.md)

```markdown
### 🎞️ Kodak 2383 Film Emulation
*   **[Kodak 2383 Correct Application — Darren Mostyn]** :: `Color Grading & Looks/Kodak 2383/Kodak-2383_Darren-Mostyn_Correct-Application.md`
*   **[Kodak 2383 Comprehensive — Gabe Lomotey]** :: `Color Grading & Looks/Kodak 2383/Kodak-2383_Gabe-Lomotey_DWG-DCTL-Dehancer-Workflow.md`

### 🎯 Color Correction Fundamentals
*   **[Scopes Fundamentals — Darren Mostyn]** :: `Color Grading & Looks/Color Correction Fundamentals/01-Scopes-Waveform-Vectorscope-Parade-Fundamentals-Darren-Mostyn.md`
*   **[Primary Color Correction — Waqas Qazi]** :: `Color Grading & Looks/Color Correction Fundamentals/02-Primary-Color-Correction-Workflow-Linear-Printer-Lights.md`
*   **[Cinematic Look via Correction — Joris Hermans]** :: `Color Grading & Looks/Color Correction Fundamentals/03-Cinematic-Look-Through-Proper-Color-Correction-Linear-Gain.md`
*   **[Skin Tone Correction — Waqas Qazi]** :: `Color Grading & Looks/Color Correction Fundamentals/04-Skin-Tone-Correction-Using-Scopes-Vectorscope.md`

### 🍎 Apple Log 2 (iPhone) Tutorials
*   **[Apple Log 2 Dual-CST — Russell Wofford]** :: `Color Grading & Looks/Apple Log 2/Apple-Log2_Russell-Wofford_CST-DWG-Workflow.md`
*   **[Apple Log 2 LUT + Manual — CineMirage]** :: `Color Grading & Looks/Apple Log 2/Apple-Log2_CineMirage_LUT-And-Manual-Grade.md`
*   **[Apple Log Basics — FujiCinema]** :: `Color Grading & Looks/Apple Log 2/Apple-Log2_FujiCinema_Basics-Kodak-Film-Look.md`

### 🎬 S-Log3 (Sony) Tutorials
*   **[S-Log3 Cinematic Node Tree — Kyle White]** :: `Color Grading & Looks/S-Log3/S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md`
*   **[S-Log3 3-Node CST — Danny Gan]** :: `Color Grading & Looks/S-Log3/S-Log3_Danny-Gan_3-Node-CST-Workflow.md`
*   **[S-Log Nuances — Cullen Kelly]** :: `Color Grading & Looks/S-Log3/S-Log3_Cullen-Kelly_Pro-Noise-Highlight-Management.md`
*   **[Cinematic Portrait PowerGrade — Mehran Hadad]** :: `Color Grading & Looks/S-Log3/S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md`
```