# Resolve Project Storage Hygiene (keep the internal SSD clean)

Resolve's working set — render cache, optimized media, gallery stills, project
backups, render output — grows to tens of GB per project. Keep all of it on an
external scratch volume so the internal SSD hosts only the app itself.

## One-time setup (do once)

- Resolve → Preferences → **Media Storage**: add the scratch volume first and create
  `Resolve/{Cache,Gallery,Optimized,Projects,Renders}/` on it.
- Preferences → Media Storage: point cache / gallery / optimized-media at those folders.
- Project Settings → Master Settings: render-cache format DNxHR LB for editing
  (smallest proxy-grade cache; switch to HQ only for finishing passes).
- Project Manager → Project Backups: relocate off `~/Movies/` onto the scratch volume.
- Deliver page: default render output → `Renders/` on the scratch volume.
- Qualify the scratch drive BEFORE assigning it — see
  `macos-storage-cleanup` → `references/external-scratch-disk.md`
  (rank by sequential WRITE; never assign a drive already >85% full).

## Per-project open (2 min)

1. Mount the scratch volume BEFORE launching Resolve — cache writes fail to missing volumes.
2. New project → File → Project Settings → confirm cache + gallery paths resolve to scratch.
3. Import with **Copy to** scratch when footage arrives on internal (cards, downloads) —
   never edit from `~/Downloads` or Desktop.

## Post-project closeout (leaves ~0 bytes behind)

1. Playback → Delete Render Cache → All (the big one — the export is permanent, the cache served its purpose).
2. Media Pool → Delete Optimized Media for that project.
3. File → Export Project (`.drp`) + Export Project Archive into `Projects/<Name>/`.
4. Verify the archive opens, then delete working cache remnants.

## Static libraries

`~/Movies/Fairlight Sound Library/` and similar static content can move to external
with a symlink back (same move+link trick as CacheClip) — Resolve keeps working
unchanged, as long as the volume is mounted whenever Resolve runs.
