from typing import AsyncGenerator

import httpx

from jarvis.llm.base import LLMProvider
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class OpenRouterProvider(LLMProvider):
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("llm.openrouter")
        self.api_key = self.settings.OPENROUTER_API_KEY
        self.model = self.settings.OPENROUTER_MODEL

    @property
    def name(self) -> str:
        return "openrouter"

    @property
    def model_name(self) -> str:
        return self.model

    async def generate(
        self, messages: list[dict], stream: bool = False, **kwargs
    ) -> str | AsyncGenerator[str, None]:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096,
            "stream": stream,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            if stream:
                return self._stream_response(client, url, payload, headers)

            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def _stream_response(
        self, client: httpx.AsyncClient, url: str, payload: dict, headers: dict
    ) -> AsyncGenerator[str, None]:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    import json

                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    if content := delta.get("content", ""):
                        yield content
                except json.JSONDecodeError:
                    continue

    async def generate_stream(
        self, messages: list[dict], **kwargs
    ) -> AsyncGenerator[str, None]:
        async for chunk in await self.generate(messages, stream=True, **kwargs):
            yield chunk
