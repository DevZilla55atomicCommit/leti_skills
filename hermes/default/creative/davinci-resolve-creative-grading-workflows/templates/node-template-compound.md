# Compound Node Template for DaVinci Resolve Creative Grading

A reusable compound node structure for common grading workflows that combines multiple adjustments into a single controllable unit. This template is designed for speed, consistency, and client delivery.

## 📋 Template Structure

```
Compound Node: CREATIVE_GRADE_{LOOK_NAME}
│
├─ INPUT: Base Footage
│
├─ NODE 1: PRIMARY CORRECTION (EXPOSURE/WB)
│   └─ Settings: [Insert values]
│
├─ NODE 2: COLOR THEORY ADJUSTMENT (SPLIT TONE/COMPLEMENTARY)
│   └─ Settings: [Insert values]
│
├─ NODE 3: FILM EMULATION (LUT/CINEON)
│   └─ Load: [LUT_PATH]
│
├─ NODE 4: SELECTIVE GRADING (POWER WINDOWS/SKIN)
│   └─ Settings: [Insert values]
│
├─ NODE 5: TEXTURE & GRAIN (FILM GRAIN/HALATION)
│   └─ Settings: [Insert values]
│
├─ OUTPUT: Graded Footage
│   └─ Optional: Export LUT (PowerGrade)
```

## ⚙️ Configuration Fields

| Field | Description | Example |
|-------|-------------|---------|
| **LOOK_NAME** | Unique identifier for the style | `TEAL_ORANGE_BALANCE`, `FILM_GRAIN_SOFT`, `WEDDING_FOREVER` |
| **EXPOSURE_NODE** | Primary exposure correction | `+0.15 EV` |
| **WB_NODE** | White balance target | `Temp: 5500K, Tint: +2` |
| **SPLIT_TONE_NODE** | Highlight/Shadow tint pair | `Highlights: Orange(30°), Shadows: Teal(210°)` |
| **LUT_PATH** | Path to LUT file | `/PowerGrades/TEAL_ORANGE.cube` |
| **POWER_WINDOW_SHAPE** | Brush/shape settings | `Radial: Size 0.6, Feather 0.3` |
| **GRAIN_LEVEL** | Film grain intensity | `Amount: 0.25, Size: 1.2` |
| **EXPORT_LUT** | Generate exportable PowerGrade? | `YES/NO` |

## 🛠️ Usage Instructions

1. **Duplicate** this template in the DaVinci Resolve Library > Compound Nodes folder
2. **Rename** to match your project's naming convention (e.g., `COMPOUND_NODE_WEDDING_LOOK`)
3. **Populate** each node's settings with project-specific values
4. **Save** as a PowerGrade for reuse across sessions
5. **Document** key values in the node's metadata for team consistency

## 💡 Pro Tips

- **Keyboard Shortcuts**: Use `Ctrl+Shift+C` to open the Compound Node builder
- **Parameter Linking**: Link nodes to sliders for dynamic adjustments
- **Version Control**: Tag versions with client/project name for auditability
- **Validation**: Run `verify-workflow.sh` script to check node count and required fields