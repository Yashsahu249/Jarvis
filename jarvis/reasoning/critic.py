from jarvis.llm.router import get_llm_router
from jarvis.utils.logger import JarvisLogger


class SelfCritic:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("reasoning.critic")
        self.llm = get_llm_router()

    async def critique_response(self, user_input: str, draft_response: str) -> str:
        crit_prompt = (
            "Critique the following draft response for:\n"
            "1. Logical consistency\n"
            "2. Factual accuracy\n"
            "3. Clarity and usefulness\n"
            "4. Tone appropriateness\n\n"
            f"User input: {user_input}\n\n"
            f"Draft response: {draft_response}\n\n"
            "Provide a brief critique and improved version if needed."
        )

        try:
            critique = await self.llm.generate(
                [{"role": "user", "content": crit_prompt}]
            )
            return critique
        except Exception as e:
            self.logger.error(f"Critique failed: {e}")
            return draft_response
