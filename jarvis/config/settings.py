import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # LLM Provider defaults
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    OLLAMA_FALLBACK_MODEL: str = os.getenv("OLLAMA_FALLBACK_MODEL", "mistral")

    # Cloud provider keys
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # TAVily
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Voice
    STT_MODEL_SIZE: str = os.getenv("STT_MODEL_SIZE", "small")
    TTS_ENGLISH_MODEL: str = os.getenv(
        "TTS_ENGLISH_MODEL", "voices/en_US-lessac-medium.onnx"
    )
    TTS_HINDI_MODEL: str = os.getenv(
        "TTS_HINDI_MODEL", "voices/hi_IN-pratham-medium.onnx"
    )
    WAKE_WORD: str = os.getenv("WAKE_WORD", "jarvis")
    LISTEN_TIMEOUT: int = int(os.getenv("LISTEN_TIMEOUT", "5"))
    AUDIO_DEVICE: int | None = (
        int(os.getenv("AUDIO_DEVICE")) if os.getenv("AUDIO_DEVICE") else None
    )

    # Memory
    MEMORY_DB_PATH: str = os.getenv(
        "MEMORY_DB_PATH", str(Path("data/memory.db"))
    )
    MEMORY_MAX_HISTORY: int = int(os.getenv("MEMORY_MAX_HISTORY", "50"))
    MEMORY_ENABLE_SUMMARIZATION: bool = (
        os.getenv("MEMORY_ENABLE_SUMMARIZATION", "true").lower() == "true"
    )

    # Safety
    AUTO_EXECUTE_SAFE: bool = (
        os.getenv("AUTO_EXECUTE_SAFE", "true").lower() == "true"
    )
    REQUIRE_CONFIRMATION: bool = (
        os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
    )
    SANDBOX_ENABLED: bool = (
        os.getenv("SANDBOX_ENABLED", "true").lower() == "true"
    )

    # Server
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Browser
    BROWSER_HEADLESS: bool = (
        os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
    )
    BROWSER_VISIBLE: bool = (
        os.getenv("BROWSER_VISIBLE", "false").lower() == "true"
    )

    # Paths
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    REPO_DIR: str = os.getenv("REPO_DIR", "repos")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
