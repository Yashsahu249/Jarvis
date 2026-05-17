import pytest

from jarvis.utils.helpers import sanitize_text, truncate_text, detect_language, chunk_text
from jarvis.utils.validators import validate_model_name, validate_url, is_safe_filename


def test_sanitize_text():
    assert sanitize_text("hello\x00world") == "helloworld"
    assert sanitize_text("normal text") == "normal text"


def test_truncate_text():
    assert truncate_text("hello", 10) == "hello"
    assert len(truncate_text("a" * 100, 10)) == 13  # 10 + "..."
    assert truncate_text("a" * 100, 10).endswith("...")


def test_chunk_text():
    chunks = chunk_text("hello world", 5)
    assert len(chunks) >= 2


def test_model_name_validation():
    assert validate_model_name("qwen2.5:3b") is True
    assert validate_model_name("") is False
    assert validate_model_name("mistral") is True


def test_url_validation():
    assert validate_url("https://example.com") is True
    assert validate_url("not-a-url") is False
    assert validate_url("http://localhost:8000") is True


def test_safe_filename():
    assert is_safe_filename("test.py") is True
    assert is_safe_filename("../evil") is False
    assert is_safe_filename("hello world") is False
