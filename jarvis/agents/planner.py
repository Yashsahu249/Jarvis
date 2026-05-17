from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Planner Agent. Your role is to break down complex tasks into clear, actionable steps.

Rules:
1. Analyze the task thoroughly before planning
2. Identify dependencies between steps
3. Estimate complexity of each step
4. Suggest the right tools for each step
5. Consider risks and alternatives

Available tools: filesystem, shell, git, code, browser, python"""


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner", SYSTEM_PROMPT)

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)
        messages.append({
            "role": "user",
            "content": "Create a detailed step-by-step plan for this task."
        })
        return await self.llm.generate(messages)
