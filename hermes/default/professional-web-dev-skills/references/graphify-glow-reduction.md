# Graphify Glow Reduction & Visualization Tuning

## Background
When visualizing the Graphify 3D data structure, the default bloom and glow settings were too intense, making nodes and links difficult to discern. User feedback requested reduced glow for clarity.

## Adjustments Made

### 1. UnrealBloomPass (Scene.tsx)
- **Strength**: Reduced from `1.5` → `0.5` → **0.3** (final production: `0.3`)
- **Radius**: Reduced from `0.4` → `0.3` → **0.25** (final production: `0.25`)
- **Threshold**: Increased from `0.85` → `0.95` → **0.98** (final production: `0.98`)

### 2. OrbitalSphere Intensity
- **Intensity**: Reduced from `1.0` → `0.5` → **0.3** (final production)

### 3. LightningLinks Glow Intensity
- **Glow Intensity**: Reduced from `1.5` → `0.5` → **0.4**

### 4. Particle Field Adjustments
- **Particle Size**: Reduced from `1` → `0.5` → **0.4**
- **Particle Opacity**: Reduced from `0.4` → `0.15` → **0.1**

### 5. Camera Settings
- **Position**: Adjusted from `[0, 0, 5]` → `[0, 0, 2.5]`
- **FOV**: Adjusted from `60` → `50`
- **Near Plane**: Adjusted from `0.1` → `0.01`

## Why These Changes Improve Visibility
- Lower bloom strength prevents the scene from washing out
- Higher threshold ensures glow only appears on truly bright elements
- Reduced particle opacity decreases visual noise
- Closer camera position with wider FOV makes nodes more distinct
- Overall intensity reduction makes nodes/links more distinguishable

## Recommended Production Settings
```js
// Final production values
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  0.3,    // strength
  0.25,   // radius
  0.98    // threshold
);
```

## Common Pitfalls
- Over-reducing bloom can make the scene look flat; find a balance
- Very low particle opacity can make links invisible; adjust based on scene complexity
- Changes to bloom parameters may require corresponding UI state adjustments
- Camera position affects depth perception; test at multiple zoom levels