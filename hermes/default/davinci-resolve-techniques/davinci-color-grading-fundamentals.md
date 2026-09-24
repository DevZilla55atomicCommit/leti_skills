---
name: davinci-color-grading-fundamentals
description: Core color grading techniques in DaVinci Resolve Color page - offset balancing, teal/orange grades, selective masking, depth of field
category: davinci-resolve
tags: [color-grading, color-correction, teal-and-orange, offset, masking, color-wheels, curves, hsl]
trigger: Use when user asks about color grading, color correction, color wheels, curves, LUTs, or cinematic looks in DaVinci Resolve
---

# DaVinci Resolve Color Grading Fundamentals

Core color grading techniques extracted from Instagram Reels, covering primary corrections, creative looks, and selective grading workflows on the Color page.

## Techniques Included

### 1. Global Offset Color Balancing
**Video ID:** `C9m9A2SpR-_` | **Difficulty:** Beginner | **Page:** Color | **Node Graph:** Serial
- **Key Node:** Offset Node
- **Parameters:** Offset: 25.00, Lift: 25.00, Gamma: 25.00, Gain: 1.00
- **Steps:**
  1. Import the video clip into the timeline
  2. Navigate to the Color page
  3. Select the Offset tool in the color wheels panel
  4. Adjust the circular color wheel to balance the global color tint and exposure
  5. Monitor the Waveform scopes to ensure highlights are not clipping
- **Tags:** color grading, mobile, offset, video editing

### 2. Teal and Orange Cinematic Grade
**Video ID:** `Cve9BKQocVN` | **Difficulty:** Beginner | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Primary Wheels, Curves, Hue/Saturation/Luma
- **Parameters:** Saturation: +15, Contrast: Increased, Midtones: Warm/Orange, Shadows: Teal/Blue
- **Steps:**
  1. Add a primary node to adjust contrast and white balance
  2. Use the Color Wheels to push shadows toward teal/blue
  3. Use the Offset or Wheels to push midtones/highlights toward a warm orange/yellow
  4. Use the Hue/Saturation curve to de-saturate greens if they appear distracting
  5. Apply a slight vignette to draw focus to the central island formation
- **Tags:** color grading, cinematic, aerial, teal-and-orange

### 3. Selective Subject Polygon Masking
**Video ID:** `C-ZGotYNz4b` | **Difficulty:** Intermediate | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Qualifier/Window, Primary Grade
- **Parameters:** Window Type: Polygon, Tracking: Active, Offset: 25.00
- **Steps:**
  1. Go to the Color page
  2. Select the Polygon Window tool from the Window tab
  3. Draw a custom path around the desired subject
  4. Go to the Tracker tab and click play to track the mask to the subject movement
  5. Apply color adjustments using the Primary Wheels or Curves to affect the masked area
- **Tags:** masking, color-grading, polygon, isolation

### 4. Artificial Depth of Field / Focus Blur
**Video ID:** `Cv2MWyANfG7` | **Difficulty:** Intermediate | **Page:** Color | **Node Graph:** Serial
- **Key Nodes:** Gaussian Blur, Magic Mask
- **Parameters:** Blur Radius: 25.0, Strength: 1.0
- **Steps:**
  1. Import footage and go to the Color Page
  2. Use the Magic Mask to isolate the subject (the drone)
  3. Create a new node for the background
  4. Add a Gaussian Blur or Lens Blur effect to the background node
  5. Adjust the blur radius to create a cinematic shallow depth of field
- **Tags:** cinematic, drone, depth-of-field, tutorial

### 5. DaVinci Resolve Instagram Reel C1ulI1PR84j (Color Grading + Vlog Editing)
**Video ID:** `C1ulI1PR84j` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial|Parallel|Layer Mixer|Compound
- **Tags:** color grading, vlog editing

### 6. Cinematic Drone Shot with DaVinci Resolve
**Video ID:** `C3xXriXIbv8` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Color Correction Node, LUT Mapping Node
- **Parameters:** Color Correction: Saturation 100%, Contrast 50%; LUT Mapping: Input LUT "Cinematic Drone LUT", Output LUT "Final Output LUT"
- **Steps:**
  1. Import footage into DaVinci Resolve
  2. Apply color correction using the Color Correction Node with desired saturation and contrast values
- **Tags:** Drone Cinematography, Color Grading, DaVinci Resolve Techniques

---

## Usage Notes

- **Primary Corrections First:** Always start with a primary node for exposure, white balance, and contrast before creative grades
- **Node Structure:** Use serial nodes for sequential corrections; parallel nodes for independent looks; layer mixer for blending
- **Scopes Are Essential:** Waveform, Parade, and Vectorscope are your reference — trust them over your monitor
- **Magic Mask (Studio):** Available in Studio version only; use Power Windows + Qualifier in Free version
- **LUT Workflow:** Apply creative LUTs on a separate node after primary correction; adjust intensity with Key Output Gain

## Common Parameters Reference

| Parameter | Typical Range | Purpose |
|-----------|---------------|---------|
| Offset | ±100 | Global color balance shift |
| Lift/Gamma/Gain | 0-100 | Shadow/Midtone/Highlight control |
| Saturation | 0-200 | Color intensity |
| Contrast/Pivot | 0-100 / 0-1 | Tonal contrast control |
| Blur Radius | 5-50 | Depth of field simulation |
| Mask Softness | 0-100 | Edge feathering |

## Skill Trigger Examples

- "How do I do teal and orange grading in DaVinci Resolve?"
- "Color grade my drone footage to look cinematic"
- "Create a depth of field blur in the Color page"
- "Use offset wheel for global color balance"
- "Polygon window tracking for selective grading"