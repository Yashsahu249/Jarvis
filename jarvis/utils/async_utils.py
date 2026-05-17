import asyncio
import threading
from typing import TypeVar, Coroutine, Any

T = TypeVar("T")

_async_loop: asyncio.AbstractEventLoop | None = None
_async_thread: threading.Thread | None = None


def _get_loop() -> asyncio.AbstractEventLoop:
    global _async_loop, _async_thread
    if _async_loop is None or _async_loop.is_closed():
        _async_loop = asyncio.new_event_loop()
        _async_thread = threading.Thread(
            target=_async_loop.run_forever, daemon=True
        )
        _async_thread.start()
    return _async_loop


def run_async(coro: Coroutine[Any, Any, T], timeout: float | None = None) -> T:
    loop = _get_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=timeout)
