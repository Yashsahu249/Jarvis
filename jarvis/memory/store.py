import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Any

from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class MemoryStore:
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("memory.store")
        self.db_path = Path(self.settings.MEMORY_DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                timestamp TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS summarizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                summary TEXT NOT NULL,
                message_count INTEGER DEFAULT 0,
                timestamp TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_conversation_session
                ON conversations(session_id);
            CREATE INDEX IF NOT EXISTS idx_memories_key
                ON memories(key);
            """
        )
        conn.commit()
        conn.close()

    def add_message(self, session_id: str, role: str, content: str):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO conversations (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, role, content, datetime.now().isoformat()),
        )
        conn.commit()
        self.logger.debug(f"Added {role} message to session {session_id}")
        conn.close()

    def get_history(
        self, session_id: str, limit: int = 50
    ) -> list[dict[str, str]]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        ).fetchall()
        conn.close()
        return [{"role": r["role"], "content": r["content"]} for r in rows][-limit:]

    def clear_history(self, session_id: str):
        conn = self._get_conn()
        conn.execute(
            "DELETE FROM conversations WHERE session_id = ?", (session_id,)
        )
        conn.commit()
        conn.close()
        self.logger.info(f"Cleared history for session {session_id}")

    def save_memory(self, key: str, value: str, category: str = "general"):
        conn = self._get_conn()
        conn.execute(
            """INSERT INTO memories (key, value, category, timestamp)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET value = ?, category = ?, timestamp = ?""",
            (
                key,
                value,
                category,
                datetime.now().isoformat(),
                value,
                category,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        conn.close()
        self.logger.debug(f"Saved memory: {key}")

    def get_memory(self, key: str) -> str | None:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT value FROM memories WHERE key = ?", (key,)
        ).fetchone()
        conn.close()
        return row["value"] if row else None

    def search_memories(self, query: str, category: str | None = None) -> list[dict]:
        conn = self._get_conn()
        like_query = f"%{query}%"
        if category:
            rows = conn.execute(
                "SELECT key, value, category, timestamp FROM memories WHERE category = ? AND (key LIKE ? OR value LIKE ?)",
                (category, like_query, like_query),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT key, value, category, timestamp FROM memories WHERE key LIKE ? OR value LIKE ?",
                (like_query, like_query),
            ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def save_summary(self, session_id: str, summary: str, msg_count: int):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO summarizations (session_id, summary, message_count, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, summary, msg_count, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()

    def get_latest_summary(self, session_id: str) -> str | None:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT summary FROM summarizations WHERE session_id = ? ORDER BY id DESC LIMIT 1",
            (session_id,),
        ).fetchone()
        conn.close()
        return row["summary"] if row else None


_store: MemoryStore | None = None


def get_memory_store() -> MemoryStore:
    global _store
    if _store is None:
        _store = MemoryStore()
    return _store
