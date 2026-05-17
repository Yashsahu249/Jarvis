import re
import time
import asyncio
from pathlib import Path
from typing import Any


def sanitize_text(text: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)


def truncate_text(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def detect_language(text: str) -> str:
    if not text.strip():
        return "unknown"
    hindi_chars = re.findall(r"[\u0900-\u097F]", text)
    english_chars = re.findall(r"[a-zA-Z]", text)
    total = len(hindi_chars) + len(english_chars)
    if total == 0:
        return "unknown"
    hindi_ratio = len(hindi_chars) / total
    if hindi_ratio > 0.7:
        return "hindi"
    elif hindi_ratio > 0.1:
        return "hinglish"
    return "english"


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_read_file(path: str | Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def chunk_text(text: str, chunk_size: int = 2000) -> list[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


async def async_retry(
    func: callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    **kwargs,
) -> Any:
    last_exc = None
    for attempt in range(max_retries):
        try:
            return await func(**kwargs)
        except Exception as e:
            last_exc = e
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (backoff**attempt))
    raise last_exc
