# Interactive Architecture Diagram Generation

## Overview
This skill produces self‑contained HTML diagrams that are:

- **Interactive** – pan/zoom canvas with mouse‑wheel zoom and click‑drag pan.
- **Toggleable Views** – switch between “Folders Only” (compact tree) and “Full (All Files)” (shows every file).
- **Color‑coded** – nodes follow the design system:
  - **Blue** – Root / Vault
  - **Yellow** – Color Grading & Looks
  - **Purple** – Color Correction
  - **Green** – Camera Theory
  - **Red** – Workflows / Other
  - **Grey** – Skills
- **Automatic Legend** – placed 20 px below the lowest boundary to avoid clipping.
- **Export Buttons** – one‑click download of SVG or PNG.

## Generation Flow
1. **Load** `knowledge_base_export.json` to obtain file/folder data.
2. **Count** items per folder.
3. **Build** Mermaid diagram string based on selected view.
4. **Render** HTML with embedded CSS/JS (`templates/interactive-diagram.html`).
5. **Write** output as `{project_name}-architecture.html`.

## Usage
```bash
# Folder‑only view (compact tree)
architecture-diagram-enhanced generate --view folders

# Full‑file view (all files listed)
architecture-diagram-enhanced generate --view full
```

Open the resulting `.html` file in any browser to view the interactive diagram.

## Legend & View Controls
- **View Switcher** – Toggle between compact folder view and detailed file view.
- **Pan & Zoom** – Mouse wheel to zoom, click‑drag to pan.
- **Export** – Download SVG or PNG.
- **Reset** – Restore default zoom/position.

## Color Mapping Reference
| Category | Color | Usage |
|----------|-------|-------|
| Root / Vault | `#1f6feb` (Blue) | Represents the top‑level project container |
| Color Grading & Looks | `#d29922` (Yellow) | All grading & look‑related folders |
| Color Correction | `#a371f7` (Purple) | Correction‑focused folders |
| Camera Theory | `#3fb950` (Green) | Camera‑related content |
| Workflows / Other | `#f85149` (Red) | Workflow, masking, power‑window, etc. |
| Skills | `#8b949e` (Grey) | External skill references |