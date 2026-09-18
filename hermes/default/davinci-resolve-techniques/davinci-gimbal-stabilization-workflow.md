---
name: davinci-gimbal-stabilization-workflow
description: Gimbal shooting techniques and DaVinci Resolve stabilization workflow. Covers in-camera gimbal settings, post-production stabilization (Edit page, Color page, Fusion), and fixing gimbal artifacts.
trigger: gimbal, stabilization, steady shot, camera movement, DaVinci Resolve stabilize, warp stabilizer, smoothcam
steps:
  - "Configure gimbal: Balance, motor strength, follow modes (PF, PTF, FPV, L)"
  - "Shoot with proper technique: Walk heel-to-toe, elbows tucked, two hands"
  - "Import footage to DaVinci Resolve Media Pool"
  - "Edit Page: Inspector → Stabilization → Choose mode (Perspective/Similarity/Translation)"
  - "Color Page: Tracker → Stabilizer (more control, can isolate axes)"
  - "Fusion Page: Tracker + Stabilize tool (most control, per-pixel)"
  - "Fix artifacts: Rolling shutter (Gyro data), Micro-jitter (Smooth), Parallax (Crop)"
  - "Add motion blur if over-stabilized (Directional Blur / RSMB)"
parameters:
  - name: gimbal_mode
    type: string
    description: Gimbal follow mode used during shoot
    enum: ["PF (Pan Follow)", "PTF (Pan/Tilt Follow)", "FPV (Full Follow)", "L (Lock All)", "POV", "Vortex", "Go Mode"]
    default: "PF (Pan Follow)"
  - name: stabilization_method
    type: string
    description: DaVinci Resolve stabilization approach
    enum: ["Edit Page Inspector (Fast)", "Color Page Tracker (Balanced)", "Fusion Stabilize (Maximum Control)", "Gyro Metadata (Sony/Cannon/GoPro)"]
    default: "Edit Page Inspector (Fast)"
  - name: stabilization_mode
    type: string
    description: Stabilization algorithm
    enum: ["Perspective (Full 3D)", "Similarity (Scale+Rot+Trans)", "Translation Only (X/Y)", "Subspace Warp (Rolling Shutter)"]
    default: "Perspective (Full 3D)"
  - name: smoothness
    type: number
    description: Smoothing amount (0-100, higher = smoother but more crop)
    default: 50
    minimum: 0
    maximum: 100
  - name: crop_factor
    type: number
    description: Auto-crop to remove black edges (1.0 = no crop, 1.2 = 20% crop)
    default: 1.1
    minimum: 1.0
    maximum: 2.0
  - name: rolling_shutter_correction
    type: boolean
    description: Enable rolling shutter reduction (uses gyro data if available)
    default: false
tags:
  - gimbal
  - stabilization
  - davinci-resolve
  - steady-shot
  - warp-stabilizer
  - smoothcam
  - color-page-tracker
  - fusion-stabilize
  - rolling-shutter
  - micro-jitter
  - fpv
  - pan-follow
category: davinci-resolve-stabilization
---

# DaVinci Resolve Gimbal & Stabilization Workflow

Complete guide from gimbal setup through post-production stabilization in DaVinci Resolve (Edit, Color, and Fusion pages).

## Part 1: Gimbal Setup & Shooting Technique

### Balancing (Critical - Do Before Every Shoot)
```
1. Tilt Axis: Camera level, lens pointing forward
   - Loosen tilt → adjust camera fore/aft → lock when level

2. Roll Axis: Camera horizontal
   - Loosen roll → adjust left/right → lock when horizon level

3. Pan Axis: Base level
   - Loosen pan → adjust base → lock when level

4. Verify: Power on → all axes hold position → no drift
```

### Motor Strength & Tuning
```
Auto-Tune (Most Gimbals): Motor → Auto Tune → Follow prompts
Manual Tuning:
- Stiffness: Higher = more resistant to movement (heavy camera = higher)
- Hold Strength: How firmly position is held
- Follow Speed: How fast gimbal follows input

Preset Profiles (DJI RS/Ronin, Zhiyun, Moza):
- "Standard": Balanced
- "Sport/Fast": High stiffness, fast follow (running)
- "Cinematic/Slow": Low stiffness, slow follow (walking, dolly)
- "FPV": All axes follow (drone-like)
```

### Follow Modes Explained

| Mode | Pan | Tilt | Roll | Use Case |
|------|-----|------|------|----------|
| **PF (Pan Follow)** | ✅ Follow | 🔒 Lock | 🔒 Lock | Walking, tracking subject |
| **PTF (Pan/Tilt Follow)** | ✅ Follow | ✅ Follow | 🔒 Lock | General run-and-gun |
| **FPV / Full Follow** | ✅ Follow | ✅ Follow | ✅ Follow | Action, FPV drone feel |
| **L (Lock)** | 🔒 Lock | 🔒 Lock | 🔒 Lock | Fixed composition, timelapse |
| **POV** | ✅ Follow | ✅ Follow | ✅ Follow (tilted) | POV shots, tilted horizon |
| **Vortex** | 🔄 360° | 🔄 360° | 🔄 360° | Creative barrel rolls |
| **Go Mode** | ⚡ Fast | ⚡ Fast | ⚡ Fast | Running, sports |

### Shooting Technique (Body Mechanics)
```
Walking (Ninja Walk):
- Heel-to-toe rolling step
- Knees bent, absorb shock with legs
- Elbows tucked into ribs
- Two hands on gimbal (one on handle, one on grip)
- Move from hips, not arms

Speed Changes:
- Slow walk: PF mode, smooth
- Fast walk/run: Sport mode, wider stance
- Stop: Don't freeze - decelerate smoothly

Common Moves:
- Push In: Walk forward, gimbal at chest height
- Pull Out: Walk backward (spotter recommended)
- Slide/Truck: Side-step, gimbal level
- Rise/Fall: Bend knees, keep gimbal level
- Orbit: Circle subject, PF mode, constant distance
```

## Part 2: DaVinci Resolve Stabilization Methods

### Method 1: Edit Page Inspector (Fastest, Good Enough)
```
1. Select clip in timeline
2. Inspector (top right) → Video → Stabilization
3. Enable "Stabilize"
4. Settings:
   - Mode: Perspective / Similarity / Translation
   - Camera Lock: ON (tries to lock camera position)
   - Zoom: Auto (crops to remove black edges)
   - Smooth: 0.5-2.0 (higher = smoother)
5. Click "Analyze" → Wait for background analysis
6. Adjust Smooth/Zoom → Re-analyze if needed
```

**Pros:** Fast, non-destructive, stays in Edit page
**Cons:** Less control, can't isolate axes, no keyframing

---

### Method 2: Color Page Tracker (Balanced Control)
```
1. Color page → Select clip
2. Tracker panel (Window → Tracker) → Stabilizer tab
3. Settings:
   - Mode: Perspective / Similarity / Translation
   - Smooth: Translation / Rotation / Zoom (separate controls!)
   - Strong: Check for more aggressive
   - Zoom: Auto / Manual (crop factor)
4. Click "Stabilize" (analyzes frames)
5. Keyframe individual axes:
   - Translation X/Y: Smooth separately
   - Rotation: Smooth or lock
   - Zoom: Lock to prevent breathing
6. "Stabilize" button toggles effect on/off for comparison
```

**Advanced: Isolate Axes**
```
Want smooth pan but keep handheld shake in tilt?
- Translation X Smooth: 0.8
- Translation Y Smooth: 0.0 (off)
- Rotation Smooth: 0.5
- Zoom Smooth: 0.0
```

**Pros:** Per-axis control, keyframeable, in Color page (track moving subjects), real-time preview
**Cons:** Single clip at a time

---

### Method 3: Fusion Page Stabilize (Maximum Control)
```
Fusion Composition:
1. MediaIn (clip)
2. Tracker tool → Operation: "Stabilize"
   - Track: Select reference frame
   - Track forward/backward
   - Pattern: High contrast area
3. Stabilize tool (after Tracker)
   - Connect Tracker → Stabilize
   - Smooth: Translation / Rotation / Scale (separate)
   - Method: Subspace Warp (rolling shutter) / Rigid / Affine
   - Border: Replicate / Reflect / Color (black)
4. MediaOut

Advanced Fusion Stabilize Graph:
MediaIn → Tracker (multiple points) → Stabilize (Subspace Warp) → 
  → Crop (remove edges) → DirectionalBlur (add motion blur) → MediaOut
```

**Pros:** Per-pixel (Subspace Warp), multiple trackers, expressions, batch via scripts
**Cons:** Steep learning curve, slower, separate comp per clip

---

### Method 4: Gyro Metadata (Camera-Specific - Best Quality)
```
Supported Cameras:
- Sony: FX3, FX6, FX9, A7S III, A7 IV, A1, ZV-E1 (Catalyst Browse/Prepare)
- Canon: R5 C, C70, C300 III (Gyro data in .mxf)
- GoPro: Hero 9/10/11/12 (Gyro in .mp4)
- DJI: Ronin 4D, Osmo (internal)
- RED: Komodo, V-Raptor (gyro in .r3d)
- iPhone: 13/14/15 Pro (Cinematic mode, Action mode)

Workflow (Sony Example):
1. Shoot with "SteadyShot: Active" or "Standard" + Gyro ON
2. Import to Sony Catalyst Browse (free)
3. Catalyst: Analyze → Stabilize → Export .xml or ProRes with stabilization baked
4. Import stabilized clip to Resolve
OR: Resolve 19+ reads gyro metadata directly (Beta)

Resolve 19+ Gyro Stabilization:
1. Clip → Right-click → "Analyze for Stabilization (Gyro)"
2. Inspector → Stabilization → "Use Gyro Data"
3. Adjust Smooth/Crop
```

## Part 3: Fixing Stabilization Artifacts

### Artifact 1: Rolling Shutter (Jello/Wobble)
```
Symptoms: Vertical lines lean, buildings warp, "jello" on fast pan
Causes: CMOS sensor readout + stabilization stretching frames

Solutions:
1. Fusion: Stabilize tool → Method: "Subspace Warp" (analyzes local motion)
2. Gyro Data: Use Method 4 above (best - uses actual sensor data)
3. RSMB Pro: ReelSmart Motion Blur with RS correction
4. Shoot: Faster shutter (1/120+), global shutter camera, or slower pans
```

### Artifact 2: Micro-Jitter (Over-Stabilization)
```
Symptoms: Uncanny "floating" look, breathing edges, loss of organic feel
Cause: Smoothness too high, trying to stabilize intentional movement

Solutions:
- Reduce Smooth: Translation 0.3-0.5, Rotation 0.2-0.3
- Enable "Camera Lock" only for locked-off shots
- Keyframe Smooth: High for static, low for intentional moves
- Add subtle Directional Blur (Fusion) to restore motion feel
```

### Artifact 3: Edge Breathing / Black Borders
```
Symptoms: Image zooms in/out, black edges appear
Cause: Stabilization moves frame, auto-zoom crops

Solutions:
- Manual Zoom: Set fixed crop (1.1-1.15x) instead of Auto
- Fusion: Stabilize → Crop tool (fixed) → Transform (reposition)
- Shoot wider: Frame for 1.2x crop in post
```

### Artifact 4: Parallax Distortion
```
Symptoms: Foreground moves differently than background, "warp" look
Cause: Perspective mode on non-planar scenes

Solutions:
- Mode: "Similarity" or "Translation" (no perspective warp)
- Fusion: Subspace Warp handles parallax better
- Shoot: Avoid strong foreground elements when stabilizing heavily
```

### Artifact 5: Subject Tracking Loss
```
Symptoms: Stabilizer locks to background, subject drifts
Cause: Tracker picks wrong reference

Solutions:
- Color Page: Place tracker on subject → Stabilize tracks subject
- Fusion: Multiple trackers → Stabilize → Weight toward subject tracker
- Manual: Keyframe stabilization OFF when subject moves differently
```

## Part 4: Creative Stabilization Techniques

### Technique: "Steady Cam" Look (Intentional Imperfection)
```
Goal: Smooth but organic, not robotic

Settings:
- Edit Page: Smooth = 0.3-0.5, Camera Lock = OFF
- Color Page: Translation Smooth = 0.4, Rotation Smooth = 0.3
- Add Fusion: Directional Blur (Angle: motion direction, Distance: 2-5px)
- Add Fusion: Film Grain (breaks up digital smoothness)
```

### Technique: Locked-Down with Drift (Timelapse/Hyperlapse)
```
For tripod/timelapse shots with slight wind drift:
- Color Page: Mode = "Translation Only"
- Smooth = 2.0-5.0 (very smooth)
- Zoom = Locked (no breathing)
- Result: Rock-solid frame
```

### Technique: FPV Drone Smoothing
```
For DJI FPV / Avata / manual drone footage:
- Gyro data preferred (Method 4)
- If no gyro: Fusion Subspace Warp
- Smooth: Translation 0.6, Rotation 0.4
- Add: RSMB for motion blur (drone shutter often fast)
- Crop: 1.15x (drone footage often wide)
```

### Technique: Vehicle Mount (Car Hood, Suction Cup)
```
Challenges: Engine vibration (high freq), body roll (low freq)
Solution: Two-pass stabilization
Pass 1 (High freq): Fusion → Stabilize → Smooth Translation 0.8, Rotation 0.6
Pass 2 (Low freq): Color Page → Tracker → Smooth Translation 0.3
Or: Export Pass 1 → Re-import → Pass 2
```

## Part 5: Batch Stabilization Workflow

### For Multiple Clips (Edit Page)
```
1. Select all clips in timeline
2. Inspector → Stabilization → Enable
3. Set default settings (Perspective, Smooth 0.5, Zoom Auto)
4. Right-click → "Analyze" (processes all in background)
5. Review each → Adjust individual as needed
```

### For Multiple Clips (Python Script)
```python
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
proj = resolve.GetProjectManager().GetCurrentProject()
tl = proj.GetCurrentTimeline()

for track_index in range(1, tl.GetTrackCount("video") + 1):
    items = tl.GetItemListInTrack("video", track_index)
    for item in items:
        clip = item.GetMediaPoolItem()
        # Enable stabilization via API
        # Note: Full stabilization API limited, use UI batch
```

## Quick Reference: Stabilization Settings by Scenario

| Scenario | Page | Mode | Smooth (T/R/Z) | Zoom | Notes |
|----------|------|------|----------------|------|-------|
| Handheld walking | Edit | Perspective | 0.5 / 0.5 / 0.3 | Auto | Quick fix |
| Gimbal (PF mode) | Color | Similarity | 0.3 / 0.2 / 0.0 | 1.05x | Light touch |
| Gimbal (FPV) | Fusion | Subspace Warp | 0.6 / 0.4 / 0.2 | 1.1x | Parallax handling |
| Tripod (wind) | Color | Translation | 3.0 / 0.0 / 0.0 | Locked | Rock solid |
| Vehicle mount | Fusion 2-pass | Subspace + Trans | 0.8/0.6 / 0.3/0.0 | 1.15x | High + low freq |
| Drone | Gyro/Color | Perspective | 0.5 / 0.3 / 0.2 | 1.1x | Gyro preferred |
| Run-and-gun | Edit | Perspective | 0.7 / 0.5 / 0.3 | Auto | Fast turnaround |
| Locked interview | Color | Translation | 2.0 / 0.0 / 0.0 | Locked | Subject still |

## Related Skills

- `davinci-fusion-stabilize-advanced` - Fusion Subspace Warp deep dive
- `davinci-gyro-stabilization` - Camera gyro metadata workflows
- `davinci-rolling-shutter-fix` - RS correction techniques
- `davinci-hyperlapse-stabilize` - Timelapse/hyperlapse specific