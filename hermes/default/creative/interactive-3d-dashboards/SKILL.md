---
name: interactive-3d-dashboards
category: creative
description: Build interactive 3D data visualization dashboards using Three.js with CSS2D overlays for sports analytics, financial data, or any domain requiring explorable 3D views.
tags: [threejs, data-visualization, dashboard, interactive, webgl, css2d, sports-analytics]
---

# Interactive 3D Dashboards with Three.js

## When to Use
- Presenting multi-dimensional data (probabilities, scenarios, comparisons) in an explorable 3D space
- Sports analytics dashboards with live match data
- Any domain where users benefit from rotating, zooming, and switching between 3D view modes
- Client-facing demos where visual impact matters

## Core Architecture

### Layer Stack (Critical for Click Handling)
```
z-index: 100  →  UI Overlay (buttons, panels, controls)     ← pointer-events: auto on .panel elements
z-index: 5    →  CSS2D Labels (floating text in 3D space)   ← pointer-events: none
z-index: 1    →  WebGL Canvas (Three.js scene)              ← pointer-events: none on canvas DOM element
```

**The key fix**: Set `renderer.domElement.style.pointerEvents = 'none'` on the canvas so clicks pass through to the UI overlay above it. The canvas container can have `pointer-events: none` or just let the canvas itself handle it.

### View Management Pattern
```javascript
const viewCreators = {
  overview: createOverviewView,
  scenarios: createScenariosView,
  factors: createFactorsView,
  // ...
};

function setView(view) {
  currentView = view;
  clearView();           // Dispose geometries, materials, remove from scene
  viewCreators[view]();  // Build new view
  updateUIButtons(view);
}
```

Always dispose geometries/materials in `clearView()` to prevent memory leaks when switching views frequently.

## Three.js + CSS2DRenderer Setup

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

// WebGL Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.domElement.style.pointerEvents = 'none';  // CRITICAL — allows UI clicks
container.appendChild(renderer.domElement);

// CSS2D Label Renderer (separate layer)
const labelRenderer = new CSS2DRenderer();
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0';
labelRenderer.domElement.style.pointerEvents = 'none';
labelRenderer.domElement.style.zIndex = '5';
document.body.appendChild(labelRenderer.domElement);

// Animation loop renders both
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}
```

## Probability Visualization Patterns

### 3D Probability Pillars (Overview View)
- BoxGeometry height = probability × scale factor
- MeshPhysicalMaterial with clearcoat for glossy look
- Top glow mesh (BoxGeometry, 2 units tall, MeshBasicMaterial)
- CSS2D labels at top showing percentage
- Ring geometries for "total advance" probabilities

### Scenario Tree (Scenarios View)
- Root sphere at top
- CatmullRomCurve3 tubes branching to scenario nodes
- Node size ∝ probability (3 + prob × 8)
- Ring around node showing prob × 3 (visual weight)
- Outcome boxes at bottom with final percentages

### Factor Comparison Bars (Factors View)
- Horizontal bars left (Team A) / right (Team B) from center line
- Bar width = percentage × maxWidth
- Impact badges (HIGH/MED/LOW) with color coding
- Labels on both sides and center

### Scoreline Bars (Scorelines View)
- Sorted by probability descending
- Horizontal bars with team flag emoji, score, percentage
- Color-coded left border per team

### Radar/Spider Chart (Radar View)
- ShapeGeometry from polar coordinates
- Two overlapping shapes (Team A green, Team B red) with transparency
- Concentric rings at 20% intervals
- Axis labels at 1.2× max radius

## Animation Techniques

### Particle System
```javascript
// 3000 particles with velocity vectors
// Colors mapped to outcomes (green=win, yellow=draw, red=loss)
// Boundary wrap at radius > 200
// Subtle rotation: particles.rotation.y += 0.0001
```

### Bar Growth Animation
```javascript
// In animate loop, lerp scale.y toward targetHeight
mesh.scale.y = THREE.MathUtils.lerp(mesh.scale.y, targetH / geo.parameters.height, 0.05);
mesh.position.y = (geo.parameters.height * mesh.scale.y) / 2;
```

### Node Pulse
```javascript
// Sphere nodes breathe
mesh.scale.setScalar(1 + Math.sin(time * 2 + mesh.position.x) * 0.05);
```

## Data Structure Template

```javascript
const DATA = {
  probabilities: { brazil90: 0.60, draw90: 0.15, norway90: 0.05, brazilET: 0.25, norwayET: 0.10 },
  scenarios: [
    { id: 'A', name: 'Brazil Controls & Wins', prob: 0.45, color: 0x00cc44, desc: '...' },
    // ...
  ],
  scorelines: [
    { score: '2-0', prob: 0.28, team: 'brazil' },
    // ...
  ],
  factors: [
    { name: 'Key Matchup', brazil: 85, norway: 40, impact: 'HIGH' },
    // ...
  ],
  radar: {
    brazil: { possession: 85, defense: 75, experience: 95 },
    norway: { possession: 15, defense: 60, experience: 40 }
  }
};
```

## Pitfalls & Fixes

| Problem | Solution |
|---------|----------|
| Buttons unclickable under canvas | `renderer.domElement.style.pointerEvents = 'none'` |
| Labels flicker on view switch | Remove old CSS2DObjects in `clearView()` before creating new |
| Memory leak on view switch | `geometry.dispose()`, `material.dispose()`, `scene.remove(obj)` for all objects |
| Mobile touch doesn't rotate | OrbitControls works but add `controls.enablePan = true` for two-finger pan |
| CSS2D labels not visible | Check `labelRenderer.domElement.style.zIndex = '5'` (above canvas, below UI) |
| Performance drops with many objects | Use InstancedMesh for repeated geometries (particles, bars) |
| Text labels cut off at edges | CSS2DObject positions need margin from screen edges |

## Sports Analytics Specifics

### Data Sources (Priority Order)
1. **ESPN Scoreboard API** — `/soccer/scoreboard/_/league/fifa.world` — reliable, structured, live
2. **Wikipedia** — `/wiki/2026_FIFA_World_Cup_qualification#Qualified_teams` — comprehensive historical
3. **FIFA.com** — Heavy bot protection, avoid for automated scraping
4. **BBC/Guardian** — Good for narratives, harder for structured data

### Match Data Extraction (ESPN)
```javascript
// From scoreboard page
document.querySelectorAll('.Scoreboard__Card').forEach(card => {
  const teams = card.querySelectorAll('.Scoreboard__TeamName');
  const scores = card.querySelectorAll('.Scoreboard__Score');
  const status = card.querySelector('.Scoreboard__Status');
  // teams[0].textContent, scores[0].textContent, etc.
});
```

### Template Files

See `templates/threejs-dashboard-starter.html` for a minimal boilerplate with:
- Three.js + CSS2DRenderer + OrbitControls imports
- Layer stack CSS
- View switching skeleton
- Particle system starter
- Animation loop with dual render

See `templates/fifa-worldcup-dashboard.html` for a complete sports analytics dashboard with:
- 5 view modes (Overview, Scenarios, Factors, Scorelines, Radar)
- Camera preset animations with easing
- FIFA World Cup specific data structures
- Probability pillars, scenario tree, factor bars, scoreline chart, radar chart
- Particle system with outcome-colored particles
- Side panel metrics and scoreline grid

## Camera Preset Animation Pattern

For smooth view transitions, define camera presets and animate with easing:

```javascript
const cameraPresets = {
  overview: { position: new THREE.Vector3(0, 35, 85), target: new THREE.Vector3(0, 20, 0) },
  scenarios: { position: new THREE.Vector3(0, 50, 100), target: new THREE.Vector3(0, 20, -20) },
  factors: { position: new THREE.Vector3(0, 30, 70), target: new THREE.Vector3(0, 0, 0) },
  scorelines: { position: new THREE.Vector3(0, 20, 70), target: new THREE.Vector3(0, 0, 0) },
  radar: { position: new THREE.Vector3(0, 60, 80), target: new THREE.Vector3(0, 0, 0) }
};

function animateCameraToPreset(view) {
  const preset = cameraPresets[view];
  if (!preset) return;
  
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = preset.position.clone();
  const endTarget = preset.target.clone();
  
  const duration = 800;
  const startTime = performance.now();
  
  function animateCamera(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
    
    camera.position.lerpVectors(startPos, endPos, eased);
    controls.target.lerpVectors(startTarget, endTarget, eased);
    
    if (progress < 1) requestAnimationFrame(animateCamera);
  }
  requestAnimationFrame(animateCamera);
}
```

Call this in `setView()` after creating the new view's objects.

## FIFA World Cup Data Extraction Pattern

For live tournament data from ESPN:

```javascript
// ESPN Scoreboard URL pattern
const url = 'https://www.espn.com/soccer/scoreboard/_/league/fifa.world';

// Extract match cards
document.querySelectorAll('.Scoreboard__Card').forEach(card => {
  const teams = card.querySelectorAll('.Scoreboard__TeamName');
  const scores = card.querySelectorAll('.Scoreboard__Score');
  const status = card.querySelector('.Scoreboard__Status');
  
  if (teams.length >= 2 && scores.length >= 2) {
    console.log(`${teams[0].textContent} ${scores[0].textContent} - ${scores[1].textContent} ${teams[1].textContent} | ${status?.textContent || 'Live'}`);
  }
});

// Date navigation: use the date combobox (ref='15' in snapshot)
// Previous/Next buttons change the date parameter
```

For Wikipedia qualification data:
```
https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification#Qualified_teams
```
Use `document.querySelector('#Qualified_teams').parentElement.parentElement.innerText` to get the full qualification table with all 48 teams.

## References
- `references/threejs-patterns.md` — Common Three.js patterns for dashboards
- `references/sports-data-sources.md` — API endpoints and scraping notes for major sports
- `references/css2d-label-patterns.md` — Label positioning, styling, and management

## Templates
- `templates/threejs-dashboard-starter.html` — Minimal boilerplate with layer stack, view switching, particles, and animation loop. Copy and extend for new dashboards.

---