import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import sounddevice as sd
import numpy as np

from jarvis.llm.router import get_llm_router
from jarvis.memory.conversation import get_conversation_manager
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT
from jarvis.voice.stt import SpeechToText
from jarvis.voice.tts import TextToSpeech
from jarvis.voice.wake import WakeWordDetector
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class VoiceUI:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("ui.voice")
        self.settings = get_settings()
        self.llm = get_llm_router()
        self.cm = get_conversation_manager()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.wake = WakeWordDetector()
        self.running = True
        self.sample_rate = 16000
        self.device = self.settings.AUDIO_DEVICE

    def record_audio(self, duration: int = 5) -> np.ndarray:
        self.logger.info(f"Listening for {duration}s...")
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            device=self.device,
        )
        sd.wait()
        return recording.flatten().astype(np.float32) / 32768.0

    def run(self):
        print("Jarvis Voice Mode. Say 'jarvis' to activate. Ctrl+C to exit.\n")

        while self.running:
            try:
                audio = self.record_audio(duration=self.settings.LISTEN_TIMEOUT)
                result = self.stt.transcribe(audio, self.sample_rate)
                text = result.get("text", "").strip()

                if not text:
                    continue

                if not self.wake.contains_wake_word(text):
                    continue

                text = self.wake.strip_wake_word(text)
                if not text:
                    continue

                print(f"You: {text}")

                self.cm.add_user_message(text)
                context = self.cm.build_context(SYSTEM_PROMPT)

                print("Jarvis: ", end="", flush=True)
                full_response = self.llm.generate_sync(context)
                print(full_response)

                self.cm.add_assistant_message(full_response)
                self.tts.speak(full_response)

            except KeyboardInterrupt:
                print("\nExiting voice mode.")
                break
            except Exception as e:
                self.logger.error(f"Voice loop error: {e}")
                print(f"\nError: {e}")


def main():
    ui = VoiceUI()
    ui.run()


if __name__ == "__main__":
    main()
