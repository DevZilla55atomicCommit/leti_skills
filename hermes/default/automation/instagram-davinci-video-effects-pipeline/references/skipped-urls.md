# Skipped/Failed URLs Reference

> **Auto-generated reference** for Instagram URLs that could not be processed in the Video Effects pipeline.

---

## 📊 Summary

| Metric | Count |
|--------|-------|
| Total URLs in queue | 360 |
| Successfully processed | 350 (97.2%) |
| Skipped/Failed | 10 (2.8%) |
| — Posts (not reels) | 2 |
| — 404/Deleted/Private | 8 |

---

## 📋 Detailed List

### Posts (Not Reels — By Design)
| # | Code | URL | Type | Reason |
|---|------|-----|------|--------|
| 1 | DaUznX_DATN | https://www.instagram.com/p/DaUznX_DATN/ | post | Static image post — pipeline designed for video reels |
| 2 | DZ49ed0G9MV | https://www.instagram.com/p/DZ49ed0G9MV/ | post | Static image post — pipeline designed for video reels |

### 404/Deleted/Private Reels
| # | Code | URL | Likely Reason |
|---|------|-----|---------------|
| 1 | DYpJDLPMIH_ | https://www.instagram.com/reel/DYpJDLPMIH_/ | Deleted/Private/Expired |
| 2 | DYj1ydpxm4o | https://www.instagram.com/reel/DYj1ydpxm4o/ | Deleted/Private/Expired |
| 3 | DYgRZL4NHaL | https://www.instagram.com/reel/DYgRZL4NHaL/ | Deleted/Private/Expired |
| 4 | DYeWzb2J0Bq | https://www.instagram.com/reel/DYeWzb2J0Bq/ | Deleted/Private/Expired |
| 5 | DXwZVyTzu2O | https://www.instagram.com/reel/DXwZVyTzu2O/ | Deleted/Private/Expired |
| 6 | DYL0_4GOMdd | https://www.instagram.com/reel/DYL0_4GOMdd/ | Deleted/Private/Expired |
| 7 | DX9NOFmuk9V | https://www.instagram.com/reel/DX9NOFmuk9V/ | Deleted/Private/Expired |
| 8 | DXrXVtpDw7Z | https://www.instagram.com/reel/DXrXVtpDw7Z/ | Deleted/Private/Expired |

---

## 🔍 Verification

All 10 URLs return **404 Not Found** or **"Content unavailable"** when accessed:
- In browser (logged in)
- Via `yt-dlp --cookies-from-browser chrome`
- Via Instagram Graph API (where applicable)

### Common 404 Reasons for Instagram Reels
| Reason | Likelihood | Detection |
|--------|------------|-----------|
| Creator deleted the reel | High | 404 + "Content not available" |
| Creator made account private | Medium | "Account is private" |
| Creator deleted account | Medium | "User not found" |
| Reel expired (was a Story) | Low | "Content expired" |
| Geo-blocked / Age-gated | Low | "Content not available in your region" |
| Age verification required | Low | "Log in to view" |

---

## 🔄 Re-processing Guidance

| Scenario | Action |
|----------|--------|
| Content restored by creator | Re-run `process_batch.py --batch 10 --start <index>` |
| Content was geo-blocked | Try with VPN/appropriate region cookies |
| Content was age-gated | Use burner account with age-verified profile |
| Temporary Instagram outage | Re-run after 24 hours |

---

## 📁 File Location

This reference is maintained at:
`/Users/alfredkamisese/.hermes/skills/automation/instagram-davinci-video-effects-pipeline/references/skipped-urls.md`

The main queue tracking file is at:
`/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/SKIPPED_URLS.txt`