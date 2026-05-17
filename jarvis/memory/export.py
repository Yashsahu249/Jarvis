import json
import os
import shutil
from pathlib import Path
from datetime import datetime

from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


CHAT_DIR = Path("/mnt/hdd/Downloads/saved chat data")


def ensure_chat_dir():
    CHAT_DIR.mkdir(parents=True, exist_ok=True)
    return CHAT_DIR


def export_session_to_json(session_id: str, messages: list[dict]) -> Path:
    ensure_chat_dir()
    safe_name = session_id[:8]
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CHAT_DIR / f"chat_{safe_name}_{now}.json"
    data = {
        "session_id": session_id,
        "exported_at": datetime.now().isoformat(),
        "message_count": len(messages),
        "messages": messages,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


def export_session_to_text(session_id: str, messages: list[dict]) -> Path:
    ensure_chat_dir()
    safe_name = session_id[:8]
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CHAT_DIR / f"chat_{safe_name}_{now}.txt"
    lines = []
    lines.append(f"Jarvis Chat Export")
    lines.append(f"{'='*50}")
    lines.append(f"Session: {session_id}")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Messages: {len(messages)}")
    lines.append("")
    for msg in messages:
        role = msg.get("role", "?").upper()
        content = msg.get("content", "")
        ts = msg.get("timestamp", "")
        lines.append(f"[{ts}] {role}")
        lines.append(content)
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def export_all_sessions(store) -> list[Path]:
    exported = []
    conn = store._get_conn()
    c = conn.cursor()
    c.execute("SELECT DISTINCT session_id FROM conversations ORDER BY session_id")
    sessions = [row[0] for row in c.fetchall()]
    for sid in sessions:
        c.execute(
            "SELECT role, content, timestamp FROM conversations WHERE session_id=? ORDER BY id",
            (sid,),
        )
        messages = [
            {"role": row[0], "content": row[1], "timestamp": row[2]} for row in c.fetchall()
        ]
        if messages:
            jp = export_session_to_json(sid, messages)
            tp = export_session_to_text(sid, messages)
            exported.extend([jp, tp])
    conn.close()
    return exported


def get_storage_stats():
    ensure_chat_dir()
    total_size = 0
    files = []
    for f in CHAT_DIR.iterdir():
        if f.is_file():
            total_size += f.stat().st_size
            files.append(f.name)
    free_space = shutil.disk_usage(CHAT_DIR).free
    return {
        "path": str(CHAT_DIR),
        "file_count": len(files),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "free_space_gb": round(free_space / (1024 ** 3), 2),
        "files": sorted(files),
    }
