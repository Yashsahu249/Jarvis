import numpy as np
from jarvis.utils.logger import JarvisLogger


class VoiceActivityDetector:
    def __init__(self, threshold: float = 0.02, min_speech_frames: int = 3):
        self.threshold = threshold
        self.min_speech_frames = min_speech_frames
        self.logger = JarvisLogger.get_logger("voice.vad")

    def is_speech(self, audio_frame: np.ndarray) -> bool:
        energy = np.mean(np.abs(audio_frame))
        return energy > self.threshold

    def detect_speech_segments(
        self, audio: np.ndarray, sample_rate: int = 16000, frame_ms: int = 30
    ) -> list[tuple[int, int]]:
        frame_size = int(sample_rate * frame_ms / 1000)
        speech_frames = 0
        segments = []
        start_sample = None

        for i in range(0, len(audio), frame_size):
            frame = audio[i : i + frame_size]
            if self.is_speech(frame):
                if start_sample is None:
                    start_sample = i
                speech_frames += 1
            else:
                if start_sample is not None and speech_frames >= self.min_speech_frames:
                    segments.append((start_sample, i))
                start_sample = None
                speech_frames = 0

        if start_sample is not None and speech_frames >= self.min_speech_frames:
            segments.append((start_sample, len(audio)))

        return segments
