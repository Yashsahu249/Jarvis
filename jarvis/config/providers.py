from jarvis.config.settings import get_settings


def get_available_providers() -> dict[str, bool]:
    s = get_settings()

    providers = {
        "ollama": True,
        "openrouter": bool(s.OPENROUTER_API_KEY),
        "groq": bool(s.GROQ_API_KEY),
        "gemini": bool(s.GEMINI_API_KEY),
    }
    return providers


def get_active_provider() -> str:
    s = get_settings()
    providers = get_available_providers()

    if s.LLM_PROVIDER in providers and providers[s.LLM_PROVIDER]:
        return s.LLM_PROVIDER

    for p in ["ollama", "groq", "openrouter", "gemini"]:
        if providers[p]:
            return p

    return "ollama"
