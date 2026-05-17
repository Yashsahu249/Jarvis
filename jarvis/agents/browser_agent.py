from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Browser Agent. You control web browsers to automate tasks.

Capabilities:
- Navigate to websites
- Search the web
- Extract information
- Interact with forms and buttons
- Take screenshots
- Fill in forms

Always specify the exact action and selector needed."""


class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__("browser", SYSTEM_PROMPT)

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)
        return await self.llm.generate(messages)
