# Particle System Patterns for Voice Visualization

Four ready-to-use particle systems for p5.js WebGL, each mapping TTS amplitude/state to distinct visual behavior.

## Common Setup

```javascript
const CONFIG = {
  particleCount: 2000,
  // ... pattern-specific params
}

const PALETTE = {
  bg: 'transparent',
  idle: { h: 45, s: 60, b: 80 },
  speaking: { h: 30, s: 85, b: 95 },
  listening: { h: 195, s: 70, b: 85 },
  thinking: { h: 275, s: 65, b: 80 },
}

let particles = []
let currentState = 'idle'
let targetAmplitude = 0
let currentAmplitude = 0
let time = 0

function setup() {
  createCanvas(w, h, WEBGL)
  colorMode(HSB, 360, 100, 100, 100)
  pixelDensity(1)
  disableFriendlyErrors = true
  // Initialize particles per pattern
}
```

---

## 1. Sphere Globe — Pulsing Shell

Particles distributed on spherical surface, radius pulses with amplitude.

```javascript
// In setup()
for (let i = 0; i < CONFIG.particleCount; i++) {
  const phi = Math.acos(2 * Math.random() - 1)
  const theta = Math.random() * Math.PI * 2
  particles.push({
    phi, theta,
    baseR: CONFIG.sphereRadius,
    offset: Math.random() * 1000,
    size: 1.5 + Math.random() * 1.5,
    hueOffset: Math.random() * 30 - 15,
  })
}

// In draw()
const stateColor = PALETTE[currentState]
const pulse = 1 + currentAmplitude * 0.4 + Math.sin(time * 2.0) * 0.05

beginShape(POINTS)
for (const p of particles) {
  const n = noise(p.phi * 10, p.theta * 10, time * 0.003 + p.offset)
  const r = p.baseR * pulse * (0.95 + n * 0.15)

  const x = r * sin(p.phi) * cos(p.theta)
  const y = r * cos(p.phi)
  const z = r * sin(p.phi) * sin(p.theta)

  const dist = sqrt(x*x + y*y + z*z)
  const bright = map(dist, CONFIG.sphereRadius*0.8, CONFIG.sphereRadius*1.2, 90, 40)
  const alpha = map(dist, CONFIG.sphereRadius*0.8, CONFIG.sphereRadius*1.2, 100, 30)

  stroke((stateColor.h + p.hueOffset + n * 20) % 360, stateColor.s, bright, alpha)
  strokeWeight(p.size * (0.8 + currentAmplitude * 0.5))
  vertex(x, y, z)
}
endShape()

// Core glow
noStroke()
fill(stateColor.h, stateColor.s, 90, 15 + currentAmplitude * 30)
sphere(CONFIG.sphereRadius * 0.15 * pulse)
```

**Best for:** JARVIS-style voice assistant, always-visible ambient presence

---

## 2. Flow Field — Curl Noise Ripples

Particles flow in 3D curl noise field, radial ripple wave on speech.

```javascript
// Curl noise helper
function curlNoise3D(x, y, z, scale) {
  const eps = 0.01
  const nx = noise((x+eps)*scale, y*scale, z*scale) - noise((x-eps)*scale, y*scale, z*scale)
  const ny = noise(x*scale, (y+eps)*scale, z*scale) - noise(x*scale, (y-eps)*scale, z*scale)
  const nz = noise(x*scale, y*scale, (z+eps)*scale) - noise(x*scale, y*scale, (z-eps)*scale)
  return { x: nz - ny, y: nx - nz, z: ny - nx }
}

// In setup()
for (let i = 0; i < CONFIG.particleCount; i++) {
  particles.push({
    x: (random()-0.5) * CONFIG.fieldSize,
    y: (random()-0.5) * CONFIG.fieldSize,
    z: (random()-0.5) * CONFIG.fieldSize,
    vx: 0, vy: 0, vz: 0,
    baseSize: 1 + random() * 2,
    hueOffset: random() * 40 - 20,
  })
}

// In draw()
const flowMult = 1 + currentAmplitude * 3
ripplePhase += currentState === 'speaking' ? 0.15 * flowMult : 0

beginShape(POINTS)
for (const p of particles) {
  const cn = curlNoise3D(p.x*0.01, p.y*0.01, p.z*0.01, 0.005 + time*0.001)
  p.vx = lerp(p.vx, cn.x * 0.3 * flowMult, 0.05)
  p.vy = lerp(p.vy, cn.y * 0.3 * flowMult, 0.05)
  p.vz = lerp(p.vz, cn.z * 0.3 * flowMult, 0.05)

  // Ripple from center
  const dist = sqrt(p.x*p.x + p.y*p.y + p.z*p.z)
  if (dist > 0.001 && currentAmplitude > 0.3) {
    const ripple = sin(dist * 0.05 - ripplePhase) * currentAmplitude * 0.5
    const falloff = exp(-dist * 0.01)
    p.vx += (p.x/dist) * ripple * falloff
    p.vy += (p.y/dist) * ripple * falloff
    p.vz += (p.z/dist) * ripple * falloff
  }

  p.x += p.vx; p.y += p.vy; p.z += p.vz
  // Boundary wrap...

  const speed = sqrt(p.vx*p.vx + p.vy*p.vy + p.vz*p.vz)
  const bright = map(speed, 0, 0.6, 40, 95)
  stroke((stateColor.h + p.hueOffset + speed*20) % 360, stateColor.s, bright, 90)
  strokeWeight(p.baseSize * (0.5 + speed*5))
  vertex(p.x, p.y, p.z)
}
endShape()
```

**Best for:** Dynamic "energy field" feel, continuous motion even when idle

---

## 3. Helix Torus — Rotating Geometry

Double helix + torus knot, rotation speed tied to amplitude.

```javascript
// In setup()
// Helix particles
for (let i = 0; i < 800; i++) {
  const t = (i/800) * PI * 8
  const strand = i % 2
  helixParticles.push({ t, strand, phase: strand*PI, baseR: 120, offset: random(100), size: 1.5+random(1.5), hueOffset: random(20)-10 })
}
// Torus knot particles
for (let i = 0; i < 600; i++) {
  torusParticles.push({ t: (i/600)*PI*2, offset: random(100), size: 1+random(2), hueOffset: random(30)-15 })
}

// In draw()
const rotY = time * 0.3 * (0.5 + currentAmplitude)
push()
rotateY(rotY)
rotateX(sin(time*0.3) * 0.2 * currentAmplitude)

// Helix
beginShape(POINTS)
for (const p of helixParticles) {
  const r = p.baseR * pulse * (0.9 + noise(p.t, time*0.05+p.offset)*0.2)
  const y = map(p.t, 0, PI*8, -140, 140) * pulse
  const x = r * cos(p.t + p.phase + time*0.2)
  const z = r * sin(p.t + p.phase + time*0.2)
  const wave = sin(p.t*2 + time*3) * currentAmplitude * 15
  stroke((stateColor.h + p.hueOffset + wave*2) % 360, stateColor.s, 60+abs(wave)*2+currentAmplitude*30, 50+currentAmplitude*40)
  strokeWeight(p.size * (0.8+currentAmplitude*0.4))
  vertex(x+wave*0.3, y, z+wave*0.3)
}
endShape()

// Torus knot (3,2)
beginShape(POINTS)
for (const p of torusParticles) {
  const pt = p.t + time*0.5*(0.5+currentAmplitude)
  const R = 160 * pulse, r = 40 * pulse
  const x = (R + r*cos(2*pt)) * cos(3*pt)
  const y = (R + r*cos(2*pt)) * sin(3*pt)
  const z = r * sin(2*pt)
  const wave = noise(p.t*5, time*0.1+p.offset) * currentAmplitude * 20
  stroke((stateColor.h + p.hueOffset + pt*10) % 360, stateColor.s, 50+wave+currentAmplitude*35, 40+currentAmplitude*45)
  strokeWeight(p.size * (0.7+currentAmplitude*0.5))
  vertex(x, y, z)
}
endShape()
pop()
```

**Best for:** Structured, geometric "AI brain" aesthetic

---

## 4. Burst Explosion — Radial Shockwaves

Particles explode outward on speech, implode on silence, with shockwave rings.

```javascript
// In setup()
for (let i = 0; i < CONFIG.particleCount; i++) {
  const phi = acos(2*random()-1), theta = random()*PI*2
  const r = 5 + random(20)
  particles.push({
    x: r*sin(phi)*cos(theta), y: r*cos(phi), z: r*sin(phi)*sin(theta),
    vx: 0, vy: 0, vz: 0, baseSize: 1+random(2),
    hueOffset: random(40)-20, life: 1, targetR: 350*(0.3+random(0.7)), launched: false
  })
}
for (let i = 0; i < 3; i++) shockwaves.push({ radius: 0, alpha: 0, hue: 45, speed: 0 })

// In draw()
const isBursting = currentState === 'speaking' && currentAmplitude > 0.4

if (isBursting && burstPhase < 1) {
  burstPhase = min(1, burstPhase + 0.03)
  for (const p of particles) {
    if (!p.launched && random() < 0.15) {
      const dir = p5.Vector.fromAngles(random()*PI*2, acos(2*random()-1))
      p.vx = dir.x * 1.0 * (0.5+random(0.8)) * currentAmplitude
      p.vy = dir.y * 1.0 * (0.5+random(0.8)) * currentAmplitude
      p.vz = dir.z * 1.0 * (0.5+random(0.8)) * currentAmplitude
      p.launched = true; p.life = 1
    }
  }
  if (random() < 0.05) {
    for (const sw of shockwaves) if (sw.alpha <= 0) { sw.radius=10; sw.alpha=0.8; sw.hue=stateColor.h; sw.speed=8*currentAmplitude; break }
  }
} else if (!isBursting) {
  burstPhase = max(0, burstPhase - 0.01)
  for (const p of particles) if (p.launched) {
    const dist = sqrt(p.x*p.x + p.y*p.y + p.z*p.z)
    if (dist > 5) { p.vx -= p.x/dist * 0.02; p.vy -= p.y/dist * 0.02; p.vz -= p.z/dist * 0.02 }
    else { p.launched=false; p.vx=p.vy=p.vz=0 }
  }
}

// Update shockwaves
for (const sw of shockwaves) if (sw.alpha > 0) { sw.radius += sw.speed; sw.alpha *= 0.97; sw.speed *= 0.99 }

// Update particles (gravity, drag, life decay)...

// Draw particles
beginShape(POINTS)
for (const p of particles) {
  const dist = sqrt(p.x*p.x + p.y*p.y + p.z*p.z)
  const speed = sqrt(p.vx*p.vx + p.vy*p.vy + p.vz*p.vz)
  if (p.launched) {
    bright = map(p.life, 0, 1, 30, 100)
    alpha = map(p.life, 0, 1, 10, 90) * (0.5+speed*2)
    hue = (stateColor.h + p.hueOffset + speed*50) % 360
  } else {
    bright = 40 + currentAmplitude*20 + noise(p.x*0.01,p.y*0.01,time*0.5)*20
    alpha = 30 + currentAmplitude*30
    hue = (stateColor.h + p.hueOffset + noise(p.x*0.01,p.y*0.01,time*0.5)*20) % 360
  }
  stroke(hue, stateColor.s, bright, alpha)
  strokeWeight(p.baseSize * p.life * (0.5+currentAmplitude*0.5))
  vertex(p.x, p.y, p.z)
}
endShape()

// Draw shockwaves
noFill()
for (const sw of shockwaves) if (sw.alpha > 0.01) {
  stroke(sw.hue, 80, 90, sw.alpha*60)
  strokeWeight(2)
  sphere(sw.radius)
}
```

**Best for:** Dramatic "speaking = energy release" metaphor

---

## State Mapping from `$voicePlayback`

| `$voicePlayback.status` | Visual State | Amplitude |
|------------------------|--------------|-----------|
| `idle` | `idle` | 0.05 + noise |
| `preparing` | `thinking` | 0.2 + noise |
| `speaking` | `speaking` | 0.6 + noise |

```javascript
const stateMap = { idle: 'idle', preparing: 'thinking', speaking: 'speaking' }
const ampMap = { idle: 0.05, preparing: 0.2, speaking: 0.7 }
currentState = stateMap[pb.status]
targetAmplitude = ampMap[pb.status] + random(0.1)
```

---

## Performance Checklist

- [ ] `disableFriendlyErrors = true` in setup
- [ ] `pixelDensity(1)` in setup
- [ ] `beginShape(POINTS)` / `endShape()` not individual shapes
- [ ] Transparent background: `background(0,0,0,0)`
- [ ] `orbitControl()` for free 3D interaction
- [ ] `ResizeObserver` on container → `resizeCanvas()`
- [ ] Dynamic p5 CDN load, guard with `if (window.p5)`
- [ ] Cleanup: `p5Ref.current.remove()` on unmount