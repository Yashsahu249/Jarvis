import json
import uuid
import time
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import aiosqlite
from loguru import logger
from app.core.config import settings


class MemoryService:
    def __init__(self):
        self.db_path = settings.MEMORY_DB_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    async def _get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute("PRAGMA foreign_keys=ON")
        return conn

    async def initialize(self):
        conn = await self._get_connection()
        try:
            await conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}'
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding BLOB,
                    metadata TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    importance REAL DEFAULT 0.0
                );
                CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
                CREATE INDEX IF NOT EXISTS idx_memory_type ON memory_entries(type);
                CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory_entries(importance);
            """)
            await conn.commit()
            logger.info(f"Memory database initialized at {self.db_path}")
        finally:
            await conn.close()

    async def store_conversation(self, conversation_id: str | None = None, title: str = "New Conversation") -> str:
        conn = await self._get_connection()
        try:
            if conversation_id:
                existing = await conn.execute_fetchall("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
                if existing:
                    return conversation_id

            cid = conversation_id or str(uuid.uuid4())
            now = datetime.now(timezone.utc).isoformat()
            await conn.execute(
                "INSERT OR IGNORE INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (cid, title, now, now),
            )
            await conn.commit()
            return cid
        finally:
            await conn.close()

    async def store_message(self, conversation_id: str, role: str, content: str, metadata: dict | None = None) -> str:
        conn = await self._get_connection()
        try:
            msg_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc).isoformat()
            meta_json = json.dumps(metadata or {})
            await conn.execute(
                "INSERT INTO messages (id, conversation_id, role, content, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)",
                (msg_id, conversation_id, role, content, now, meta_json),
            )
            await conn.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id)
            )
            await conn.commit()
            return msg_id
        finally:
            await conn.close()

    async def get_conversations(self, limit: int = 50, offset: int = 0) -> list[dict]:
        conn = await self._get_connection()
        try:
            rows = await conn.execute_fetchall(
                "SELECT c.*, (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count "
                "FROM conversations c ORDER BY c.updated_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
            return [dict(r) for r in rows]
        finally:
            await conn.close()

    async def get_conversation(self, conversation_id: str) -> dict | None:
        conn = await self._get_connection()
        try:
            rows = await conn.execute_fetchall(
                "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
            )
            if not rows:
                return None
            conv = dict(rows[0])
            msg_rows = await conn.execute_fetchall(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,),
            )
            conv["messages"] = [dict(m) for m in msg_rows]
            if isinstance(conv.get("metadata"), str):
                conv["metadata"] = json.loads(conv["metadata"])
            return conv
        finally:
            await conn.close()

    async def delete_conversation(self, conversation_id: str) -> bool:
        conn = await self._get_connection()
        try:
            await conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            await conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            await conn.commit()
            return True
        finally:
            await conn.close()

    async def clear_all_conversations(self):
        conn = await self._get_connection()
        try:
            await conn.execute("DELETE FROM messages")
            await conn.execute("DELETE FROM conversations")
            await conn.commit()
        finally:
            await conn.close()

    async def search_memory(self, query: str, limit: int = 10, type_filter: str | None = None) -> list[dict]:
        conn = await self._get_connection()
        try:
            terms = query.lower().split()
            sql = "SELECT * FROM memory_entries WHERE "
            conditions = []
            params: list[str] = []
            for term in terms:
                conditions.append("LOWER(content) LIKE ?")
                params.append(f"%{term}%")
            if type_filter:
                conditions.append("type = ?")
                params.append(type_filter)
            sql += " AND ".join(conditions) if conditions else "1=1"
            sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
            params.append(str(limit))

            rows = await conn.execute_fetchall(sql, params)
            results = []
            for r in rows:
                d = dict(r)
                if isinstance(d.get("metadata"), str):
                    d["metadata"] = json.loads(d["metadata"])
                results.append(d)
            return results
        finally:
            await conn.close()

    async def get_stats(self) -> dict:
        conn = await self._get_connection()
        try:
            conv_count = (await conn.execute_fetchall("SELECT COUNT(*) as c FROM conversations"))[0]["c"]
            msg_count = (await conn.execute_fetchall("SELECT COUNT(*) as c FROM messages"))[0]["c"]
            mem_count = (await conn.execute_fetchall("SELECT COUNT(*) as c FROM memory_entries"))[0]["c"]
            db_size = Path(self.db_path).stat().st_size if Path(self.db_path).exists() else 0
            return {
                "conversations": conv_count,
                "messages": msg_count,
                "memory_entries": mem_count,
                "database_size_bytes": db_size,
                "database_path": self.db_path,
            }
        finally:
            await conn.close()

    async def store_memory(self, type_: str, content: str, metadata: dict | None = None, importance: float = 0.0) -> str:
        conn = await self._get_connection()
        try:
            mem_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc).isoformat()
            meta_json = json.dumps(metadata or {})
            await conn.execute(
                "INSERT INTO memory_entries (id, type, content, metadata, created_at, updated_at, importance) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (mem_id, type_, content, meta_json, now, now, importance),
            )
            await conn.commit()
            return mem_id
        finally:
            await conn.close()

    async def clear_memory(self):
        conn = await self._get_connection()
        try:
            await conn.execute("DELETE FROM memory_entries")
            await conn.commit()
        finally:
            await conn.close()


memory_service = MemoryService()
