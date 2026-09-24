# 2026-07-20 Overnight Run — Session Reference

## Run Summary
- **Started**: 2026-07-20 14:33 (Samsung LED external SSD)
- **Process**: PID 15880 (`proc_141af4499dda`)
- **Script**: `download_instagram_collections.py` (custom async + yt-dlp nightly)
- **Config**: 2 concurrent, 5 retries, 300s timeout, exponential backoff
- **Cookies**: `cookies_www.instagram.com_2026-07-19.txt` (sessionid expires ~30 days)

## Progress at 16:37 (2+ hours)
| Metric | Value |
|--------|-------|
| Collections started | 41 / 117 |
| Items downloaded | 1,030 / 3,504 (29%) |
| Failed URLs | 2 (AI collection — deleted/private) |
| Disk used | 52 GB / 120 GB |
| ETA | ~3-4 more hours |

## Collections Completed (41)
AI (4), Animal_potrait (1), Aperture (2), Apple_LOG (1), Apple_Shortcuts (1), Audio_Effects (1), Billards (1), Blackmagic_App (1), Blending_Modes (1), Bracketing (1), Business_Tricks (1), Camera (6), Canva_Hack (1), Capcut (4), Car_Shooting_tips (24), Cheat_Card (1), Cinematic (78), Claude (4), Collage (1), Color_Grading_Assets (1), Color_grading (186), Content_creators_idea (1), Cooking_Recipes (1), Cooking_shooting (1), Creating_Jarvis (1), Cybersecurity (1), DRS_20 (2), DR_Making_CG (1), DR_Masking (1), DR_Noise_Reduction (2), DR_Photo_Editing (1), DaVinci (8), DaVinci_Tricks (113), Dance (3), Directing_Board (1), Dji_Gimbals_Tips (6), Dressing (3), Drone (57), Exercise (1), Export_Photos (5), Export_Videos (30 — in progress)

## Collections Remaining (76)
Filters (1), Fitness (201), Focusing_shooting (4), Fonts (1), Food_for_thoughts (2), Footage_Collection (20), Fun_games (6), Games (1), Gimbal (6), Gimbal_Moves (237), Health (2), Ideas_for_Shooting_Videos (398), Lens (2), Life (141), Lifestyle (1), Lighting (25), Lightroom (191), Mac_Tips (2), Masking_Color_Subjects (3), Masking_Video_Edits (3), Medicine (1), Mens_Fashions (13), Osmo_Gimbal (1), Out_of_camera_Video_profile (1), PS5_Tips (1), Panning_Photography (1), Parallax_Effect (8), Photography_2 (28), Photography_Videography (395), Photograpy (130), Photoshop (28), Piano (3), Pickleball (57), Poses (110), Post_horizontal_videos_in_reels (1), Potrait (12), Powergrade (1), Project_Ideas (51), Property_Shooting (17), Prosthetic_Workout (1), Python (2), Quotes (1), Recipe (49), Reels_tips (1), Reels_tutorials (20), Religion_ (3), S-Log_3 (3), S-Log_Convertion (1), Self_Portrait (2), Shutter_Speed (14), Skin_Retouch (10), Skin_Routine (1), Skin_tones_CG (2), Skintones (6), Slow_Models (44), Slow_Motion (7), Snapseed (3), Social_media_audience_Hooks (1), Sony_Videography_Tips (2), Sound_Design (37), Speed_Ramp (45), Sports (1), Sports_Videography (1), Stabelize_DR (1), Stabilizing_DR (5), Text_Effects (57), Transition (23), Video_Editing_Shortcut (2), Video_Effect (366), Video_shooting_style_kids (2), Videographer (62), Web_Design (28), Wedding_Videography (31), White_Balance (3)

## Biggest Remaining (by volume)
1. Ideas for Shooting Videos — 398
2. Photography/Videography — 395
3. Video Effect — 366
4. Gimbal Moves — 237
5. Fitness — 201
6. Lightroom — 191
7. Color grading — 186 remaining
8. DaVinci Tricks — 113 (done!)
8. Videographer — 62 remaining
9. Poses — 110
10. Drone — 57
11. Pickleball — 57
12. Text Effects — 57

## Key Technical Notes
- **No rate limiting issues** at 2 concurrent (well under 35 RPM/account)
- **Exponential backoff working**: 30s→60s→120s→240s→480s (only 2 URLs hit max retries)
- **Graceful shutdown tested**: SIGTERM at 14:28 finished current URLs, wrote report
- **Resume-safe**: `--continue --no-overwrites` — restart anytime
- **Cookies holding**: No expiry warnings (sessionid ~30 day lifetime)
- **Disk I/O**: Samsung LED sustaining ~5-10 MB/s writes, no bottlenecks
- **Memory**: Python process ~50 MB RSS (trivial)

## Failed URLs (2 total)
```
AI collection:
https://www.instagram.com/p/DaYFGZukjyH — failed after 5 retries (deleted/private)
https://www.instagram.com/p/DZpITAbDlIP — failed after 5 retries (deleted/private)
```

## Mid-Run Cookie Expiry (22:00 UTC)
- **Issue**: `sessionid` cookie expired July 19, 2025 16:06 UTC (mid-run on July 20)
- **Impact**: Life collection (141 URLs) and all subsequent collections failing with HTTP 400 "Bad Request"
- **Progress at failure**: 41/117 collections started, 2,818/3,504 MP4s downloaded (80%)
- **Collections affected**: Life (68/141 failing), and all remaining 75 collections
- **Action required**: Refresh cookies, restart with same script (resumes via `--continue --no-overwrites`)
- **Remaining**: ~700 URLs in 75 collections

## Next Steps (Post-Run)
1. Run `generate_master_index.py` → `MASTER_INDEX.json`
2. Run `tag_techniques_from_kb.py` → `TECHNIQUE_TAGS.json`
3. Cross-reference with DaVinci KB for technique tagging
4. Move completed collections to vault discipline folders
5. Update `instagram-saved-collections-pipeline` skill with final stats