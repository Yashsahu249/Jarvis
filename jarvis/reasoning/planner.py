import json
from jarvis.llm.router import get_llm_router
from jarvis.utils.logger import JarvisLogger


class ReasoningPlanner:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("reasoning.planner")
        self.llm = get_llm_router()

    async def create_plan(self, task: str, context: str = "") -> list[dict]:
        plan_prompt = (
            "Break this task into a sequence of concrete steps.\n"
            "Return as JSON array: [{\"step\": 1, \"action\": \"...\", \"tool\": \"...\"}]\n\n"
            f"Task: {task}\n"
            f"Context: {context}\n"
        )

        try:
            response = await self.llm.generate(
                [{"role": "user", "content": plan_prompt}]
            )
            cleaned = response.strip().removeprefix("```json").removesuffix("```").strip()
            plan = json.loads(cleaned)
            return plan if isinstance(plan, list) else []
        except (json.JSONDecodeError, Exception) as e:
            self.logger.error(f"Plan creation failed: {e}")
            return [{"step": 1, "action": task, "tool": "llm"}]
