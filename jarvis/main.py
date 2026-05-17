"""Jarvis FastAPI server."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from jarvis.llm.router import get_llm_router
from jarvis.memory.conversation import get_conversation_manager
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT
from jarvis.tools.registry import get_tool_registry
from jarvis.utils.logger import JarvisLogger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = JarvisLogger.get_logger("server")
    logger.info("Jarvis server starting")
    yield
    logger.info("Jarvis server shutting down")


app = FastAPI(title="Jarvis API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = JarvisLogger.get_logger("server.api")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    stream: bool = True


class ChatResponse(BaseModel):
    response: str
    session_id: str


from fastapi.responses import StreamingResponse
import json


@app.post("/chat")
async def chat(req: ChatRequest):
    cm = get_conversation_manager()
    llm = get_llm_router()

    if req.session_id:
        cm.set_session(req.session_id)

    cm.add_user_message(req.message)
    context = cm.build_context(SYSTEM_PROMPT)

    if req.stream:
        async def event_stream():
            full = ""
            try:
                stream = await llm.generate(context, stream=True)
                if hasattr(stream, "__aiter__"):
                    async for chunk in stream:
                        full += chunk
                        yield json.dumps({"chunk": chunk}) + "\n"
                else:
                    full = stream
                    yield json.dumps({"chunk": stream}) + "\n"
            except Exception as e:
                yield json.dumps({"error": str(e)}) + "\n"
            finally:
                cm.add_assistant_message(full)

        return StreamingResponse(
            event_stream(),
            media_type="application/x-ndjson",
        )

    response = await llm.generate(context, stream=False)
    cm.add_assistant_message(response)

    return ChatResponse(
        response=response,
        session_id=cm.session_id,
    )


@app.post("/clear")
async def clear(session_id: str | None = None):
    cm = get_conversation_manager()
    if session_id:
        cm.set_session(session_id)
    cm.clear()
    return {"status": "memory cleared", "session_id": cm.session_id}


@app.get("/tools")
async def list_tools():
    registry = get_tool_registry()
    return {"tools": registry.list_tools()}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "provider": get_llm_router().active_provider,
    }
