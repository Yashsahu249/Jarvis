from jarvis.agents.base import BaseAgent


SYSTEM_PROMPT = """You are Jarvis Memory Agent. You manage conversation memory and recall.

Responsibilities:
1. Remember important information from conversations
2. Recall relevant past context
3. Identify patterns in user behavior
4. Store and retrieve user preferences
5. Summarize conversations for context preservation"""


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__("memory", SYSTEM_PROMPT)
        from jarvis.memory.store import get_memory_store
        from jarvis.memory.conversation import get_conversation_manager
        self.store = get_memory_store()
        self.conversation = get_conversation_manager()

    async def run(self, task: str, context: list[dict] | None = None):
        messages = self.build_messages(task, context)

        relevant = self.store.search_memories(task)
        if relevant:
            mem_context = "\n".join(
                f"- {m['key']}: {m['value'][:200]}"
                for m in relevant[:5]
            )
            messages.append({
                "role": "system",
                "content": f"Relevant memories:\n{mem_context}"
            })

        return await self.llm.generate(messages)
