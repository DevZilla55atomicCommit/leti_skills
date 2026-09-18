---
name: hermes-profile-skills-dedup
description: Dedup profile skills mirroring shared to reclaim 20+ GB.
category: cleanup
version: 1.0.0
---

# Hermes Profile Skills Deduplication

A skill to audit and safely deduplicate Hermes Agent profile `skills/` folders that duplicate the shared `~/.hermes/skills/`, reclaiming 20-40+ GB on multi-profile setups.

## When to Use

- Multiple Hermes profiles exist (beyond `default`)
- Disk space is low on `/System/Volumes/Data`
- Profile `skills/` folders appear identical to shared skills
- Setting up a new machine (MacBook Pro) with same profile structure

## Prerequisites

- Hermes Agent installed with multiple profiles
- Profiles located at `~/.hermes/profiles/<name>/`
- Shared skills at `~/.hermes/skills/`

## Workflow

### 1. Audit Profile Skills

```bash
# List all profiles
ls ~/.hermes/profiles/

# Check each profile's skills folder size
for p in ~/.hermes/profiles/*/; do
  profile=$(basename "$p")
  if [ -d "$p/skills" ]; then
    size=$(du -sh "$p/skills" 2>/dev/null | cut -f1)
    count=$(ls "$p/skills" 2>/dev/null | wc -l)
    echo "$profile: $size ($count skills)"
  else
    echo "$profile: no local skills (uses shared)"
  fi
done

# Compare with shared skills
shared_count=$(ls ~/.hermes/skills | wc -l)
echo "Shared: $shared_count skills"
```

### 2. Verify Duplication

```bash
# For each profile with skills/, compare to shared
for p in ~/.hermes/profiles/*/skills/; do
  profile=$(basename $(dirname "$p"))
  diff <(ls "$p" | sort) <(ls ~/.hermes/skills | sort) >/dev/null && \
    echo "$profile: IDENTICAL to shared" || \
    echo "$profile: DIFFERS from shared"
done
```

### 3. Safe Deduplication

**Only proceed if all profiles show IDENTICAL to shared.**

```bash
# Remove duplicated skills folders (keeps shared as fallback)
for p in ~/.hermes/profiles/*/; do
  profile=$(basename "$p")
  if [ "$profile" != "default" ] && [ -d "$p/skills" ]; then
    echo "Removing $profile/skills..."
    rm -rf "$p/skills"
  fi
done
```

> **Why skip `default`?** The default profile is the orchestrator and may need all skills. Specialized profiles (apollo, helios, hephaestus, hestia, kairos, etc.) fall back to shared automatically.

### 4. Verify Cleanup

```bash
# Confirm skills folders gone
for p in ~/.hermes/profiles/*/; do
  profile=$(basename "$p")
  if [ -d "$p/skills" ]; then
    echo "$profile: STILL HAS local skills"
  else
    echo "$profile: OK (uses shared)"
  fi
done

# Check disk space reclaimed
df -h /System/Volumes/Data
```

### 5. Optional: Curate Per-Profile Subsets

After deduplication, create minimal skill sets per profile:

```bash
# Example: Apollo (creative) only needs creative/video skills
mkdir -p ~/.hermes/profiles/apollo/skills
for s in creative videography videographer davinci-resolve davinci-resolve-techniques cinematography-techniques photography-techniques video-effects video-storyboard-generation design ui-ux-pro-max camera-hardware visual-spec-best-practices; do
  ln -s ~/.hermes/skills/$s ~/.hermes/profiles/apollo/skills/
done
```

## Safety Notes

- **Hermes fallback behavior**: When a profile lacks `skills/`, it automatically uses `~/.hermes/skills/`
- **Never delete `~/.hermes/skills/`** — that's the source of truth
- **Backup first** if uncertain: `cp -r ~/.hermes/profiles ~/.hermes/profiles.backup.$(date +%s)`
- **Test one profile first** — remove one, restart Hermes, verify skills load

## Expected Savings

| Profiles | Skills Each | Shared Size | Savings |
|----------|-------------|-------------|---------|
| 5 specialized | 154 | ~6.9 GB | ~27 GB |
| 8 specialized | 154 | ~6.9 GB | ~48 GB |

## Automation

Add as a cron job for monthly audits:

```bash
# Monthly audit - runs first Monday 6 AM
cronjob create \
  --name "Hermes Skills Deduplication Audit" \
  --schedule "0 6 * * 1" \
  --prompt "Run hermes-profile-skills-dedup audit on all profiles" \
  --skills ["hermes-profile-skills-dedup"]
```

## References

- Hermes profile structure: `~/.hermes/profiles/<name>/`
- Shared skills: `~/.hermes/skills/`
- Profile config: `~/.hermes/profiles/<name>/config.yaml`