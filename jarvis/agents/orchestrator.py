from jarvis.utils.logger import JarvisLogger


class Orchestrator:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("agents.orchestrator")
        from jarvis.llm.router import get_llm_router
        self.llm = get_llm_router()
        self.agents = self._init_agents()

    def _init_agents(self):
        from jarvis.agents.planner import PlannerAgent
        from jarvis.agents.coder import CodingAgent
        from jarvis.agents.browser_agent import BrowserAgent
        from jarvis.agents.memory_agent import MemoryAgent
        from jarvis.agents.research import ResearchAgent
        from jarvis.agents.execution import ExecutionAgent
        return {
            "planner": PlannerAgent(),
            "coder": CodingAgent(),
            "browser": BrowserAgent(),
            "memory": MemoryAgent(),
            "research": ResearchAgent(),
            "execution": ExecutionAgent(),
        }

    async def delegate(self, task: str, agent_name: str | None = None) -> str:
        if agent_name and agent_name in self.agents:
            self.logger.info(f"Delegating to {agent_name}: {task[:80]}")
            return await self.agents[agent_name].run(task)

        agent = self._select_agent(task)
        self.logger.info(f"Auto-selected {agent.name}: {task[:80]}")
        return await agent.run(task)

    def _select_agent(self, task: str):
        task_lower = task.lower()
        if any(w in task_lower for w in ["plan", "organize", "strategy", "break down"]):
            return self.agents["planner"]
        elif any(w in task_lower for w in ["code", "write", "program", "script", "implement"]):
            return self.agents["coder"]
        elif any(w in task_lower for w in ["browser", "web page", "google", "website", "open url", "navigate", "web search"]):
            return self.agents["browser"]
        elif any(w in task_lower for w in ["remember", "memory", "recall", "store"]):
            return self.agents["memory"]
        elif any(w in task_lower for w in ["research", "investigate", "study", "search for", "find information"]):
            return self.agents["research"]
        elif any(w in task_lower for w in ["run", "execute", "shell", "command", "terminal"]):
            return self.agents["execution"]
        return self.agents["planner"]


_orchestrator: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator
