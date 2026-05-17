from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Execution Agent. You execute tasks using available tools.

Rules:
1. Only use safe commands automatically
2. Ask for confirmation on medium-risk operations
3. Block dangerous operations
4. Log all executions
5. Handle errors gracefully
6. Report results clearly"""


class ExecutionAgent(BaseAgent):
    def __init__(self):
        super().__init__("execution", SYSTEM_PROMPT)

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)
        return await self.llm.generate(messages)
