---
name: architecture-diagram-enhanced
description: Interactive, pan‑zoomable architecture diagrams with folder‑only and full‑file views.
version: 1.0.0
author: Alfred (Hermes Agent)
license: MIT
date: 2026-07-12
tags: [architecture, diagrams, SVG, HTML, visualization, infrastructure, cloud]
related_skills: [architecture-diagram, concept-diagrams, excalidraw]
---

## Interactive Workflow & Usage
After generating an architecture diagram HTML, you can open it directly in any browser to view an interactive, pan‑zoomable diagram. The generated HTML includes built‑in controls for:

* **View Mode Switcher** – Toggle between “Folders Only” (compact tree view) and “Full (All Files)” to show detailed file listings.
* **Pan & Zoom** – Use mouse wheel to zoom, click‑drag to pan across large diagrams.
* **Color Legend** – Click the legend to highlight specific categories (e.g., Camera Theory, Workflows).
* **Export Buttons** – One‑click download of SVG or PNG exports for sharing.
* **Reset View** – Restore default zoom/position instantly.

### Generation Script (Updated)
The skill ships with a Python‑style script that:

1. Loads `knowledge_base_export.json` to count files/folders.
2. Builds a self‑contained HTML file with embedded CSS/JS for the diagram.
3. Injects dynamic Mermaid code based on the selected view.
4. Applies color‑coded categories matching the design system.
5. Adds a legend outside the diagram boundary.

### Updated Generation Script
```python
def generate_interactive_diagram(view='folders'):
    # 1. Load export data
    import json, os
    with open('knowledge_base_export.json') as f:
        data = json.load(f)

    # 2. Count items per folder
    folder_counts = {f: len(files) for f, files in data['folders'].items()}

    # 3. Build Mermaid code based on view
    mermaid_code = build_mermaid(view, folder_counts)

    # 4. Render HTML (includes full CSS/JS)
    html = render_template('templates/interactive-diagram.html',
                           mermaid_code=mermaid_code,
                           folder_data=data['folders'],
                           metadata=data['metadata'])
    out_path = f'{data["metadata"]["project_name"]}-architecture.html'
    write_file(out_path, html)
    return out_path
```

### How to Use
```bash
# Generate a folder‑only diagram
architecture-diagram-enhanced generate --view folders

# Generate a full‑file diagram
architecture-diagram-enhanced generate --view full

# Open the result
open ./my‑project‑architecture.html   # macOS
xdg-open ./my‑project‑architecture.html   # Linux
```

### Design System Recap
* **Color Mapping** – Blue (Root), Yellow (Grading & Looks), Purple (Correction), Green (Camera Theory), Red (Workflows), Grey (Skills).
* **Typography** – JetBrains Mono, 12 px titles, 9 px labels, 8 px annotations.
* **Background** – Slate‑950 (`#020617`) with a subtle 40 px grid.
* **Component Boxes** – Rounded rectangles with double‑masking for visible arrows.
* **Legend Placement** – Dynamically placed 20 px below the lowest boundary.

Embed these details directly into each diagram generation for consistency.