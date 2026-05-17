import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import settings


def setup_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add(
        settings.LOG_FILE,
        rotation="10 MB",
        retention="1 week",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")

    from app.services.memory_service import memory_service
    await memory_service.initialize()

    from app.services.browser_service import browser_service
    from app.services.agent_service import agent_service

    app.state.memory_service = memory_service
    app.state.browser_service = browser_service
    app.state.agent_service = agent_service

    from app.api.system import _start_time
    global _start_time
    _start_time = time.time()

    logger.info(f"{settings.APP_NAME} v{settings.VERSION} started on {settings.HOST}:{settings.PORT}")
    yield

    logger.info("Shutting down...")
    if browser_service.browser:
        await browser_service.close_browser()
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Jarvis OS - AI-Powered Operating System Assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    from app.api.system import _request_count, _request_times
    global _request_count, _request_times
    _request_count += 1
    _request_times.append(time.time())
    _request_times[:] = [t for t in _request_times if time.time() - t < 60]

    logger.debug(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "path": request.url.path})


from app.api import chat, voice, agents, browser, repos, memory, system, tools

app.include_router(chat.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(browser.router, prefix="/api")
app.include_router(repos.router, prefix="/api")
app.include_router(memory.router, prefix="/api")
app.include_router(system.router, prefix="/api")
app.include_router(tools.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "uptime": time.time() - getattr(app.state, "start_time", time.time()),
    }


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/api/health",
    }
