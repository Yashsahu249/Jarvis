from typing import AsyncGenerator

import httpx

from jarvis.llm.base import LLMProvider
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class GeminiProvider(LLMProvider):
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("llm.gemini")
        self.api_key = self.settings.GEMINI_API_KEY
        self.model = self.settings.GEMINI_MODEL

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self.model

    def _convert_messages(self, messages: list[dict]) -> list[dict]:
        contents = []
        system_instruction = None
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
                continue
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        return contents, system_instruction

    async def generate(
        self, messages: list[dict], stream: bool = False, **kwargs
    ) -> str | AsyncGenerator[str, None]:
        contents, system_instruction = self._convert_messages(messages)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return ""
            parts = candidates[0].get("content", {}).get("parts", [])
            return "".join(p.get("text", "") for p in parts)

    async def generate_stream(
        self, messages: list[dict], **kwargs
    ) -> AsyncGenerator[str, None]:
        contents, system_instruction = self._convert_messages(messages)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:streamGenerateContent?key={self.api_key}"
        payload = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        import json

                        data = json.loads(line.lstrip("data: "))
                        candidates = data.get("candidates", [])
                        if not candidates:
                            continue
                        parts = candidates[0].get("content", {}).get("parts", [])
                        for p in parts:
                            if text := p.get("text", ""):
                                yield text
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
