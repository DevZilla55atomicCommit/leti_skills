# CSS2D Label Patterns for Three.js Dashboards

## Basic Label Creation
```javascript
function createLabel(html, position, className = 'label') {
  const div = document.createElement('div');
  div.className = className;
  div.innerHTML = html;
  const label = new CSS2DObject(div);
  label.position.copy(position);
  return label;
}
```

## Label CSS Classes

### Standard Panel Label
```css
.label.panel {
  background: rgba(10, 18, 35, 0.92);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.75rem;
  min-width: 100px;
  text-align: center;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  white-space: nowrap;
}
```

### Small Inline Label
```css
.label.small {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.65rem;
  color: #aaa;
}
```

### Highlighted Value Label
```css
.label.value {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  font-weight: 700;
  text-shadow: 0 0 8px currentColor;
}
.label.value.brazil { color: #00ff88; }
.label.value.norway { color: #ff4444; }
.label.value.draw   { color: #ffcc00; }
```

## Positioning Strategies

### Above Object (Y-offset)
```javascript
const label = createLabel('85%', new THREE.Vector3(0, height + 8, 0));
mesh.add(label); // Attach to mesh so it moves with it
```

### World Position (Fixed in Scene)
```javascript
const label = createLabel('Brazil Total: 85%', new THREE.Vector3(-30, 15, 40));
scene.add(label); // Fixed world position
```

### Screen-Space Anchor (CSS2D)
```javascript
// CSS2DObjects automatically project to screen space
// Just set position in world coordinates
label.position.set(x, y, z);
```

## Dynamic Label Updates
```javascript
function updateLabel(label, newHtml) {
  label.element.innerHTML = newHtml;
}

// For animated values (e.g., counting up)
function animateValue(label, start, end, duration = 1000) {
  const startTime = performance.now();
  function step(now) {
    const t = Math.min(1, (now - startTime) / duration);
    const val = start + (end - start) * t;
    label.element.textContent = `${val.toFixed(1)}%`;
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
```

## Label Lifecycle Management

### Add to View
```javascript
function addLabelToView(key, label) {
  scene.add(label);
  viewLabels.set(key, label); // Map for cleanup
}
```

### Cleanup on View Switch
```javascript
function clearLabels() {
  viewLabels.forEach(label => {
    label.element.remove();
    scene.remove(label);
  });
  viewLabels.clear();
}
```

## Multi-line Labels with HTML
```javascript
const html = `
  <div style="line-height: 1.4;">
    <div style="font-weight: 700; color: #00d4ff;">Scenario A</div>
    <div style="font-size: 0.7rem; color: #8ab4f8;">Brazil Controls & Wins</div>
    <div style="font-size: 1.5rem; font-weight: 700; color: #00cc44; margin-top: 4px;">45%</div>
    <div style="font-size: 0.6rem; color: #668; margin-top: 2px;">2-0 or 3-1 most likely</div>
  </div>
`;
const label = createLabel(html, position);
```

## Performance Tips

1. **Reuse label objects** — Don't create/destroy every frame; update `.element.innerHTML`
2. **Limit total labels** — Keep under ~50 for smooth 60fps on mobile
3. **Use `pointerEvents: none`** on label renderer DOM element
4. **Batch updates** — Collect all label changes, apply once per frame
5. **Hide off-screen labels** — Check `label.element.style.display = 'none'` when far from camera

## Common Issues

| Issue | Fix |
|-------|-----|
| Labels behind objects | CSS2D always renders on top; check z-index of label renderer (5) |
| Labels flicker on rotate | Ensure `labelRenderer.render(scene, camera)` called AFTER `renderer.render()` |
| Text blurry on retina | Set `renderer.setPixelRatio(window.devicePixelRatio)` |
| Labels don't appear | Check `labelRenderer.domElement` is in DOM and visible |
| Memory leak | Always `.element.remove()` and `scene.remove(label)` on cleanup |

## Animation: Label Follow Mesh
```javascript
// In animate loop
labels.forEach(({label, mesh, offset}) => {
  // Get mesh world position
  const pos = new THREE.Vector3();
  mesh.getWorldPosition(pos);
  pos.add(offset);
  label.position.copy(pos);
});
```