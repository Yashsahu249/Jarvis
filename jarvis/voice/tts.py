import os
import re
import time
import tempfile
from pathlib import Path

from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class TextToSpeech:
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("voice.tts")
        self._piper_voice = None
        self._piper_voice_hi = None
        self._current_model = None
        self._gtts = None
        self._init_engines()

    def _init_engines(self):
        try:
            import piper

            self._piper = piper
            self._apply_onnx_patch()

            en_path = self.settings.TTS_ENGLISH_MODEL
            hi_path = self.settings.TTS_HINDI_MODEL
            if Path(en_path).exists():
                self._piper_voice = piper.PiperVoice.load(en_path)
                self.logger.info(f"Piper EN voice loaded: {en_path}")
            if Path(hi_path).exists():
                self._piper_voice_hi = piper.PiperVoice.load(hi_path)
                self.logger.info(f"Piper HI voice loaded: {hi_path}")
            if not self._piper_voice and not self._piper_voice_hi:
                self.logger.warning("No Piper voice models found")
        except Exception as e:
            self.logger.warning(f"Piper not available: {e}")

    def _apply_onnx_patch(self):
        import piper.voice as pv
        import numpy as np

        original = pv.PiperVoice.phoneme_ids_to_audio

        if getattr(original, "_jarvis_patched", False):
            return

        def patched(self, phoneme_ids, syn_config=None, include_alignments=False):
            try:
                return original(self, phoneme_ids, syn_config, include_alignments)
            except Exception as e:
                err = str(e)
                if "tensor(double)" in err and "tensor(float)" in err:
                    if syn_config is None:
                        syn_config = self._piper.SynthesisConfig(
                            noise_scale=0.667, length_scale=1.0, noise_w_scale=0.8,
                        )
                    sid = syn_config.speaker_id
                    ns = syn_config.noise_scale or self.config.noise_scale
                    ls = syn_config.length_scale or self.config.length_scale
                    nws = syn_config.noise_w_scale or self.config.noise_w_scale

                    pids = np.expand_dims(np.array(phoneme_ids, dtype=np.int64), 0)
                    pids_len = np.array([pids.shape[1]], dtype=np.int64)
                    scales = np.array([ns, ls, nws], dtype=np.float32)

                    args = {"input": pids, "input_lengths": pids_len, "scales": scales}
                    if self.config.num_speakers > 1:
                        args["sid"] = np.array([sid or 0], dtype=np.int64)

                    result = self.session.run(None, args)
                    audio = result[0].squeeze()
                    if not include_alignments:
                        return audio
                    if len(result) == 1:
                        return audio, None
                    return audio, (result[1].squeeze() * self.config.hop_length).astype(np.int64)
                raise

        patched._jarvis_patched = True
        pv.PiperVoice.phoneme_ids_to_audio = patched
        self.logger.debug("ONNX double/float patch applied")

        try:
            from gtts import gTTS

            self._gtts = gTTS
            self.logger.info("gTTS fallback loaded")
        except Exception as e:
            self.logger.warning(f"gTTS not available: {e}")

        if not self._piper_voice and not self._piper_voice_hi and not self._gtts:
            self.logger.error("No TTS engine available")

    def _get_voice(self, text: str):
        has_hindi = bool(re.search(r"[\u0900-\u097F]", text))
        if has_hindi and self._piper_voice_hi:
            return self._piper_voice_hi
        return self._piper_voice

    def speak(self, text: str):
        if not text.strip():
            return
        text = re.sub(r"[^\u0900-\u097Fa-zA-Z0-9\s\.\,\!\?\-\:\;]", "", text)

        voice = self._get_voice(text)

        if voice:
            self._speak_piper(text, voice)
        elif self._gtts:
            self._speak_gtts(text)

    def _speak_piper(self, text: str, voice):
        output_file = os.path.join(tempfile.gettempdir(), "jarvis_output.wav")

        try:
            import numpy as np
            import wave

            synth_config = self._piper.SynthesisConfig(
                noise_scale=0.667,
                length_scale=1.0,
                noise_w_scale=0.8,
            )
            audio_chunks = list(voice.synthesize(text, synth_config))

            if not audio_chunks:
                self.logger.warning("No audio generated")
                return

            audio_bytes = b"".join(c.audio_int16_bytes for c in audio_chunks)
            sample_rate = audio_chunks[0].sample_rate or 22050

            with wave.open(output_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_bytes)

            import pygame

            try:
                pygame.mixer.quit()
                pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
            finally:
                try:
                    pygame.mixer.quit()
                except Exception:
                    pass

            self.logger.info("Piper playback complete")

        except Exception as e:
            self.logger.error(f"Piper playback error: {e}")
            if self._gtts:
                self.logger.info("Falling back to gTTS")
                self._speak_gtts(text)

    def _speak_gtts(self, text: str):
        try:
            has_hindi = bool(re.search(r"[\u0900-\u097F]", text))
            tts = self._gtts(text=text, lang="hi" if has_hindi else "en", slow=False)
            output_file = os.path.join(tempfile.gettempdir(), "jarvis_output.mp3")
            tts.save(output_file)

            import pygame

            try:
                pygame.mixer.quit()
                pygame.mixer.init()
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
            finally:
                try:
                    pygame.mixer.quit()
                except Exception:
                    pass

        except Exception as e:
            self.logger.error(f"gTTS error: {e}")
