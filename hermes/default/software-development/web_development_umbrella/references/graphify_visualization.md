# Graphify 3D Visualization Pipeline (Reference)

- **Data Source**: Extracted from Obsidian vault (2,500 nodes, 7,742 links, 305 communities)
- **Core Files**: 
  - `graph-data.json` (≈902 KB) – node and link graph
  - `layout.json` (≈161 KB) – layout configuration
- **Build‑time Embedding**:
  - Moved files to `src/components/Graph/data/` and imported via `@/components/Graph/data/graph-data.json`
  - Eliminates runtime fetch stalls; data is bundled with the Next.js build
- **Visualization Features**:
  - Central glowing sphere with Fresnel shader + pulse animation + particle field
  - 2,500 node spheres colored by community
  - 7,742 lightning‑bolt shaders between connected nodes
  - UnrealBloomPass for cinematic glow
  - OrbitControls with damping
- **Post‑Processing**: 
  - Bloom, ambient occlusion, and depth‑based shading for depth perception
- **Pitfalls & Fixes**:
  - **Module‑not‑found errors**: Relative import paths broke after moving files; fix by using the `@/components/Graph/data/` alias.
  - **Build failures**: Missing `resolveJsonModule` in `tsconfig.json`; add `"resolveJsonModule": true`.
  - **Rate limiting**: Sub‑agent calls to NVIDIA API hit 429; mitigate by batching tasks and reducing concurrency.
  - **Large JSON stalls**: Browser fetch hangs on >900 KB responses; solution is build‑time import, not runtime fetch.
- **Outcome**: Fully functional 3D force‑directed graph with animated links, ready for Next.js + Three.js/WebGL integration.

*Saved for future reference: 2026‑07‑18, Alfred (Maddie)*