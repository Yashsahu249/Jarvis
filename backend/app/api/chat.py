import json
import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends, Query
from sse_starlette.sse import EventSourceResponse
from loguru import logger
from app.models.schemas import ChatRequest, ChatMessage
from app.services.llm_service import llm_service
from app.services.memory_service import memory_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def send_message(req: ChatRequest):
    conversation_id = await memory_service.store_conversation(req.conversation_id)

    await memory_service.store_message(conversation_id, "user", req.message)

    messages = []
    conv = await memory_service.get_conversation(conversation_id)
    if conv:
        for msg in conv.get("messages", [])[-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    response_text = ""
    async for chunk in llm_service.chat_stream(messages):
        response_text += chunk

    await memory_service.store_message(conversation_id, "assistant", response_text)

    return {
        "message": ChatMessage(role="assistant", content=response_text, timestamp=datetime.now(timezone.utc).isoformat()),
        "conversation_id": conversation_id,
    }


@router.post("/streaming")
async def streaming_chat(req: ChatRequest):
    conversation_id = await memory_service.store_conversation(req.conversation_id)

    await memory_service.store_message(conversation_id, "user", req.message)

    messages = []
    conv = await memory_service.get_conversation(conversation_id)
    if conv:
        for msg in conv.get("messages", [])[-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    async def event_generator():
        full_response = ""
        try:
            async for chunk in llm_service.chat_stream(messages):
                full_response += chunk
                yield {"event": "token", "data": json.dumps({"token": chunk})}

            await memory_service.store_message(conversation_id, "assistant", full_response)
            yield {
                "event": "done",
                "data": json.dumps({
                    "conversation_id": conversation_id,
                    "full_response": full_response,
                }),
            }
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield {"event": "error", "data": json.dumps({"error": str(e)})}

    return EventSourceResponse(event_generator())


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    conversation_id = None
    try:
        data = await websocket.receive_json()
        conversation_id = data.get("conversation_id")
        message = data.get("message", "")
    except Exception:
        await websocket.send_json({"error": "Invalid message format"})
        await websocket.close()
        return

    if not message:
        await websocket.send_json({"error": "Message is required"})
        await websocket.close()
        return

    conversation_id = await memory_service.store_conversation(conversation_id)
    await memory_service.store_message(conversation_id, "user", message)

    messages = []
    conv = await memory_service.get_conversation(conversation_id)
    if conv:
        for msg in conv.get("messages", [])[-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    full_response = ""
    try:
        async for chunk in llm_service.chat_stream(messages):
            full_response += chunk
            await websocket.send_json({"type": "token", "token": chunk})
            await asyncio.sleep(0.01)

        await memory_service.store_message(conversation_id, "assistant", full_response)
        await websocket.send_json({
            "type": "done",
            "conversation_id": conversation_id,
            "full_response": full_response,
        })
    except Exception as e:
        logger.error(f"WebSocket streaming error: {e}")
        await websocket.send_json({"type": "error", "error": str(e)})
    finally:
        await websocket.close()


@router.get("/history")
async def get_history(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    conversations = await memory_service.get_conversations(limit=limit, offset=offset)
    return {"conversations": conversations, "total": len(conversations)}


@router.delete("/history")
async def clear_history():
    await memory_service.clear_all_conversations()
    return {"status": "cleared"}
