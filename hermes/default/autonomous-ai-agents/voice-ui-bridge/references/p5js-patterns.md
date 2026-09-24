# p5.js WebGL Patterns — JARVIS Voice UI

Best practices and patterns extracted from building the JARVIS reactive voice UI.

## Instance Mode vs Global Mode

**Always use instance mode for production UIs** — global mode pollutes `window` and breaks when embedding multiple sketches.

```javascript
const sketch = (p) => {
  p.setup = () => {
    p.createCanvas(800, 600, p.WEBGL);
    p.pixelDensity(1);
    p.colorMode(p.RGB, 255, 255, 255, 255);
  };
  p.draw = () => {
    p.background(0);
    // render logic using p.* not global functions
  };
};

new p5(sketch, 'canvas-container-id');
```

In global mode (what we used for simplicity in the standalone HTML), just call `new p5()` at the end of DOMContentLoaded.

## Critical Setup (Global Mode)

```javascript
// BEFORE setup() - disable friendly errors for 10x performance
p5.disableFriendlyErrors = true;

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  pixelDensity(1);           // prevent 2x-4x overdraw on retina
  colorMode(RGB, 255, 255, 255, 255);
  
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
}
```

## Performance Patterns

### Use `Math.*` in hot paths (draw loop)
```javascript
// SLOW: p5 wrappers
let a = sin(t);
let d = dist(x1, y1, x2, y2);
let r = random();

// FAST: native Math
let a = Math.sin(t);
let d = Math.hypot(x1-x2, y1-y2);  // or compare magSq
let r = Math.random();
```

### Vectorize particle rendering
```javascript
// SLOW: individual shapes
for (let p of particles) {
  push(); translate(p.x, p.y, p.z); sphere(p.size); pop();
}

// FAST: single beginShape with POINTS
beginShape(POINTS);
for (let p of particles) vertex(p.x, p.y, p.z);
endShape();

// FASTEST: pixel buffer for massive counts
loadPixels();
for (let p of particles) {
  let idx = 4 * (Math.floor(p.y) * width + Math.floor(p.x));
  pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;
}
updatePixels();
```

### Offscreen buffers for layers (essential)
```javascript
let trailLayer, glowLayer;

function setup() {
  createCanvas(w, h, WEBGL);
  trailLayer = createGraphics(w, h);
  glowLayer = createGraphics(w, h);
}

function draw() {
  // Persistent trails
  trailLayer.fill(0, 0, 0, 0.07);
  trailLayer.noStroke();
  trailLayer.rect(0, 0, width, height);
  
  // Render to trail layer
  for (let p of particles) trailLayer.point(p.x, p.y, p.z);
  
  // Composite
  image(trailLayer, 0, 0);
}
```

## WEBGL Gotchas

| Issue | Fix |
|-------|-----|
| Origin at center | `translate(-width/2, -height/2)` for P2D-like coords |
| Y-axis inverted | Positive Y goes UP in WEBGL |
| Matrix stack overflow | `push()`/`pop()` around EVERY transform |
| Texture order | `texture()` BEFORE `rect()`/`plane()` |
| Blend modes | Use `blendMode(ADD)` for glow effects |

## Camera Orbit Pattern

```javascript
let camRadius = 600;
function draw() {
  let camX = camRadius * sin(frameCount * 0.0003);
  let camZ = camRadius * cos(frameCount * 0.0003);
  let camY = 100 * sin(frameCount * 0.0002);
  camera(camX, camY, camZ, 0, 0, 0, 0, 1, 0);
}
```

## Depth Sorting for Transparency

```javascript
particles.sort((a, b) => b.pos.z - a.pos.z);  // back-to-front
for (let p of particles) p.show();
```

## Noise Displacement on Geometry

```javascript
function drawWireframeSphere(radius, detail) {
  for (let i = 0; i <= detail; i++) {
    let lat = map(i, 0, detail, 0, PI);
    let r = radius * sin(lat);
    let y = radius * cos(lat);
    
    beginShape();
    for (let j = 0; j <= detail * 2; j++) {
      let lon = map(j, 0, detail * 2, 0, TAU);
      let x = r * cos(lon);
      let z = r * sin(lon);
      
      // Noise displacement
      let n = noise(x * 0.01, y * 0.01, z * 0.01, millis() * 0.001);
      let disp = (n - 0.5) * 8;
      vertex(x + disp * cos(lon), y, z + disp * sin(lon));
    }
    endShape();
  }
}
```

## Seeded Randomness (Always)

```javascript
function setup() {
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
}

// For new seed:
function newSeed() {
  CONFIG.seed = floor(random(999999));
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  // Re-initialize all noise-dependent state
}
```

## Color Mode — Use HSB for Generative

```javascript
colorMode(HSB, 360, 100, 100, 100);
// fill(hue, sat, bri, alpha)
// Rotate: fill((base + offset) % 360, 80, 90)
// Desaturate: fill(hue, sat * 0.3, bri)
// Darken: fill(hue, sat, bri * 0.5)
```

## Key Bindings Convention

```javascript
function keyPressed() {
  if (key === 's' || key === 'S') saveCanvas('output', 'png');
  if (key === 'g' || key === 'G') saveGif('output', 5);
  if (key === 'r' || key === 'R') { randomSeed(millis()); noiseSeed(millis()); }
  if (key === ' ') CONFIG.paused = !CONFIG.paused;
}
```

## Headless Export — Use noLoop()

```javascript
function setup() {
  createCanvas(1920, 1080, WEBGL);
  pixelDensity(1);
  noLoop();                    // capture script controls frame advance
  window._p5Ready = true;      // signal readiness to capture script
}

// In capture script (Node/Puppeteer):
// detect _p5Ready, then call redraw() once per frame
```

## Export Pipeline

```bash
# PNG
saveCanvas('name', 'png')

# GIF (5 seconds)
saveGif('name', 5)

# Frame sequence for MP4
saveFrames('frame', 'png', 10, 30)  # 10s at 30fps
# Then: ffmpeg -i frame-%04d.png -c:v libx264 output.mp4

# High-res via Puppeteer
node export-frames.js sketch.html --width 3840 --height 2160 --frames 300
```

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| `console.log()` in draw() | Remove or guard with `frameCount % 60 === 0` |
| DOM manipulation in draw() | Never |
| No `pixelDensity(1)` | Add it — prevents 4x overdraw on retina |
| Global mode with multiple sketches | Use instance mode |
| Raw `background(0)` | Always textured/gradient/layered |
| Single shell sphere | 3+ shells with varying alpha |
| No depth sorting | Sort particles by Z before render |
| `dist()` in hot loop | Use `magSq()` or `Math.hypot()` |
| Default color palette | Always custom 3-7 color palette |
| No seeded randomness | Always `randomSeed()` + `noiseSeed()` |