# Burner Account Workflow for Instagram Access

> **Reference guide** for creating and maintaining a burner Instagram account for pipeline authentication.

---

## 🔥 Why a Burner Account?

| Risk | Main Account | Burner Account |
|------|--------------|----------------|
| Ban impact | Catastrophic (main identity) | Zero (disposable) |
| Personal data exposure | High | None |
| Rate limit sharing | Shared with personal use | Isolated |
| Cookie freshness | Manual rotation needed | Can be automated |
| Recovery if banned | Difficult/impossible | Trivial (create new) |

**Bottom line**: Burner account is **standard practice** for Instagram automation.

---

## 🛠️ Setup Procedure

### 1. Create Burner Identity

| Component | Recommendation |
|-----------|----------------|
| **Email** | ProtonMail / Tuta / SimpleLogin alias (no real name) |
| **Phone** | VoIP (Google Voice, TextNow, Hushed) or burner SIM ($5) |
| **Username** | Generic: `viewer_2024`, `scout_burner`, `ig_burner_24` |
| **Password** | Unique, generated, stored in password manager |

### 2. Isolated Browser Profile

```bash
# Create isolated Chrome profile
mkdir -p /tmp/ig_burner_profile

# Launch isolated Chrome instance
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --user-data-dir=/tmp/ig_burner_profile \
  --profile-directory=Default \
  --no-first-run \
  --no-default-browser-check \
  "https://www.instagram.com"
```

**This creates a completely isolated Chrome instance** — no shared cookies, history, or login state with your main profile.

### 3. Account Creation Flow

1. Open the isolated Chrome window
2. Go to `instagram.com` → **Sign up**
3. **Email**: Burner email
7. **Phone**: Burner number (SMS verification)
8. **Username**: Generic (e.g., `scout_burner_24`)
10. **Password**: Strong, unique, saved in password manager
11. **Profile**: Minimal — no bio, no photo, no posts, no follows

### 4. Cookie Export

1. Install **Cookie Editor** extension in the burner Chrome profile
2. Go to `instagram.com` (logged in)
3. Click Cookie Editor → **Export** → **Netscape format**
8. Save as: `burner_cookies.txt`

```bash
# Save to project directory
cp ~/Downloads/instagram_cookies.txt \
   "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/burner_cookies.txt"
```

---

## 🔧 Pipeline Integration

### Update `scripts/process_batch.py`

```python
# In download_reel() function:
cmd = [
    "yt-dlp",
    "--cookies", "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/burner_cookies.txt",
    "-f", "bestvideo+bestaudio/best",
    "--merge-output-format", "mp4",
    "-o", str(output_dir / f"{reel_code}.%(ext)s"),
    url
]
```

### Run with Burner Cookies

```bash
cd "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects"
python3 scripts/process_batch.py --batch 50 --start 0
```

---

## 🔄 Cookie Maintenance

| Frequency | Action |
|-----------|--------|
| **Weekly** | Verify cookies still work: `yt-dlp --cookies burner_cookies.txt "https://www.instagram.com/reel/DaxUaKYuhb0/"` |
| **Monthly** | Re-export cookies from burner profile |
| **On 403/429** | Re-export immediately |
| **After Instagram updates** | Re-export after major app updates |

### Cookie Format (Netscape Format)
```
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	TRUE	1735689600	sessionid	your_session_id
.instagram.com	TRUE	/	TRUE	1735689600	ds_user_id	your_user_id
.instagram.com	TRUE	/	TRUE	1735689600	csrftoken	your_csrf_token
.instagram.com	TRUE	/	TRUE	1735689600	mid	your_mid
.instagram.com	TRUE	/	TRUE	1735689600	ig_did	your_ig_did
```

---

## 🚨 Security Rules

| Rule | Rationale |
|------|-----------|
| **Never** use main account | Protects identity & content |
| **Never** post/like/comment from burner | Looks like bot behavior |
| **Never** follow accounts from burner | Looks like bot behavior |
| **Only** view reels | Mimics normal browsing |
| **Delete** cookies file after use | No credential leakage |
| **Rotate** burner account every 3-6 months | Prevents pattern detection |

---

## 🔄 Cookie File Location

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/burner_cookies.txt
```

**Pipeline Integration:**
```python
# In process_batch.py download_reel():
cmd = [
    "yt-dlp",
    "--cookies", str(VAULT_BASE / "burner_cookies.txt"),
    "-f", "bestvideo+bestaudio/best",
    "--merge-output-format", "mp4",
    "-o", str(output_dir / f"{reel_code}.%(ext)s"),
    url
]
```

---

## 🚨 Troubleshooting

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `403 Forbidden` | Cookies expired | Re-export cookies |
| `429 Too Many Requests` | Rate limited | Wait 1 hour, reduce batch size |
| `404 Not Found` | Content deleted | Skip (log in SKIPPED_URLS.md) |
| `Login required` | Age-gated/geo-blocked | Use age-verified burner account |
| `Private account` | Account is private | Skip (cannot access) |

---

## 📁 File Locations

| File | Path |
|------|------|
| Burner cookies | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/burner_cookies.txt` |
| Chrome profile | `/tmp/ig_burner_profile` |
| Pipeline script | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/scripts/process_batch.py` |
| Queue file | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/VIDEO_EFFECTS_QUEUE.md` |
| Processed tracking | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/PROCESSED_REELS.json` |

---

## 🎯 Quick Commands

```bash
# Test burner cookies
yt-dlp --cookies burner_cookies.txt "https://www.instagram.com/reel/DaxUaKYuhb0/"

# Run batch with burner
python3 scripts/process_batch.py --batch 10 --start 50

# Refresh cookies (manual)
# 1. Open burner Chrome profile
# 2. Go to instagram.com (auto-login)
# 3. Cookie Editor → Export → burner_cookies.txt
# 3. Copy to project directory
```

---

*Part of the Instagram → DaVinci Video Effects Pipeline*  
*References: `SKILL.md` | `skipped-urls.md` | `visual-asset-pipeline.md`*