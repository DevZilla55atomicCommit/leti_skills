# 3D Visualization Debug Checklist

## Pre-Flight Checks

1. **Install dependencies**
   ```bash
   cd /Users/alfredkamisese/vault-graph-viz
   npm install three @react-three/fiber @react-three/drei
   ```

2. **Verify TypeScript types**
   ```bash
   npx tsc --noEmit
   ```

3. **Start dev server**
   ```bash
   npm run dev
   ```

## Runtime Diagnostics

### Console Logging Verification
- Verify `Force-directed complete` logs show non-zero ranges
- Check `NodeField rendering positions` shows sample nodes with x,y,z values
- Confirm `LightningLinks rendering` shows edge connections with color codes

### Visual Validation

1. Open http://localhost:3003
2. Use mouse to orbit - verify depth perception
3. Expect to see:
   - Point cloud of nodes (not flat grid)
   - Connected edges forming network
   - Legend filtering works on click
4. Press 'R' to reset camera framing
5. Check browser devtools console for error messages

## Root Cause Analysis Templates

### Issue: All nodes at z=0
- Check `src/types/vault.ts` - is `z` optional (`?`)?
- In `GraphCanvas.tsx` verify force-directed mutation writes `z` values
- Add `n.z = n.z ?? 0` before logging

### Issue: Empty render (no nodes/edges)
- Console logs show 0 for node count or empty arrays
- Check API response at `/api/vault/canvas` has data
- Verify GraphCanvas receives props: {nodes: [...], edges: [...]}

### Issue: Wrong camera framing
- Check `cameraPosition` and `cameraFOV` props
- Verify graph bounding sphere calculation
- Test auto-camera-framing code snippet

## Verification Script

### Quick Validation
```bash
# Check build output
npm run build

# Count nodes in API response
curl http://localhost:3000/api/vault/canvas | jq '.nodes | length'
curl http://localhost:3000/api/vault/canvas | jq '.edges | length'

# Check browser console for debug logs
# Look for "Force-directed complete" with non-zero ranges
# Look for "NodeField rendering positions" showing sample nodes
```

### Expected Output Examples
```json
// API response sample
{
  "nodes": [
    {
      "id": "root",
      "x": -3.2,
      "y": 4.1,
      "z": 2.5,
      "connections": 4
    }
    // ... total 197 nodes
  ],
  "edges": [
    {
      "source": "root",
      "target": "child1",
      "label": ""
    }
    // ... total 96 edges
  ]
}
```

## Common Fixes Summary

| Symptom | Likely Cause | Fix |
|--------|--------------|-----|
| 2D grid layout | `z` not propagated to renderer | Make `z: number` required in `ProcessedNode` |
| No nodes visible | Empty nodes array or zero positions | Add debug logs to verify data flow |
| Camera doesn't frame graph | Fixed camera distance too small | Compute distance from bounding sphere |
| Flickering nodes | Size attenuation issues | Adjust `size` and `sizeAttenuation` parameters |