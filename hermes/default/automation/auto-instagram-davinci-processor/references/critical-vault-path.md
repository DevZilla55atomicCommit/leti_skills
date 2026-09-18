# Critical Vault Path — MUST USE EXACT PATH

## The Problem
The pipeline was previously writing to the WRONG vault:
```
❌ WRONG: ~/Obsidian/EMAI/Instagram Reels/
❌ WRONG: ~/Obsidian/EMAI/
❌ WRONG: ~/instagram-davinci-pipeline/vault/
```

## The Correct Path
All output MUST go to the **TamaZila Obsidian Vault** at:
```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
```

### Required Output Directories
| Artifact | Path |
|----------|------|
| Vision Reports | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports/` |
| Hermes Skills (source) | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Hermes_Skills/` |
| Vault Notes | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels/` |
| Transcripts | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Transcripts/` |
| Hermes Skills (installed) | `~/.hermes/skills/creative/` (copied from vault source) |

## Why This Matters
- The **TamaZila Obsidian Vault** is the user's actual knowledge base
- Writing to `~/Obsidian/EMAI/` creates artifacts in a DIFFERENT vault that won't be discoverable
- The DaVinci_Knowledge_Base is a specific folder structure inside TamaZila
- Hermes skills are installed from vault source to `~/.hermes/skills/creative/` for agent discovery

## Config Enforcement
```yaml
# config.yaml — ALL paths must use exact TamaZila path
paths:
  skills_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Hermes_Skills"
  vault_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Instagram_Reels"
  vision_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Vision_Reports"
  transcripts_dir: "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Transcripts"
```

## Verification Checklist
- [ ] All output paths in config.yaml point to TamaZila path
- [ ] Pipeline creates directories under TamaZila path
- [ ] Vault notes appear in TamaZila Obsidian app
- [ ] Hermes skills appear in `hermes skills list` (after install)
- [ ] No artifacts written to ~/Obsidian/EMAI/