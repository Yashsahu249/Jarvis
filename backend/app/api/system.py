import os
import time
import json
import psutil
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.core.config import settings
from app.models.schemas import SystemStatus, SystemMetrics, LogEntry

router = APIRouter(prefix="/system", tags=["system"])

_start_time = time.time()
_request_count = 0
_request_times: list[float] = []


def record_request():
    global _request_count
    _request_count += 1


@router.get("/status", response_model=SystemStatus)
async def system_status():
    import app.services.browser_service as bs
    import app.services.agent_service as ag

    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    uptime = time.time() - _start_time

    llm_connected = False
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            llm_connected = resp.status_code == 200
    except Exception:
        pass

    active_agents = sum(1 for a in ag.agent_service.list_agents() if a["status"] == "busy")
    active_browsers = 1 if bs.browser_service.browser else 0

    return SystemStatus(
        status="healthy",
        version=settings.VERSION,
        uptime=uptime,
        cpu_percent=cpu,
        memory_percent=memory,
        active_agents=active_agents,
        active_browsers=active_browsers,
        llm_provider=settings.LLM_PROVIDER,
        llm_connected=llm_connected,
    )


@router.get("/metrics", response_model=SystemMetrics)
async def system_metrics():
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = time.time() - _start_time

    now = datetime.now(timezone.utc).isoformat()
    requests_per_min = 0
    avg_response = 0
    if _request_times:
        recent = [t for t in _request_times if time.time() - t < 60]
        requests_per_min = len(recent)
        avg_response = 0

    return SystemMetrics(
        cpu_percent=cpu,
        memory_percent=memory,
        disk_percent=disk,
        uptime_seconds=uptime,
        active_connections=0,
        requests_total=_request_count,
        requests_per_minute=requests_per_min,
        avg_response_time_ms=avg_response,
        timestamp=now,
    )


@router.get("/logs", response_model=list[LogEntry])
async def get_logs(limit: int = Query(50, ge=1, le=500)):
    log_file = settings.LOG_FILE
    entries = []
    if os.path.exists(log_file):
        try:
            with open(log_file) as f:
                lines = f.readlines()[-limit:]
            for line in lines:
                try:
                    parts = line.strip().split(" | ")
                    if len(parts) >= 3:
                        entries.append(LogEntry(
                            timestamp=parts[0],
                            level=parts[1].strip(),
                            message=" | ".join(parts[2:]),
                        ))
                    else:
                        entries.append(LogEntry(
                            timestamp=datetime.now().isoformat(),
                            level="INFO",
                            message=line.strip(),
                        ))
                except Exception:
                    pass
        except Exception as e:
            logger.warning(f"Failed to read logs: {e}")

    return entries[-limit:]


@router.get("/ollama/status")
async def ollama_status():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            if resp.status_code == 200:
                return {"status": "connected", "host": settings.OLLAMA_HOST}
            return {"status": "error", "host": settings.OLLAMA_HOST, "detail": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"status": "disconnected", "host": settings.OLLAMA_HOST, "detail": str(e)}


@router.get("/ollama/models")
async def ollama_models():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                return {"models": data.get("models", [])}
            return {"models": [], "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"models": [], "error": str(e)}


@router.post("/ollama/pull")
async def ollama_pull(model: str = Query(...)):
    try:
        payload = {"name": model, "stream": False}
        async with httpx.AsyncClient(timeout=300) as client:
            resp = await client.post(f"{settings.OLLAMA_HOST}/api/pull", json=payload)
            if resp.status_code == 200:
                return {"status": "pulled", "model": model}
            return {"status": "error", "model": model, "detail": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
