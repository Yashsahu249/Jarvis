import json
import httpx
from typing import AsyncGenerator
from loguru import logger
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.system_prompt = (
            "You are Jarvis OS, an advanced AI operating system assistant. "
            "You help users with coding, research, system automation, and general tasks. "
            "Be concise, accurate, and helpful. Use available tools when needed."
        )

    async def chat_stream(
        self, messages: list[dict], model: str | None = None, temperature: float = 0.7, max_tokens: int | None = None
    ) -> AsyncGenerator[str, None]:
        provider = self.provider
        if model:
            provider = self._detect_provider_from_model(model)

        if provider == "ollama":
            async for chunk in self._ollama_stream(messages, model or settings.OLLAMA_MODEL, temperature):
                yield chunk
        elif provider == "groq":
            async for chunk in self._groq_stream(messages, model or settings.GROQ_MODEL, temperature, max_tokens):
                yield chunk
        elif provider == "openrouter":
            async for chunk in self._openrouter_stream(messages, model or settings.OPENROUTER_MODEL, temperature, max_tokens):
                yield chunk
        elif provider == "gemini":
            async for chunk in self._gemini_stream(messages, model or settings.GEMINI_MODEL, temperature, max_tokens):
                yield chunk
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def chat(
        self, messages: list[dict], model: str | None = None, temperature: float = 0.7, max_tokens: int | None = None
    ) -> str:
        full_response = ""
        async for chunk in self.chat_stream(messages, model, temperature, max_tokens):
            full_response += chunk
        return full_response

    async def get_available_models(self) -> list[dict]:
        models = []
        if self.provider == "ollama" or self.provider == "auto":
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
                    if resp.status_code == 200:
                        data = resp.json()
                        for m in data.get("models", []):
                            models.append({"id": m["name"], "provider": "ollama", "size": m.get("size", 0)})
            except Exception as e:
                logger.warning(f"Failed to fetch ollama models: {e}")
        models.append({"id": settings.GROQ_MODEL, "provider": "groq"})
        models.append({"id": settings.OPENROUTER_MODEL, "provider": "openrouter"})
        models.append({"id": settings.GEMINI_MODEL, "provider": "gemini"})
        return models

    async def _ollama_stream(self, messages: list[dict], model: str, temperature: float) -> AsyncGenerator[str, None]:
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        payload = {
            "model": model,
            "messages": full_messages,
            "stream": True,
            "options": {"temperature": temperature},
        }
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream("POST", f"{settings.OLLAMA_HOST}/api/chat", json=payload) as resp:
                    async for line in resp.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    yield data["message"]["content"]
                                if data.get("done"):
                                    break
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            yield f"\n[Error: LLM connection failed - {e}]"

    async def _groq_stream(self, messages: list[dict], model: str, temperature: float, max_tokens: int | None) -> AsyncGenerator[str, None]:
        if not settings.GROQ_API_KEY:
            yield "[Error: GROQ_API_KEY not configured]"
            return
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        payload = {
            "model": model,
            "messages": full_messages,
            "temperature": temperature,
            "stream": True,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream("POST", "https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers) as resp:
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"Groq stream error: {e}")
            yield f"\n[Error: Groq API failed - {e}]"

    async def _openrouter_stream(self, messages: list[dict], model: str, temperature: float, max_tokens: int | None) -> AsyncGenerator[str, None]:
        if not settings.OPENROUTER_API_KEY:
            yield "[Error: OPENROUTER_API_KEY not configured]"
            return
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        payload = {
            "model": model,
            "messages": full_messages,
            "temperature": temperature,
            "stream": True,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Jarvis OS",
        }
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream("POST", "https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers) as resp:
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"OpenRouter stream error: {e}")
            yield f"\n[Error: OpenRouter API failed - {e}]"

    async def _gemini_stream(self, messages: list[dict], model: str, temperature: float, max_tokens: int | None) -> AsyncGenerator[str, None]:
        if not settings.GEMINI_API_KEY:
            yield "[Error: GEMINI_API_KEY not configured]"
            return
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        gen_model = genai.GenerativeModel(model_name=model, system_instruction=self.system_prompt)
        try:
            history = []
            for msg in messages:
                if msg["role"] in ("user", "assistant"):
                    history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})
            chat = gen_model.start_chat(history=history)
            response = chat.send_message(
                messages[-1]["content"] if messages else "",
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens or 8192,
                ),
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Gemini stream error: {e}")
            yield f"\n[Error: Gemini API failed - {e}]"

    def _detect_provider_from_model(self, model: str) -> str:
        if "/" in model and not model.startswith("gemini"):
            return "openrouter"
        if model.startswith("gemini"):
            return "gemini"
        if model.startswith("mixtral") or model.startswith("llama") and "groq" not in model:
            return "groq"
        return self.provider


llm_service = LLMService()
