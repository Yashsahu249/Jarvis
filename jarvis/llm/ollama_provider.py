from typing import AsyncGenerator

import httpx

from jarvis.llm.base import LLMProvider
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class OllamaProvider(LLMProvider):
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("llm.ollama")
        self.base_url = self.settings.OLLAMA_HOST.rstrip("/")
        self.model = self.settings.OLLAMA_MODEL
        self.fallback_model = self.settings.OLLAMA_FALLBACK_MODEL
        self._current_model = self.model

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self._current_model

    async def _call_ollama(
        self, messages: list[dict], stream: bool = False
    ) -> dict | AsyncGenerator:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self._current_model,
            "messages": messages,
            "stream": stream,
            "options": {"num_predict": 4096, "temperature": 0.7},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            if stream:
                return self._stream_response(client, url, payload)

            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def _stream_response(
        self, client: httpx.AsyncClient, url: str, payload: dict
    ) -> AsyncGenerator[str, None]:
        async with client.stream("POST", url, json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.strip():
                    continue
                try:
                    import json

                    data = json.loads(line)
                    if content := data.get("message", {}).get("content", ""):
                        yield content
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue

    async def generate(
        self, messages: list[dict], stream: bool = False, **kwargs
    ) -> str | AsyncGenerator[str, None]:
        try:
            if stream:
                return self._call_ollama(messages, stream=True)

            result = await self._call_ollama(messages, stream=False)
            return result.get("message", {}).get("content", "")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404 and self._current_model != self.fallback_model:
                self.logger.warning(
                    f"Model {self._current_model} not found, falling back to {self.fallback_model}"
                )
                self._current_model = self.fallback_model
                return await self.generate(messages, stream=stream, **kwargs)
            self.logger.error(f"Ollama error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Ollama error: {e}")
            raise

    async def generate_stream(
        self, messages: list[dict], **kwargs
    ) -> AsyncGenerator[str, None]:
        async for chunk in await self.generate(messages, stream=True, **kwargs):
            yield chunk
