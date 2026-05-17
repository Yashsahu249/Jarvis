import re
from pathlib import Path


def validate_path(path: str) -> str | None:
    if not path or not path.strip():
        return "Path is empty"
    p = Path(path).resolve()
    if not p.exists():
        return f"Path does not exist: {path}"
    return None


def validate_command(command: str) -> str | None:
    dangerous_patterns = [
        r"\brm\s+-rf\s+/",
        r"\bshutdown\b",
        r"\breboot\b",
        r"\b:\(\)\s*\{\s*:\s*\|\s*:&\s*\};:\b",
        r"\bmkfs\b",
        r"\bdd\b",
        r">\s*/dev/",
        r"\bsudo\b",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            return f"Dangerous command blocked: {command}"
    return None


def validate_model_name(model: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_.\-/:]+$", model))


def validate_url(url: str) -> bool:
    return bool(re.match(r"^https?://[^\s/$.?#].[^\s]*$", url))


def is_safe_filename(name: str) -> bool:
    if not name:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_\-\.]+$", name)) and ".." not in name
