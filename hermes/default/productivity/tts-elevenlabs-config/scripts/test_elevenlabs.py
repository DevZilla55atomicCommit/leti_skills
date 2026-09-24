#!/usr/bin/env python3
"""
Quick ElevenLabs TTS test script for Hermes Agent.
Usage: python test_elevenlabs.py "Your text here" [voice_id] [model_id]
"""

import os
import sys
import json

# Load API key from .env if not in env
def load_env_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return None

api_key = os.environ.get("ELEVENLABS_API_KEY") or load_env_key()
if not api_key:
    print("ERROR: ELEVENLABS_API_KEY not set in env or ~/.hermes/.env")
    sys.exit(1)

os.environ["ELEVENLABS_API_KEY"] = api_key

from elevenlabs.client import ElevenLabs

voice_id = sys.argv[2] if len(sys.argv) > 2 else "pNInz6obpgDQGcFmaJgB"
model_id = sys.argv[3] if len(sys.argv) > 3 else "eleven_multilingual_v2"
text = sys.argv[1] if len(sys.argv) > 1 else "Hello from Hermes Agent ElevenLabs TTS test!"

try:
    client = ElevenLabs(api_key=api_key)
    
    # Verify voice exists
    voices = client.voices.get_all()
    voice_names = {v.voice_id: v.name for v in voices.voices}
    if voice_id not in voice_names:
        print(f"WARNING: Voice ID {voice_id} not found in your account.")
        print(f"Available voices: {list(voice_names.items())[:5]}...")
    
    # Generate audio
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
    )
    
    output_path = f"/tmp/elevenlabs_test_{voice_id[:8]}.mp3"
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    size = os.path.getsize(output_path)
    print(json.dumps({
        "success": True,
        "file_path": output_path,
        "size_bytes": size,
        "voice_id": voice_id,
        "voice_name": voice_names.get(voice_id, "unknown"),
        "model_id": model_id,
        "text_chars": len(text)
    }, indent=2))
    
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}, indent=2))
    sys.exit(1)