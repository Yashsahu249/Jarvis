import asyncio
from typing import AsyncGenerator

from jarvis.llm.base import LLMProvider
from jarvis.llm.ollama_provider import OllamaProvider
from jarvis.llm.groq_provider import GroqProvider
from jarvis.llm.openrouter_provider import OpenRouterProvider
from jarvis.llm.gemini_provider import GeminiProvider
from jarvis.config.providers import get_available_providers, get_active_provider
from jarvis.utils.logger import JarvisLogger


class LLMRouter:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("llm.router")
        self.providers: dict[str, LLMProvider] = {
            "ollama": OllamaProvider(),
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
            "gemini": GeminiProvider(),
        }
        self._active_provider: str | None = None

    @property
    def active_provider(self) -> str:
        if self._active_provider is None:
            self._active_provider = get_active_provider()
        return self._active_provider

    def get_provider(self, name: str | None = None) -> LLMProvider:
        provider_name = name or self.active_provider
        provider = self.providers.get(provider_name)
        if not provider:
            self.logger.warning(
                f"Provider {provider_name} not found, falling back to ollama"
            )
            provider = self.providers["ollama"]
        return provider

    async def generate(
        self, messages: list[dict], stream: bool = False, **kwargs
    ) -> str | AsyncGenerator[str, None]:
        provider = self.get_provider()
        self.logger.info(
            f"Generating with {provider.name}/{provider.model_name}, stream={stream}"
        )
        try:
            return await provider.generate(messages, stream=stream, **kwargs)
        except Exception as e:
            self.logger.error(f"Provider {provider.name} failed: {e}")
            fallback = self._get_fallback(provider.name)
            if fallback:
                self.logger.info(f"Falling back to {fallback.name}")
                return await fallback.generate(messages, stream=stream, **kwargs)
            raise

    async def generate_stream(
        self, messages: list[dict], **kwargs
    ) -> AsyncGenerator[str, None]:
        provider = self.get_provider()
        self.logger.info(
            f"Streaming from {provider.name}/{provider.model_name}"
        )
        try:
            async for chunk in provider.generate_stream(messages, **kwargs):
                yield chunk
        except Exception as e:
            self.logger.error(f"Stream failed from {provider.name}: {e}")
            fallback = self._get_fallback(provider.name)
            if fallback:
                self.logger.info(f"Falling back stream to {fallback.name}")
                async for chunk in fallback.generate_stream(messages, **kwargs):
                    yield chunk
            raise

    def generate_sync(self, messages: list[dict], **kwargs) -> str:
        import concurrent.futures

        async def _run():
            result = await self.generate(messages, stream=False, **kwargs)
            return result

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(asyncio.run, _run())
            return fut.result(timeout=120)

    def _get_fallback(self, failed_provider: str) -> LLMProvider | None:
        available = get_available_providers()
        for name in ["ollama", "groq", "openrouter", "gemini"]:
            if name != failed_provider and available.get(name):
                return self.providers[name]
        return None


_router: LLMRouter | None = None


def get_llm_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
