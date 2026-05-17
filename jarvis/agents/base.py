from abc import ABC, abstractmethod
from typing import AsyncGenerator

from jarvis.utils.logger import JarvisLogger


class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.logger = JarvisLogger.get_logger(f"agents.{name}")
        from jarvis.llm.router import get_llm_router
        from jarvis.tools.registry import get_tool_registry
        self.llm = get_llm_router()
        self.tools = get_tool_registry()

    @abstractmethod
    async def run(
        self, task: str, context: list[dict] | None = None
    ) -> str | AsyncGenerator[str, None]:
        ...

    def build_messages(
        self, task: str, context: list[dict] | None = None
    ) -> list[dict]:
        messages = [{"role": "system", "content": self.system_prompt}]
        if context:
            messages.extend(context) if isinstance(context, list) else None
        messages.append({"role": "user", "content": task})
        return messages

    def get_tool(self, name: str):
        return self.tools.get(name)
