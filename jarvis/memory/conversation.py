import uuid
from typing import AsyncGenerator
from pathlib import Path

from jarvis.memory.store import get_memory_store
from jarvis.llm.router import get_llm_router
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class ConversationManager:
    def __init__(self):
        self.store = get_memory_store()
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("memory.conversation")
        self._session_id: str | None = None

    @property
    def session_id(self) -> str:
        if self._session_id is None:
            self._session_id = str(uuid.uuid4())
        return self._session_id

    def set_session(self, session_id: str):
        self._session_id = session_id

    def add_user_message(self, content: str):
        self.store.add_message(self.session_id, "user", content)

    def add_assistant_message(self, content: str):
        self.store.add_message(self.session_id, "assistant", content)
        self._auto_export()

    def get_history(self) -> list[dict[str, str]]:
        return self.store.get_history(
            self.session_id, limit=self.settings.MEMORY_MAX_HISTORY
        )

    def clear(self):
        self.store.clear_history(self.session_id)

    def build_context(self, system_prompt: str, additional_context: str = "") -> list[dict]:
        messages = [{"role": "system", "content": system_prompt}]

        if additional_context:
            messages.append({"role": "system", "content": additional_context})

        summary = self.store.get_latest_summary(self.session_id)
        if summary:
            messages.append(
                {
                    "role": "system",
                    "content": f"Previous conversation summary: {summary}",
                }
            )

        messages.extend(self.get_history())
        return messages

    def _auto_export(self):
        try:
            from jarvis.memory.export import export_session_to_json, export_session_to_text
            history = self.store.get_history(self.session_id, limit=9999)
            if history:
                export_session_to_json(self.session_id, history)
                export_session_to_text(self.session_id, history)
        except Exception as e:
            self.logger.debug(f"Auto-export failed (non-critical): {e}")

    async def summarize_if_needed(self):
        history = self.get_history()
        if len(history) >= self.settings.MEMORY_MAX_HISTORY:
            msgs = [{"role": "system", "content": "Summarize this conversation concisely:"}]
            msgs.extend(history)
            router = get_llm_router()
            try:
                summary = await router.generate(msgs)
                if summary:
                    self.store.save_summary(
                        self.session_id, summary, len(history)
                    )
                    self.logger.info("Conversation summarized")
            except Exception as e:
                self.logger.error(f"Summarization failed: {e}")


_manager: ConversationManager | None = None


def get_conversation_manager() -> ConversationManager:
    global _manager
    if _manager is None:
        _manager = ConversationManager()
    return _manager
