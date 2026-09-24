# Python Image Generation Guide — Come Follow Me Lesson Prep

## Environment Setup
Use the Hermes venv Python (has matplotlib, numpy pre-installed):
```bash
/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python script.py
```

## Core Libraries
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
```

## Standard Figure Settings
```python
fig, ax = plt.subplots(figsize=(16, 5))  # Timeline
fig, ax = plt.subplots(figsize=(14, 5))  # 3-card layout (daughters, etc.)
fig, ax = plt.subplots(figsize=(14, 8))  # Flowchart
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.axis('off')
```

## Reusable Components

### Colored Rounded Box (phases, cards)
```python
box = FancyBboxPatch(
    (x, y), width, height,
    boxstyle="round,pad=0.05,rounding_size=0.1",
    facecolor=color, edgecolor='white', linewidth=2
)
ax.add_patch(box)
```

### Number Circle
```python
circle = plt.Circle((x + width/2, y + height + 0.05), 0.25, 
                    color=color, ec='white', lw=2, zorder=10)
ax.add_patch(circle)
ax.text(x + width/2, y + height + 0.05, str(num), 
        ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=11)
```

### Arrow Between Elements
```python
arrow = FancyArrowPatch(
    (x1, y1), (x2, y2),
    arrowstyle='->,head_width=8,head_length=6', color='#34495e', lw=2
)
ax.add_patch(arrow)
```

### Diamond Node (decision points)
```python
verts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
patch = mpatches.Polygon(verts, facecolor=color, edgecolor='white', lw=2)
ax.add_patch(patch)
```

## Color Palette (Lesson-Themed)
```python
colors = {
    'premortal': '#27ae60',      # green
    'council': '#8e44ad',        # purple
    'testing': '#e74c3c',        # red
    'health': '#c0392b',         # dark red
    'wrestling': '#f39c12',      # orange
    'restoration': '#27ae60',    # green
    'faith': '#2980b9',          # blue
    'whirlwind': '#34495e',      # dark gray
    'dove': '#3498db',           # light blue
    'oil': '#f39c12',            # gold
    'glory': '#e74c3c',          # red
}
```

## Save
```python
plt.tight_layout()
plt.savefig('/Users/alfredkamisese/filename.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
```

## Common Layouts

### Timeline (Horizontal, 6 phases)
- Width: 16, Height: 5
- Phase boxes: 2.3 wide, 1.5 tall, gap 0.3
- Start x: 0.5

### Three Cards (Daughters, etc.)
- Width: 14, Height: 5
- Card width: 3.5, gap: 4.3 between centers
- Emoji at top, name, Hebrew, temple stage, details

### Flowchart
- Width: 14, Height: 8-10
- Nodes positioned by (x, y) coordinates
- Draw nodes first, then arrows
- Legend in top-left