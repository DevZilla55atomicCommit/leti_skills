#!/usr/bin/env python3
"""
Meta AI Responses API → OpenAI Chat Completions Adapter
Production-ready adapter for Meta's muse-spark-1.1 model.
Translates Hermes' Chat Completions format to Meta's Responses API format.
Includes proper SSE streaming support for Meta's event-based streaming.
"""
import os
import json
import uuid
import time
from typing import Any, Optional, Union, AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field
import httpx
import uvicorn

app = FastAPI(title="Meta AI Adapter", version="1.0.0")

META_API_KEY = os.environ.get("META_API_KEY")
META_BASE_URL = "https://api.meta.ai/v1"
META_MODEL = "muse-spark-1.1"

if not META_API_KEY:
    raise RuntimeError("META_API_KEY environment variable required")


class ChatMessage(BaseModel):
    role: str
    content: Union[str, list]
    name: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    model_config = ConfigDict(extra="allow")


def convert_messages_to_input(messages: list[ChatMessage]) -> list[dict]:
    """Convert OpenAI messages format to Meta Responses API input format."""
    input_items = []
    for msg in messages:
        content = msg.content
        if isinstance(content, str):
            content = [{"type": "input_text", "text": content}]
        elif isinstance(content, list):
            new_content = []
            for part in content:
                if isinstance(part, dict) and "type" in part:
                    new_content.append(part)
                elif isinstance(part, str):
                    new_content.append({"type": "input_text", "text": part})
                else:
                    new_content.append({"type": "input_text", "text": str(part)})
            content = new_content

        input_items.append({
            "role": msg.role,
            "content": content
        })
    return input_items


def convert_response_to_chat(data: dict) -> dict:
    """Convert Meta Responses API output to OpenAI Chat Completions format."""
    text_content = ""
    for output_item in data.get("output", []):
        if output_item.get("type") == "message":
            for content_part in output_item.get("content", []):
                if content_part.get("type") == "output_text":
                    text_content += content_part.get("text", "")

    usage = data.get("usage", {})
    return {
        "id": data.get("id", "").replace("resp_", "chatcmpl-"),
        "object": "chat.completion",
        "created": int(data.get("created_at", 0)),
        "model": META_MODEL,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": text_content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": usage.get("input_tokens", 0),
            "completion_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0)
        }
    }


def _chunk(chat_id: str, created: int, delta: str, first: bool) -> str:
    """Build a single SSE chunk."""
    if first:
        chunk = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": META_MODEL,
            "choices": [{
                "index": 0,
                "delta": {"role": "assistant", "content": delta},
                "finish_reason": None
            }]
        }
    else:
        chunk = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": META_MODEL,
            "choices": [{
                "index": 0,
                "delta": {"content": delta},
                "finish_reason": None
            }]
        }
    return f"data: {json.dumps(chunk)}\n\n"


def _final_chunk(chat_id: str, created: int) -> str:
    """Build final SSE chunk with finish_reason."""
    chunk = {
        "id": chat_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": META_MODEL,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    return f"data: {json.dumps(chunk)}\n\n"


async def stream_meta_response(resp: httpx.Response) -> AsyncGenerator[str, None]:
    """Convert Meta's SSE streaming to OpenAI Chat Completions SSE format."""
    chat_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created = int(time.time())
    first_chunk = True
    
    current_event = None
    async for line in resp.aiter_lines():
        line = line.strip()
        if not line:
            continue
        
        # Parse SSE format: event: <name> / data: <json>
        if line.startswith("event: "):
            current_event = line[7:].strip()
            continue
        
        if line.startswith("data: "):
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                yield _final_chunk(chat_id, created)
                yield "data: [DONE]\n\n"
                break
            
            try:
                event_data = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            
            # Handle Meta's streaming events
            # The actual text deltas come in response.output_text.delta events
            if current_event == "response.output_text.delta":
                delta_text = event_data.get("delta", "")
                if delta_text:
                    yield _chunk(chat_id, created, delta_text, first_chunk)
                    first_chunk = False
            
            # Reset event after processing data
            current_event = None


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    """Translate Chat Completions request to Meta Responses API."""
    try:
        # Convert messages to Meta input format
        input_items = convert_messages_to_input(req.messages)
        
        # Build Meta API request
        meta_payload = {
            "model": META_MODEL,
            "input": input_items,
            "stream": req.stream,
        }
        
        if req.temperature is not None:
            meta_payload["temperature"] = req.temperature
        if req.max_tokens is not None:
            meta_payload["max_output_tokens"] = req.max_tokens
        if req.top_p is not None:
            meta_payload["top_p"] = req.top_p
        
        headers = {
            "Authorization": f"Bearer {META_API_KEY}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            if req.stream:
                # Streaming response
                resp = await client.post(
                    f"{META_BASE_URL}/responses",
                    headers=headers,
                    json=meta_payload,
                    timeout=None  # No timeout for streaming
                )
                
                if resp.status_code != 200:
                    error_text = await resp.aread()
                    raise HTTPException(
                        status_code=resp.status_code,
                        detail=f"Meta API error: {error_text.decode()}"
                    )
                
                return StreamingResponse(
                    stream_meta_response(resp),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "X-Accel-Buffering": "no"
                    }
                )
            else:
                # Non-streaming response
                resp = await client.post(
                    f"{META_BASE_URL}/responses",
                    headers=headers,
                    json=meta_payload
                )
                
                if resp.status_code != 200:
                    raise HTTPException(
                        status_code=resp.status_code,
                        detail=f"Meta API error: {resp.text}"
                    )
                
                meta_response = resp.json()
                return convert_response_to_chat(meta_response)
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Meta API timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Meta API connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adapter error: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok", "model": META_MODEL}


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{
            "id": META_MODEL,
            "object": "model",
            "created": 0,
            "owned_by": "meta"
        }]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)