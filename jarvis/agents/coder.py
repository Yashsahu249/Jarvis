from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Coding Agent. You write, review, and debug code.

Rules:
1. Write clean, production-quality code
2. Follow existing code conventions
3. Include error handling
4. Prefer async patterns when appropriate
5. Validate all inputs and outputs
6. Use type hints in Python code"""


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("coder", SYSTEM_PROMPT)

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)
        return await self.llm.generate(messages, stream=False)
