#!/bin/bash
# Meta AI Adapter launcher for LaunchAgent
# Runs the FastAPI adapter that translates OpenAI Chat Completions to Meta's Responses API

export META_API_KEY="${META_API_KEY}"
export PYTHONPATH="/Users/alfredkamisese/Library/Python/3.9/lib/python/site-packages"

exec /Library/Developer/CommandLineTools/usr/bin/python3 /Users/alfredkamisese/meta-adapter/meta_adapter.py