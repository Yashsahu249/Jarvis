import json
import re
from typing import Any
from loguru import logger
from app.services.llm_service import llm_service
from app.core.config import settings


class PlannerAgent:
    def __init__(self):
        self.id = "planner"
        self.name = "Planner Agent"
        self.role = "planner"

    async def decompose(self, task: str, context: dict[str, Any] | None = None) -> list[dict]:
        prompt = (
            "You are a task planning agent. Break down the following task into clear, actionable steps.\n\n"
            f"Task: {task}\n\n"
            "Respond with a JSON array of steps. Each step must have: 'id' (number), 'description' (string), "
            "'agent' (one of: planner, coder, researcher, executor), 'depends_on' (list of step ids this depends on), "
            "'priority' (high/medium/low).\n"
            "Only respond with the JSON array, no other text."
        )

        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)

        steps = self._parse_steps(response)
        return steps

    async def refine_plan(self, plan: list[dict], feedback: str) -> list[dict]:
        prompt = (
            "Refine the following plan based on feedback.\n\n"
            f"Current plan: {json.dumps(plan, indent=2)}\n\n"
            f"Feedback: {feedback}\n\n"
            "Respond with the updated JSON array of steps."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)
        return self._parse_steps(response)

    async def estimate_effort(self, task: str) -> dict:
        prompt = (
            "Estimate the effort required for the following task.\n\n"
            f"Task: {task}\n\n"
            "Respond with a JSON object containing: 'complexity' (simple/medium/complex), "
            "'estimated_minutes' (number), 'required_agents' (list of agent roles), "
            "'risk_level' (low/medium/high).\n"
            "Only respond with the JSON object."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)

        try:
            cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"complexity": "unknown", "estimated_minutes": 0, "required_agents": [], "risk_level": "unknown"}

    def _parse_steps(self, response: str) -> list[dict]:
        cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
        try:
            steps = json.loads(cleaned)
            if isinstance(steps, dict) and "steps" in steps:
                steps = steps["steps"]
            return steps if isinstance(steps, list) else []
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse plan steps from: {response[:100]}")
            return [{"id": 1, "description": task.strip(), "agent": "executor", "depends_on": [], "priority": "medium"}
                    for task in re.split(r'\n\d+[.)]\s*', response) if task.strip()]


planner_agent = PlannerAgent()
