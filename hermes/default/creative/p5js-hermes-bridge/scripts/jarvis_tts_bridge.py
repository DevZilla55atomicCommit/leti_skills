#!/usr/bin/env python3
"""
JARVIS UI — Hermes TTS Bridge

This script bridges the JARVIS UI (p5.js in browser) to Hermes TTS.
It runs as a local HTTP/WebSocket server that:
1. Accepts TTS requests from the UI
2. Calls Hermes' text_to_speech_tool programmatically
3. Broadcasts state changes (idle/listening/speaking/thinking) via WebSocket
4. Provides real-time audio level data for visualization

Usage:
    python jarvis_tts_bridge.py --port 8765

Then open jarvis-voice-ui.html and it will auto-connect to ws://localhost:8765
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add Hermes to path
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
HERMES_AGENT = HERMES_HOME / "hermes-agent"
sys.path.insert(0, str(HERMES_AGENT))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jarvis-tts-bridge")

# ============================================================
# STATE MANAGEMENT
# ============================================================
class JarvisState:
    def __init__(self):
        self.state = "idle"  # idle, listening, speaking, thinking
        self.amplitude = 0.0
        self.waveform = [0.0] * 64
        self.current_text = ""
        self.websocket_clients = set()
        self._lock = asyncio.Lock()
    
    async def set_state(self, new_state: str, text: str = ""):
        async with self._lock:
            if new_state in ("idle", "listening", "speaking", "thinking"):
                self.state = new_state
                self.current_text = text
                await self.broadcast({
                    "type": "state_change",
                    "state": new_state,
                    "text": text,
                    "timestamp": time.time()
                })
    
    async def update_audio(self, amplitude: float, waveform: list):
        async with self._lock:
            self.amplitude = amplitude
            self.waveform = waveform
            await self.broadcast({
                "type": "audio_update",
                "amplitude": amplitude,
                "waveform": waveform,
                "timestamp": time.time()
            })
    
    async def broadcast(self, message: dict):
        dead = set()
        for ws in self.websocket_clients:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.add(ws)
        self.websocket_clients -= dead


jarvis = JarvisState()

# ============================================================
# PYDANTIC MODELS
# ============================================================
class TTSRequest(BaseModel):
    text: str
    provider: Optional[str] = None
    speed: Optional[float] = None
    instructions: Optional[str] = None


class StateRequest(BaseModel):
    state: str
    text: str = ""


# ============================================================
# HERMES TTS INTEGRATION
# ============================================================
async def generate_tts(text: str, provider: Optional[str] = None, 
                       speed: Optional[float] = None, 
                       instructions: Optional[str] = None) -> dict:
    """Call Hermes' text_to_speech_tool programmatically."""
    try:
        from tools.tts_tool import text_to_speech_tool
        result = text_to_speech_tool(
            text=text,
            provider=provider,
            speed=speed,
            instructions=instructions
        )
        return json.loads(result)
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return {"success": False, "error": str(e)}


async def speak_text(text: str, provider: Optional[str] = None,
                     speed: Optional[float] = None,
                     instructions: Optional[str] = None):
    """Full speak pipeline: state change -> TTS -> state change."""
    await jarvis.set_state("speaking", text)
    
    # Simulate audio levels during generation
    for i in range(10):
        amp = 0.3 + 0.5 * abs(__import__('math').sin(time.time() * 8 + i * 0.5))
        wave = [max(0, min(1, 0.1 + 0.3 * __import__('math').sin(time.time() * 12 + j * 0.3) + 0.1 * __import__('random').random())) 
                for j in range(64)]
        await jarvis.update_audio(amp, wave)
        await asyncio.sleep(0.05)
    
    result = await generate_tts(text, provider, speed, instructions)
    
    if result.get("success"):
        await jarvis.update_audio(0.8, [0.5 + 0.3 * __import__('math').sin(time.time() * 20 + j * 0.2) for j in range(64)])
        await asyncio.sleep(0.5)
    
    await jarvis.set_state("listening")
    return result


# ============================================================
# FASTAPI APP
# ============================================================
app = FastAPI(title="JARVIS TTS Bridge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the JARVIS UI
UI_DIR = Path(__file__).parent
app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")


@app.get("/")
async def root():
    return {"service": "JARVIS TTS Bridge", "status": "running", "ui": "/ui/jarvis-voice-ui.html"}


@app.get("/health")
async def health():
    return {"status": "ok", "state": jarvis.state}


@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    """Generate TTS via Hermes."""
    result = await speak_text(
        request.text,
        provider=request.provider,
        speed=request.speed,
        instructions=request.instructions
    )
    return result


@app.post("/state")
async def state_endpoint(request: StateRequest):
    """Manually set JARVIS state."""
    await jarvis.set_state(request.state, request.text)
    return {"success": True, "state": jarvis.state}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    jarvis.websocket_clients.add(websocket)
    
    # Send initial state
    await websocket.send_text(json.dumps({
        "type": "init",
        "state": jarvis.state,
        "amplitude": jarvis.amplitude,
        "waveform": jarvis.waveform
    }))
    
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            if msg.get("type") == "tts":
                asyncio.create_task(speak_text(
                    msg.get("text", ""),
                    provider=msg.get("provider"),
                    speed=msg.get("speed"),
                    instructions=msg.get("instructions")
                ))
            elif msg.get("type") == "state":
                await jarvis.set_state(msg.get("state", "idle"), msg.get("text", ""))
            elif msg.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        jarvis.websocket_clients.discard(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        jarvis.websocket_clients.discard(websocket)


# ============================================================
# BACKGROUND TASKS
# ============================================================
async def idle_animation():
    """Keep subtle animation running in idle/listening states."""
    while True:
        await asyncio.sleep(0.05)
        if jarvis.state in ("idle", "listening"):
            if jarvis.state == "idle":
                amp = 0.1 + 0.05 * __import__('math').sin(time.time() * 0.5)
                wave = [max(0, min(1, 0.05 + 0.03 * __import__('math').sin(time.time() * 1 + j * 0.2) + 0.02 * __import__('random').random()))
                        for j in range(64)]
            else:  # listening
                amp = 0.15 + 0.1 * __import__('math').sin(time.time() * 1.5)
                wave = [max(0, min(1, 0.1 + 0.08 * __import__('math').sin(time.time() * 3 + j * 0.15) + 0.05 * __import__('random').random()))
                        for j in range(64)]
            await jarvis.update_audio(amp, wave)


# ============================================================
# ENTRY POINT
# ============================================================
UI_DIR = Path(__file__).parent

def main():
    import argparse
    parser = argparse.ArgumentParser(description="JARVIS TTS Bridge")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind")
    parser.add_argument("--ui-path", default=None, help="Path to JARVIS UI HTML")
    args = parser.parse_args()
    
    ui_dir = Path(args.ui_path) if args.ui_path else UI_DIR
    
    # Re-mount static files with correct path
    app.mount("/ui", StaticFiles(directory=str(ui_dir), html=True), name="ui")
    
    # Start background task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(idle_animation())
    
    # Run server
    config = uvicorn.Config(app, host=args.host, port=args.port, log_level="info")
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    main()