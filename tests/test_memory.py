import pytest
import tempfile
from pathlib import Path

from jarvis.memory.store import MemoryStore
from jarvis.memory.conversation import ConversationManager


@pytest.fixture
def memory_store():
    tmp = tempfile.mktemp(suffix=".db")
    store = MemoryStore()
    store.db_path = Path(tmp)
    store._init_db()
    yield store


def test_store_add_and_get_message(memory_store):
    memory_store.add_message("test_session", "user", "hello")
    memory_store.add_message("test_session", "assistant", "hi there")
    history = memory_store.get_history("test_session")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "hello"


def test_store_clear_history(memory_store):
    memory_store.add_message("test_session", "user", "hello")
    memory_store.clear_history("test_session")
    history = memory_store.get_history("test_session")
    assert len(history) == 0


def test_store_save_and_get_memory(memory_store):
    memory_store.save_memory("user_name", "John", "preferences")
    result = memory_store.get_memory("user_name")
    assert result == "John"


def test_store_search_memories(memory_store):
    memory_store.save_memory("fav_color", "blue", "preferences")
    memory_store.save_memory("fav_food", "pizza", "preferences")
    results = memory_store.search_memories("blue")
    assert len(results) >= 1


def test_conversation_manager_init():
    cm = ConversationManager()
    assert cm.session_id is not None
    assert len(cm.session_id) > 0
