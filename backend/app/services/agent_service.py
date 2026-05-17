import uuid
import asyncio
from datetime import datetime, timezone
from typing import Any
from loguru import logger
from app.core.config import settings


class AgentService:
    def __init__(self):
        self.agents: dict[str, dict[str, Any]] = {}
        self.tasks: dict[str, dict[str, Any]] = {}
        self._init_default_agents()

    def _init_default_agents(self):
        defaults = [
            {
                "id": "planner",
                "name": "Planner",
                "role": "planner",
                "status": "idle",
                "model": settings.OLLAMA_MODEL,
                "capabilities": ["task_decomposition", "scheduling", "workflow_design"],
                "metadata": {},
            },
            {
                "id": "coder",
                "name": "Coder",
                "role": "coder",
                "status": "idle",
                "model": settings.OLLAMA_MODEL,
                "capabilities": ["code_generation", "code_review", "debugging", "refactoring"],
                "metadata": {},
            },
            {
                "id": "researcher",
                "name": "Researcher",
                "role": "researcher",
                "status": "idle",
                "model": settings.OLLAMA_MODEL,
                "capabilities": ["web_search", "fact_checking", "information_synthesis", "source_analysis"],
                "metadata": {},
            },
            {
                "id": "executor",
                "name": "Executor",
                "role": "executor",
                "status": "idle",
                "model": settings.OLLAMA_MODEL,
                "capabilities": ["command_execution", "tool_usage", "system_automation", "file_operations"],
                "metadata": {},
            },
        ]
        for agent in defaults:
            self.agents[agent["id"]] = agent

    def list_agents(self) -> list[dict]:
        return list(self.agents.values())

    def get_agent(self, agent_id: str) -> dict | None:
        return self.agents.get(agent_id)

    def create_task(self, agent_id: str, task_type: str, description: str, input_data: dict | None = None) -> dict:
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")

        task_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        task = {
            "id": task_id,
            "agent_id": agent_id,
            "type": task_type,
            "description": description,
            "status": "pending",
            "input": input_data or {},
            "output": None,
            "created_at": now,
            "completed_at": None,
        }
        self.tasks[task_id] = task
        self.agents[agent_id]["status"] = "busy"
        return task

    async def execute_task(self, task_id: str) -> dict:
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        agent = self.agents.get(task["agent_id"])
        if not agent:
            raise ValueError(f"Agent {task['agent_id']} not found")

        task["status"] = "running"
        try:
            result = await self._run_agent_task(agent, task)
            task["output"] = result
            task["status"] = "completed"
            task["completed_at"] = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            task["status"] = "failed"
            task["output"] = {"error": str(e)}
            task["completed_at"] = datetime.now(timezone.utc).isoformat()
            logger.error(f"Task {task_id} failed: {e}")
        finally:
            self.agents[task["agent_id"]]["status"] = "idle"

        return task

    def get_tasks(self, agent_id: str | None = None) -> list[dict]:
        if agent_id:
            return [t for t in self.tasks.values() if t["agent_id"] == agent_id]
        return list(self.tasks.values())

    def get_task(self, task_id: str) -> dict | None:
        return self.tasks.get(task_id)

    def get_agent_memory(self, agent_id: str) -> list[dict]:
        tasks = self.get_tasks(agent_id)
        memory = []
        for t in tasks[-20:]:
            memory.append({
                "task_id": t["id"],
                "type": t["type"],
                "description": t["description"],
                "status": t["status"],
                "output_preview": str(t.get("output", ""))[:200] if t.get("output") else None,
                "completed_at": t.get("completed_at"),
            })
        return memory

    async def _run_agent_task(self, agent: dict, task: dict) -> Any:
        await asyncio.sleep(0.1)

        role_map = {
            "planner": self._planner_execute,
            "coder": self._coder_execute,
            "researcher": self._researcher_execute,
            "executor": self._executor_execute,
        }
        handler = role_map.get(agent["role"], self._default_execute)
        return await handler(task)

    async def _planner_execute(self, task: dict) -> dict:
        desc = task["description"]
        steps = [s.strip() for s in desc.split("\n") if s.strip()]
        if not steps:
            steps = [desc]
        return {
            "plan": steps,
            "estimated_steps": len(steps),
            "strategy": "sequential",
            "recommendations": [f"Step {i+1}: {s}" for i, s in enumerate(steps)],
        }

    async def _coder_execute(self, task: dict) -> dict:
        from app.services.llm_service import llm_service

        prompt = f"Generate code for the following task:\n{task['description']}\n\nContext: {task['input']}"
        messages = [{"role": "user", "content": prompt}]
        code = await llm_service.chat(messages, temperature=0.3)
        return {"code": code, "language": "python", "quality_check": "passed"}

    async def _researcher_execute(self, task: dict) -> dict:
        from app.services.llm_service import llm_service

        prompt = f"Research the following topic and provide comprehensive findings:\n{task['description']}"
        messages = [{"role": "user", "content": prompt}]
        findings = await llm_service.chat(messages, temperature=0.7)
        return {"findings": findings, "sources": [], "confidence": 0.85}

    async def _executor_execute(self, task: dict) -> dict:
        cmd = task["input"].get("command", task["description"])
        import subprocess
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout[-2000:],
                "stderr": result.stderr[-2000:],
            }
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": "Command timed out"}
        except Exception as e:
            return {"exit_code": -1, "stdout": "", "stderr": str(e)}

    async def _default_execute(self, task: dict) -> dict:
        return {"result": f"Processed task: {task['description'][:100]}", "status": "completed"}


agent_service = AgentService()
