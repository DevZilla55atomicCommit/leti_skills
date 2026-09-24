#!/usr/bin/env python3
"""
Generate custom notification sounds using ElevenLabs TTS.
Requires ELEVENLABS_API_KEY in ~/.hermes/.env

Outputs to ~/.hermes/desktop-plugins/custom-notifications/sounds/
"""

import os
import sys
from pathlib import Path

try:
    from elevenlabs import ElevenLabs
except ImportError:
    print("Installing elevenlabs...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "elevenlabs"], check=True)
    from elevenlabs import ElevenLabs

# Load API key from .env
env_path = Path.home() / '.hermes' / '.env'
api_key = None
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith('ELEVENLABS_API_KEY='):
            api_key = line.split('=', 1)[1].strip()
            break

if not api_key:
    print("ERROR: ELEVENLABS_API_KEY not found in ~/.hermes/.env")
    print("Add it like: ELEVENLABS_API_KEY=your_key_here")
    sys.exit(1)

client = ElevenLabs(api_key=api_key)

# Voice settings for "youthful pro female British"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.5,
    "use_speaker_boost": True
}

# Notification phrases - short and distinct
NOTIFICATIONS = {
    "turnComplete": "Done.",
    "approvalNeeded": "Permission needed.",
    "toolComplete": "Tool finished.",
    "error": "Error occurred.",
}

OUTPUT_DIR = Path.home() / '.hermes' / 'desktop-plugins' / 'custom-notifications' / 'sounds'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Generating sounds to {OUTPUT_DIR}...")

for name, text in NOTIFICATIONS.items():
    output_path = OUTPUT_DIR / f"{name}.mp3"
    print(f"  Generating {name}: '{text}'")
    
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel - young professional female
            model_id="eleven_multilingual_v2",
            voice_settings=VOICE_SETTINGS,
            output_format="mp3_44100_128"
        )
        
        with open(output_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"    ✓ Saved to {output_path}")
    except Exception as e:
        print(f"    ✗ Failed: {e}")

print("\nDone! Reload desktop plugins (⌘K → Reload desktop plugins)")
print("Then open the Custom Notifications pane and load each .mp3 file for the corresponding event.")