from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.models.schemas import MemoryEntry, MemorySearchResult, MemorySearchRequest
from app.services.memory_service import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("/conversations")
async def list_conversations(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    conversations = await memory_service.get_conversations(limit=limit, offset=offset)
    return {"conversations": conversations, "total": len(conversations)}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    conv = await memory_service.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    result = await memory_service.delete_conversation(conversation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted", "conversation_id": conversation_id}


@router.get("/search", response_model=MemorySearchResult)
async def search_memory(query: str = Query(...), limit: int = Query(10, ge=1, le=100), type_filter: str | None = Query(None, alias="type")):
    import time
    start = time.time()
    results = await memory_service.search_memory(query=query, limit=limit, type_filter=type_filter)
    time_taken = time.time() - start
    return MemorySearchResult(
        query=query,
        results=[MemoryEntry(**r) for r in results],
        total=len(results),
        time_taken=time_taken,
    )


@router.get("/stats")
async def get_memory_stats():
    stats = await memory_service.get_stats()
    return stats


@router.post("/entries")
async def store_memory(entry: MemoryEntry):
    mem_id = await memory_service.store_memory(
        type_=entry.type,
        content=entry.content,
        metadata=entry.metadata,
        importance=entry.importance or 0.0,
    )
    return {"id": mem_id, "status": "stored"}


@router.delete("/entries")
async def clear_memory():
    await memory_service.clear_memory()
    return {"status": "cleared"}
