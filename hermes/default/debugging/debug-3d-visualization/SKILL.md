---
name: debug-3d-visualization
description: Debug workflow for 3D node rendering issues in vault graph visualization
---
# Debug 3D Visualization in Vault Graph

## Common Issues
- Nodes render as 2D grid instead of 3D positions
- Only grid/axes visible, no nodes or edges
- Type definition `z?: number` causing positions to be treated as optional

## Debug Steps
1. Check `src/types/vault.ts` - ensure `ProcessedNode` has `z: number`
2. Add debug logging to `src/components/GraphCanvas.tsx` to verify force-directed output
3. Add console logs to `NodeField.tsx` and `LightningLinks.tsx` to verify positions reach GPU
4. Verify camera framing in `Scene.tsx`

## Files Modified
- `src/types/vault.ts`
- `src/components/GraphCanvas.tsx`
- `src/components/NodeField.tsx`
- `src/components/LightningLinks.tsx`

## Verification
- Run `npm run build`
- Check browser console for debug logs
- Verify 3D point cloud appears with depth