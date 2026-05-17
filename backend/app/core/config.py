from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Jarvis OS"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    LLM_PROVIDER: str = "ollama"

    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "mixtral-8x7b-32768"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    TAVILY_API_KEY: str = ""

    STT_MODEL_SIZE: str = "base"

    MEMORY_DB_PATH: str = str(BASE_DIR / "data" / "memory.db")

    BROWSER_HEADLESS: bool = True

    AUTO_EXECUTE_SAFE: bool = True
    REQUIRE_CONFIRMATION: bool = True
    SANDBOX_ENABLED: bool = True

    CORS_ORIGINS: list[str] = ["*"]

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = str(BASE_DIR / "logs" / "jarvis.log")


settings = Settings()

os.makedirs(os.path.dirname(settings.MEMORY_DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
