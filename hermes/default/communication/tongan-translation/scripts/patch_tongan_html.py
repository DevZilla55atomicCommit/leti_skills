#!/usr/bin/env python3
"""
Reserve script for patching the escalated sections once authoritative Tongan
is available. Do NOT hand-fabricate Tongan in this file. Only use source:
https://github.com/kool60545/tongan-english-dictionary or the official Church
Tongan scriptures or the deep-method skill output.

Current verified replacements (from official Church Tongan scriptures Ps 23:1):
"""
# Status: BLOCKED on remaining sections pending verified translation.
# The only section patched so far is the subtitle, using official Ps 23:1:
#   "Ko hoku Tauhi a Jihova (Sāme 23:1)"
# Remaining ESCALATED sections require either:
#   A) cloud model once 429 resets, OR
#   B) a fluent Tongan speaker, OR
#   C) official Church Tongan scriptures for each anchor verse.
# Do NOT fill them with fabricated Tongan.

import sys

# Patch only if authoritative source provided via CLI args
# format: python patch_tongan_html.py '<english>' '<verified_tongan>'
if __name__ == '__main__':
    if len(sys.argv) == 3:
        from pathlib import Path
        path = Path("/Users/alfredkamisese/Desktop/Come Follow Me 2026/2026-08-Week4_Psalms_Aug17-23/Psalms_Lesson_Tongan.html")
        html = path.read_text(encoding="utf-8")
        english, tongan = sys.argv[1], sys.argv[2]
        if english in html and tongan:
            html = html.replace(english, tongan, 1)
            path.write_text(html, encoding="utf-8")
            print(f"Patched: {english[:50]} => {tongan}")
        else:
            print("English text not found or no Tongan provided.")
    else:
        print("Usage: python patch_tongan_html.py '<english>' '<verified_tongan>'")
        print("Only patch with VERIFIED Tongan. Do not fabricate.")