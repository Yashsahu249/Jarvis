import re
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class WakeWordDetector:
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("voice.wake")
        self.wake_word = self.settings.WAKE_WORD.lower()
        self.pattern = re.compile(rf"\b{re.escape(self.wake_word)}\b", re.IGNORECASE)

    def contains_wake_word(self, text: str) -> bool:
        return bool(self.pattern.search(text))

    def strip_wake_word(self, text: str) -> str:
        return self.pattern.sub("", text)
