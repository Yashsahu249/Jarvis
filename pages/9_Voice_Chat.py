import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Voice Chat - Jarvis", page_icon="", layout="wide")

from jarvis.voice.stt import SpeechToText
from jarvis.voice.tts import TextToSpeech
from jarvis.llm.router import get_llm_router
from jarvis.memory.conversation import get_conversation_manager
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT

stt = SpeechToText()
tts = TextToSpeech()
llm = get_llm_router()
cm = get_conversation_manager()

st.markdown("""
<style>
    .chat-msg {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #333;
    }
    .chat-msg.user { background: #1a2e2a; }
    .chat-msg.assistant { background: #1e1e1e; }
    .chat-role { font-size: 0.75rem; color: #00BFA5; font-weight: 600; margin-bottom: 0.3rem; }
    .chat-content { font-size: 0.95rem; line-height: 1.6; }
    .recording-box {
        background: #1e1e1e;
        border: 2px solid #333;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    .recording-box.active {
        border-color: #ff4444;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Voice Chat")
st.markdown("Talk to Jarvis using your microphone")

col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Status")
    status_placeholder = st.empty()
    status_placeholder.info("Ready")

    st.markdown("### TTS Engine")
    engine = st.radio("Voice output", ["Piper (offline)", "gTTS (online)"], index=0)
    st.markdown("### Settings")
    use_wake = st.checkbox("Wake word required", value=False, help='Say "Jarvis" before your command')
    st.markdown("---")
    st.markdown("### Conversation")
    if st.button(" Clear History", use_container_width=True):
        cm.clear()
        st.session_state.voice_messages = []
        st.rerun()

if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = []

with col1:
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.voice_messages:
            role_class = msg["role"]
            content = msg["content"]
            st.markdown(
                f'<div class="chat-msg {role_class}">'
                f'<div class="chat-role">{"" if role_class == "user" else " Jarvis"}</div>'
                f'<div class="chat-content">{content}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    audio_data = st.audio_input("Record your message", key="voice_input")

    if audio_data:
        audio_bytes = audio_data.getvalue()
        status_placeholder.warning("Transcribing...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            audio_path = f.name

        try:
            import numpy as np
            import soundfile as sf

            audio_array, sample_rate = sf.read(audio_path)
            result = stt.transcribe(audio_array, sample_rate)
            text = result.get("text", "").strip()

            os.unlink(audio_path)

            if not text:
                status_placeholder.error("Could not understand audio")
                st.rerun()

            lang = result.get("language", "en")
            lang_label = {"en": "English", "hi": "Hindi"}.get(lang, lang)
            status_placeholder.info(f"Transcribed ({lang_label}): {text}")

            if use_wake:
                from jarvis.voice.wake import WakeWordDetector
                wake = WakeWordDetector()
                if not wake.contains_wake_word(text):
                    status_placeholder.info("Wake word not detected — try again")
                    st.rerun()
                text = wake.strip_wake_word(text).strip()
                if not text:
                    status_placeholder.info("Only wake word detected")
                    st.rerun()

            st.session_state.voice_messages.append({"role": "user", "content": text})
            cm.add_user_message(text)

            with chat_container:
                st.markdown(
                    f'<div class="chat-msg user">'
                    f'<div class="chat-role"></div>'
                    f'<div class="chat-content">{text}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            status_placeholder.info(" Jarvis is thinking...")
            context = cm.build_context(SYSTEM_PROMPT)
            response = llm.generate_sync(context)

            st.session_state.voice_messages.append({"role": "assistant", "content": response})
            cm.add_assistant_message(response)

            with chat_container:
                display = response.replace("\n", "<br>")
                st.markdown(
                    f'<div class="chat-msg assistant">'
                    f'<div class="chat-role"> Jarvis</div>'
                    f'<div class="chat-content">{display}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            if engine == "Piper (offline)":
                status_placeholder.info(" Speaking...")
                tts.speak(response)
            else:
                status_placeholder.info(" Generating speech...")
                try:
                    from gtts import gTTS
                    import io

                    has_hindi = bool(__import__("re").search(r"[\u0900-\u097F]", response))
                    tts_obj = gTTS(text=response, lang="hi" if has_hindi else "en", slow=False)
                    mp3_bytes = io.BytesIO()
                    tts_obj.write_to_fp(mp3_bytes)
                    mp3_bytes.seek(0)
                    st.audio(mp3_bytes, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.warning(f"TTS error: {e}")

            status_placeholder.success("Done")

        except Exception as e:
            status_placeholder.error(f"Error: {e}")
            if os.path.exists(audio_path):
                os.unlink(audio_path)

        st.rerun()
