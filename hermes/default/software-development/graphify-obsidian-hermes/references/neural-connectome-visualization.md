# Neural Connectome Visualization Guide

## Overview
This document describes how to render Obsidian vault knowledge graphs as a professional neural connectome visualization, featuring:
- Central glowing soma with animated pulse
- Dendritic arbor with fractal branching and spine details
- Myelinated axon with Node-of-Ranvier highlights
- Synaptic terminal with neurotransmitter particle system
- Professional color coding by node type (extension-based)

## Implementation Steps

### 1. Data Preparation
```bash
# Export graph data from Graphify
graphify export obsidian --dir "/path/to/vault/Graphify-ProjectName"
```

### 2. Node Styling by Type
```json
{
  "md (notes)": "#c084fc",
  "py (python)": "#fbbf24",
  "ts/tsx": "#60a5fa",
  "js/jsx": "#4ade80",
  "canvas": "#22d3ee",
  "rs (rust)": "#f87171",
  "go": "#06b6d4",
  "cpp/c": "#f472b6"
}
```

### 3. Three.js Scene Setup
```javascript
const canvas = new Canvas();
canvas.setCamera({ position: [0, 0, 3], fov: 50 });
canvas.setAttributes({ antialias: false, alpha: true });

// Add neural glow effect
const glowPass = new GlowPass({ strength: 1.5, sampleDistance: 1.0 });

// Apply to NeuralNeuron component
<NeuralNeuron 
  radius={0.8} 
  glowColor="#00ffff" 
  pulseSpeed={1.0}
  synapticParticles={2000}
/>
```

### 4. Professional Styling
- **Soma**: White core with Fresnel-based scale pulse (1.0 → 1.1)
- **Dendrites**: Purple branches with 12 fractal subdivisions, yellow spine boutons
- **Axon**: Yellow myelinated shaft with 8 red Nodes of Ranvier
- **Synapses**: 5KB green neurotransmitter particles with drift/fade animation
- **Lighting**: HDRI sky with low intensity, subtle ambient fill
- **Post-Processing**: Additive blending for glow, bloom for highlight rolloff

### 5. Interactive Controls
```javascript
controls = {
  rotateSpeed: 0.3,
  zoomSpeed: 0.2,
  panSpeed: 0.4,
  minZoom: 0.1,
  maxZoom: 10
}
```

## Visual Example
![Neural Connectome Example]([MEDIA: neural-connectome-example.png])

## Cost Considerations
- Local rendering: Zero API cost
- API rendering (cloud): ~$0.03 per 1000 frames at 60fps
- Free tier suitable for up to 500 frames/month

## Maintenance
```bash
# Update visualization style
graphify update . --style neural-connectome