#!/usr/bin/env python3
"""
Fill the Tongan translation worksheet using the cloud model.
Marks high-risk doctrinal terms (shepherd, refuge, mercy, covenant, atonement,
soul, grace, tribe, temple, Messiah, prophecy) with ⚠ for human verification.
Only usable once the Ollama rate limit is clear.
"""
import re, sys, json, subprocess, time
from pathlib import Path

ws = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan_Translation_Worksheet.md")
out = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan_DRAFT.md")

# Doctrinal terms that need human verification (model often hallucinates)
RISK_WORDS = [
    "shepherd", "refuge", "mercy", "covenant", "atonement", "soul", "grace",
    "anoint", "Messiah", "prophecy", "temple", "redeem", "salvation", "Savior",
    "righteousness", "wicked", "psalmist", "lament", "fortress", "deliverer",
    "courage", "redeem"
]

def translate_cloud(english):
    """Translate via cloud model with a strict prompt."""
    prompt = (
        f"Translate this Christian Sunday School teaching sentence into correct, "
        f"natural Tongan (Lea faka-Tonga). Use proper macrons and fakau'a. "
        f"If a word has no standard Tongan equivalent, keep it in English in parentheses. "
        f"Answer with ONLY the Tongan sentence, no explanation: \n"
        f"ENGLISH: {english}"
    )
    try:
        r = subprocess.run(["ollama", "run", "nemotron-3-ultra:cloud", prompt],
                          capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            out_text = r.stdout.strip()
            # Remove thinking preamble
            if "Thinking..." in out_text[:50]:
                idx = out_text.rfind("...done thinking.")
                if idx > 0:
                    out_text = out_text[idx+len("...done thinking."):].strip()
            return out_text
        return None
    except Exception as e:
        print(f"  err: {e}")
        return None

def flag_risk(text):
    """Return ⚠ list of doctrinal terms in the English needing human review."""
    flags = [w for w in RISK_WORDS if re.search(r'\b' + re.escape(w), text, re.IGNORECASE)]
    return flags

# Parse worksheet blocks
content = ws.read_text(encoding="utf-8")
blocks = re.split(r'(?=^## )', content, flags=re.MULTILINE)

output_lines = []
output_lines.append("# Psalms Lesson — Tongan Translation DRAFT (model-generated, needs REVIEW)")
output_lines.append("")
output_lines.append("⚠ = contains doctrinal term a fluent speaker MUST verify (model may hallucinate).")
output_lines.append("Scripture quotes: use the OFFICIAL rendering already in the HTML, not this draft.")
output_lines.append("")
output_lines.append("---")
output_lines.append("")

skipped = []
for block in blocks:
    block = block.strip()
    if not block or block.startswith("# Psalms Lesson") or block.startswith("# "):
        continue
    if not block.startswith("## "):
        continue
    
    em = re.search(r"\*\*English:\*\*\s*(.+)", block)
    if not em:
        output_lines.append(block)
        output_lines.append("")
        continue
    english = em.group(1).strip()
    
    # Print progress
    label = block.split("\n")[0].replace("## ", "")
    print(f"[{label[:45]}] " + english[:50])
    
    tongan = translate_cloud(english)
    time.sleep(1.5)  # be gentle on rate limit
    
    if tongan:
        risks = flag_risk(english)
        risk_mark = f" ⚠ {' | '.join(risks)}" if risks else ""
        # Replace the Tongan blank
        block = re.sub(r"\*\*Tongan:\*\*\s*$", f"**Tongan:** {tongan}{risk_mark}", block, flags=re.MULTILINE)
        output_lines.append(block)
    else:
        skipped.append(label)
        output_lines.append(block)  # keep blank
    output_lines.append("")

out.write_text("\n".join(output_lines), encoding="utf-8")
print(f"\nDone. Wrote {out.name}")
print(f"Skipped (rate limit/errors): {skipped if skipped else 'none'}")

# Count filled vs blank
filled = sum(1 for l in output_lines if "**Tongan:** " in l and l.strip().endswith("⚠") or ("**Tongan:** " in l and len(l.split("**Tongan:** ")[1].strip()) > 3))
print(f"Filled: {filled}")