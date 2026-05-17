from jarvis.llm.router import get_llm_router
from jarvis.utils.logger import JarvisLogger
from jarvis.utils.helpers import detect_language


class StrategicThinker:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("reasoning.thinker")
        self.llm = get_llm_router()

    async def analyze(self, user_input: str, context: list[dict]) -> str:
        lang = detect_language(user_input)
        lang_instruction = {
            "hindi": "जवाब हिंदी में दो।",
            "hinglish": "Hinglish mein jawab do.",
            "english": "Respond in English.",
        }.get(lang, "Respond in English.")

        thinking_prompt = (
            "You are Jarvis, a strategic thinking AI assistant. "
            "Analyze the user's input carefully. "
            f"{lang_instruction}\n\n"
            "Before responding:\n"
            "1. Identify any logical flaws or contradictions\n"
            "2. Consider if the user's request is optimal\n"
            "3. Think about long-term consequences\n"
            "4. Suggest better approaches when relevant\n"
            "5. Teach useful concepts naturally\n\n"
            "User: {input}"
        ).format(input=user_input)

        messages = context + [
            {"role": "user", "content": thinking_prompt}
        ]

        response = await self.llm.generate(messages)
        return response
