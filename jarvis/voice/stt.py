import numpy as np

from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class SpeechToText:
    def __init__(self):
        from faster_whisper import WhisperModel
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("voice.stt")
        self.logger.info(
            f"Loading Whisper model: {self.settings.STT_MODEL_SIZE}"
        )
        self.model = WhisperModel(
            self.settings.STT_MODEL_SIZE,
            compute_type="int8",
            device="cpu",
        )
        self.logger.info("Whisper model loaded")

    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> dict:
        segments, info = self.model.transcribe(
            audio_data,
            beam_size=5,
            vad_filter=True,
            language=None,
        )
        text = " ".join(segment.text for segment in segments)
        lang = info.language if info else "en"
        self.logger.debug(f"Transcribed: {len(text)} chars, lang={lang}")
        return {"text": text.strip(), "language": lang, "segments": list(segments)}

    def transcribe_file(self, filepath: str) -> dict:
        segments, info = self.model.transcribe(
            filepath,
            beam_size=5,
            vad_filter=True,
        )
        text = " ".join(segment.text for segment in segments)
        return {"text": text.strip(), "language": info.language if info else "en"}
