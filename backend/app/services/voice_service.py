import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator
from loguru import logger
from app.core.config import settings


class VoiceService:
    def __init__(self):
        self.model = None
        self.audio_dir = Path(settings.MEMORY_DB_PATH).parent / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    async def transcribe(self, file_path: str, language: str | None = None, model_size: str | None = None) -> dict:
        size = model_size or settings.STT_MODEL_SIZE
        try:
            from faster_whisper import WhisperModel

            if self.model is None:
                self.model = WhisperModel(size, device="cpu", compute_type="int8")

            segments, info = await self._run_async(self.model.transcribe, file_path, language=language, beam_size=5)

            text_parts = []
            seg_list = []
            for seg in segments:
                text_parts.append(seg.text.strip())
                seg_list.append({
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip(),
                })

            return {
                "text": " ".join(text_parts),
                "segments": seg_list,
                "duration": info.duration if info else None,
                "language": info.language if info else None,
            }
        except ImportError:
            logger.warning("faster-whisper not installed, using fallback")
            return await self._transcribe_fallback(file_path)
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise

    async def synthesize(self, text: str, voice: str | None = None, speed: float = 1.0) -> dict:
        output_path = self.audio_dir / f"tts_{abs(hash(text))}.wav"
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=voice or "en", slow=speed < 1.0)
            tts.save(str(output_path))
            duration = len(text.split()) * 0.3 / speed
            return {"audio_path": str(output_path), "duration": duration}
        except ImportError:
            logger.warning("gTTS not installed, creating fallback")
            output_path.write_text(text)
            return {"audio_path": str(output_path), "duration": 0.0}
        except Exception as e:
            logger.error(f"TTS synthesis error: {e}")
            raise

    async def stream_audio(self, text: str) -> AsyncGenerator[bytes, None]:
        output_path = self.audio_dir / f"stream_{abs(hash(text))}.wav"
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en")
            tts.save(str(output_path))
            with open(output_path, "rb") as f:
                chunk = f.read(4096)
                while chunk:
                    yield chunk
                    chunk = f.read(4096)
            os.unlink(output_path)
        except Exception as e:
            logger.error(f"Audio stream error: {e}")
            yield b""

    async def _run_async(self, func, *args, **kwargs):
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, lambda: func(*args, **kwargs))

    async def _transcribe_fallback(self, file_path: str) -> dict:
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return {"text": text, "segments": None, "duration": None, "language": "en"}
        except ImportError:
            return {"text": "[Transcription unavailable]", "segments": None, "duration": None, "language": None}
        except Exception as e:
            return {"text": f"[Transcription error: {e}]", "segments": None, "duration": None, "language": None}


voice_service = VoiceService()
