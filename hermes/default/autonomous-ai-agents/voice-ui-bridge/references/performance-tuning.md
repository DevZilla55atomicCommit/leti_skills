# Performance Tuning — JARVIS Voice UI

Optimization patterns for running 60fps WebGL with 3000-15000 particles.

## Target Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Frame rate | 60fps sustained | `frameRate()` in draw() |
| Frame time | < 16.67ms | Chrome DevTools Performance |
| Particle count | 3000-15000 | `particles.length` |
| Memory | < 100MB | Chrome Task Manager |
| GPU memory | < 500MB | `about:gpu` |
| WebSocket latency | < 50ms local | `performance.now()` roundtrip |

## Profiling Checklist

### 1. Chrome DevTools Performance Tab
```javascript
// Add to draw() for frame timing
if (frameCount % 60 === 0) {
  console.log('Frame time:', (1000 / frameRate()).toFixed(2), 'ms');
}
```

Record 10s profile → Look for:
- **Scripting** (JS execution) — should be < 5ms/frame
- **Rendering** (WebGL draw calls) — should be < 8ms/frame
- **Painting** — should be minimal (canvas only)
- **GPU** — check for shader compilation stalls

### 2. WebGL Inspector (Chrome Extension)
- Draw call count per frame
- Buffer uploads per frame
- Texture bindings
- Shader switches

## Particle System Optimization

### Current: 3000 particles at 60fps ✓

```javascript
// What we do RIGHT:
beginShape(POINTS);          // Single draw call
for (p of particles) vertex(p.x, p.y, p.z);
endShape();

// Depth sort once per frame
particles.sort((a, b) => b.pos.z - a.pos.z);
```

### If scaling to 15000:

```javascript
// Use instanced rendering (advanced)
const INSTANCE_COUNT = 15000;
const positions = new Float32Array(INSTANCE_COUNT * 3);
// Update positions array each frame
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.DYNAMIC_DRAW);
gl.drawArraysInstanced(gl.POINTS, 0, 1, INSTANCE_COUNT);
```

### If scaling to 50000+:

```javascript
// Pixel buffer (fastest for massive counts)
loadPixels();
for (let p of particles) {
  let idx = 4 * (Math.floor(p.y) * width + Math.floor(p.x));
  if (idx >= 0 && idx < pixels.length) {
    pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;
  }
}
updatePixels();
```

## Wireframe Sphere Optimization

### Current: 3 shells × 24 detail = ~3500 lines ✓

```javascript
// What we do:
for (shell = 0; shell < 3; shell++) {
  // Latitude + longitude lines
  // Noise displacement per vertex
}
```

### Optimizations if needed:

```javascript
// Precompute geometry in setup()
let sphereGeo = { latLines: [], lonLines: [] };

function setup() {
  for (let shell = 0; shell < 3; shell++) {
    // Compute all vertex positions once
    // Store in arrays for direct rendering
  }
}

function draw() {
  // Just push/pull transforms, render precomputed
  // Only noise displacement computed per-frame
}
```

## Noise Computation

### Current: 3D noise per particle per frame

```javascript
// 3000 particles × 3 noise calls = 9000 noise/frame
let nx = noise(x, y, z, time * scale);
```

### Optimization: Noise texture

```javascript
// Generate noise texture once
let noiseTex = createGraphics(256, 256, WEBGL);
noiseTex.noStroke();
for (let x = 0; x < 256; x++) {
  for (let y = 0; y < 256; y++) {
    let n = noise(x * 0.01, y * 0.01, z * 0.01);
    noiseTex.set(x, y, color(n * 255));
  }
}
noiseTex.updatePixels();

// In draw: sample texture instead of computing
let n = noiseTex.get(p.x * scale, p.y * scale);
```

## Camera & Transform Optimization

### Current: Camera orbit + push/pop per particle

```javascript
// For particle billboards:
push();
translate(p.x, p.y, p.z);
sphere(p.size);
pop();  // 3000 push/pop per frame!
```

### Optimization: Vertex shader billboards

```glsl
// In custom shader:
attribute vec3 position;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

void main() {
  vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
  // Billboard: zero out rotation
  mvPos.xy = position.xy;
  gl_Position = projectionMatrix * mvPos;
}
```

## Memory Management

### Avoid GC pressure in draw()

```javascript
// BAD: Creates new objects every frame
let color = color(r, g, b, a);
let v = createVector(x, y, z);

// GOOD: Reuse objects
_color.setRed(r); _color.setGreen(g); _color.setBlue(b); _color.setAlpha(a);
_vec.set(x, y, z);

// BETTER: Pre-allocate arrays
const colors = new Float32Array(particleCount * 4);
const positions = new Float32Array(particleCount * 3);
```

### Texture/buffer cleanup

```javascript
// When switching visual modes, clean up old buffers
function setVisualMode(mode) {
  if (currentMode === 'particles') {
    trailLayer.remove();  // Free offscreen buffer
    trailLayer = null;
  }
  // ... init new mode
}
```

## WebSocket Performance

### Current: ~20 msg/sec during SPEAKING

```javascript
// Throttle audio updates to 20fps
let lastAudioUpdate = 0;
function sendAudioUpdate() {
  if (millis() - lastAudioUpdate < 50) return;
  lastAudioUpdate = millis();
  ws.send(JSON.stringify({ type: 'audio_update', ... }));
}
```

### Binary protocol (if needed)

```javascript
// Instead of JSON, send binary
const buffer = new ArrayBuffer(4 + 64 * 4);  // amplitude + 64 floats
const view = new DataView(buffer);
view.setFloat32(0, amplitude);
for (let i = 0; i < 64; i++) {
  view.setFloat32(4 + i * 4, waveform[i]);
}
ws.send(buffer);
```

## CSS/Animation Performance

### Pulse rings: CSS animation (GPU-accelerated) ✓

```css
@keyframes pulse-ring {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.4; }
  100% { transform: translate(-50%, -50%) scale(2.5); opacity: 0; }
}
.pulse-ring {
  animation: pulse-ring 2s ease-out infinite;
  will-change: transform, opacity;  /* Hint to browser */
}
```

### Waveform bars: DOM updates (batched) ✓

```javascript
// Update all bars in single loop
for (let i = 0; i < bars.length; i++) {
  bars[i].style.height = `${h}px`;
  bars[i].style.opacity = opacity;
}
// Single reflow after loop
```

## Profiling Commands

```bash
# Run with profiling
cd ~/.hermes/hermes-agent
source venv/bin/activate
python -m cProfile -o profile.stats jarvis_tts_bridge.py

# Analyze
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

## Quick Wins Checklist

- [ ] `p5.disableFriendlyErrors = true` (10x speedup)
- [ ] `pixelDensity(1)` (4x less pixels on retina)
- [ ] `beginShape(POINTS)` for particles (1 draw call vs N)
- [ ] Depth sort particles back-to-front
- [ ] CSS animations for pulse rings (GPU)
- [ ] Throttle WebSocket to 20fps
- [ ] Reuse p5.Vector/color objects
- [ ] Precompute static geometry in setup()
- [ ] Use `Math.*` in hot loops
- [ ] Profile with Chrome DevTools before optimizing

## When to Worry

| Symptom | Likely Cause |
|---------|--------------|
| FPS drops to 30 | Too many particles, or noise in hot loop |
| FPS drops when tab inactive | Browser throttling — use `visibilitychange` to pause |
| Memory grows over time | Object allocation in draw(), uncleaned buffers |
| Jank every few seconds | GC pressure — reuse objects |
| WebGL context lost | Too many resources, or driver crash |

## Scaling Guide

| Particles | Approach | Expected FPS |
|-----------|----------|--------------|
| 3,000 | Current (beginShape POINTS) | 60 |
| 8,000 | Current + depth sort | 55-60 |
| 15,000 | Instanced rendering | 50-60 |
| 50,000 | Pixel buffer | 40-50 |
| 100,000 | Compute shader / pixel buffer | 30-40 |