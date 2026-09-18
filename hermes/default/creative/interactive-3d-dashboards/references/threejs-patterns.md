# Three.js Patterns for Interactive Dashboards

## Import Map (ESM via unpkg)
```html
<script type="importmap">
{ "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
} }
</script>
```
Then: `import * as THREE from 'three';` and `import { OrbitControls } from 'three/addons/controls/OrbitControls.js';`

## Material Cheatsheet

| Material | Use Case | Key Props |
|----------|----------|-----------|
| `MeshBasicMaterial` | Unlit, UI elements, glows | `color`, `transparent`, `opacity` |
| `MeshStandardMaterial` | PBR, lit objects | `color`, `metalness`, `roughness` |
| `MeshPhysicalMaterial` | Advanced PBR (clearcoat, transmission) | `clearcoat`, `clearcoatRoughness`, `transmission` |
| `PointsMaterial` | Particles | `size`, `vertexColors`, `sizeAttenuation`, `blending` |
| `LineBasicMaterial` | Wireframes, axes | `color`, `linewidth` (limited support) |

## Geometry Disposal Pattern
```javascript
function disposeObject(obj) {
  if (obj.geometry) obj.geometry.dispose();
  if (obj.material) {
    if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
    else obj.material.dispose();
  }
  // Recurse children
  obj.children.forEach(disposeObject);
}
```

## CSS2DObject Label Helper
```javascript
function createLabel(html, position, className = 'panel') {
  const div = document.createElement('div');
  div.className = className;
  div.innerHTML = html;
  const label = new CSS2DObject(div);
  label.position.copy(position);
  return label;
}
// Add to scene: scene.add(label);
// Remove: label.element.remove(); scene.remove(label);
```

## Curve & Tube Geometry
```javascript
const points = [new THREE.Vector3(0,0,0), new THREE.Vector3(10,10,10)];
const curve = new THREE.CatmullRomCurve3(points);
const tubeGeo = new THREE.TubeGeometry(curve, 20, 0.5, 8, false);
```

## ShapeGeometry from Data (Radar Charts)
```javascript
const shape = new THREE.Shape();
data.forEach((val, i) => {
  const angle = (i / n) * Math.PI * 2 - Math.PI / 2;
  const x = Math.cos(angle) * radius * val;
  const y = Math.sin(angle) * radius * val;
  i === 0 ? shape.moveTo(x, y) : shape.lineTo(x, y);
});
const geo = new THREE.ShapeGeometry(shape);
```

## InstancedMesh for Performance (1000+ objects)
```javascript
const mesh = new THREE.InstancedMesh(geometry, material, count);
const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set(x, y, z);
  dummy.scale.set(sx, sy, sz);
  dummy.updateMatrix();
  mesh.setMatrixAt(i, dummy.matrix);
}
mesh.instanceMatrix.needsUpdate = true;
scene.add(mesh);
```

## Animation Loop Template
```javascript
let time = 0;
function animate() {
  requestAnimationFrame(animate);
  time += 0.016; // ~60fps delta
  // Update objects...
  controls.update();
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}
```

## Resize Handler
```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  labelRenderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Fog for Depth
```javascript
scene.fog = new THREE.FogExp2(0x0a0e1a, 0.0015); // color matches background
```

## Shadow Setup
```javascript
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
// Light
dirLight.castShadow = true;
dirLight.shadow.mapSize.set(2048, 2048);
dirLight.shadow.camera.near = 10; far = 300;
dirLight.shadow.camera.left = -100; right = 100; top = 100; bottom = -100;
// Objects
mesh.castShadow = true;
ground.receiveShadow = true;
```

## Post-Processing (Optional)
```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85));
// In animate: composer.render(); instead of renderer.render()
```