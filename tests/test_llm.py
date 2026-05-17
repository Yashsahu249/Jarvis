import pytest
import pytest_asyncio

from jarvis.llm.router import LLMRouter
from jarvis.llm.ollama_provider import OllamaProvider


@pytest.mark.asyncio
async def test_llm_router_initialization():
    router = LLMRouter()
    assert router.active_provider is not None
    assert "ollama" in router.providers
    assert "groq" in router.providers
    assert "openrouter" in router.providers
    assert "gemini" in router.providers


def test_ollama_provider_init():
    provider = OllamaProvider()
    assert provider.name == "ollama"
    assert provider.model_name is not None


def test_provider_has_required_methods():
    provider = OllamaProvider()
    assert hasattr(provider, "generate")
    assert hasattr(provider, "generate_stream")
    assert hasattr(provider, "name")
    assert hasattr(provider, "model_name")


@pytest.mark.asyncio
async def test_llm_router_get_provider():
    router = LLMRouter()
    provider = router.get_provider("ollama")
    assert provider.name == "ollama"

    provider = router.get_provider("nonexistent")
    assert provider.name == "ollama"
