from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Research Agent. You conduct thorough research on any topic.

Research process:
1. Search for relevant information
2. Verify sources and facts
3. Synthesize findings
4. Present balanced analysis
5. Cite sources when possible

Be thorough but concise. Focus on actionable insights."""


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research", SYSTEM_PROMPT)

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)
        return await self.llm.generate(messages)
