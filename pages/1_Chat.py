import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Chat - Jarvis", page_icon="", layout="wide")

from jarvis.llm.router import get_llm_router
from jarvis.memory.conversation import get_conversation_manager
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT
from jarvis.tools.registry import get_tool_registry

llm = get_llm_router()
cm = get_conversation_manager()
tools = get_tool_registry()

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
    .stTextInput input { font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Chat with Jarvis")
st.markdown("Multilingual · Strategic thinking · Tool-enabled")

col1, col2 = st.columns([4, 1])

with col2:
    st.markdown("### Info")
    st.markdown(f"**Session:** `{cm.session_id[:8]}...`")
    st.markdown(f"**Provider:** {llm.active_provider}")
    st.markdown(f"**Model:** {llm.get_provider().model_name}")
    st.markdown("### Tools")
    for t in tools.list_tools():
        st.markdown(f"- {t['name']}")
    if st.button(" Clear History", use_container_width=True):
        cm.clear()
        st.session_state.messages = []
        st.rerun()

with col1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            role_class = msg["role"]
            st.markdown(
                f'<div class="chat-msg {role_class}">'
                f'<div class="chat-role">{"" if role_class == "user" else " Jarvis"}</div>'
                f'<div class="chat-content">{msg["content"]}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    if prompt := st.chat_input("Type your message...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        cm.add_user_message(prompt)

        with chat_container:
            st.markdown(
                f'<div class="chat-msg user">'
                f'<div class="chat-role"></div>'
                f'<div class="chat-content">{prompt}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

        with chat_container:
            loading = st.empty()
            loading.info(" Jarvis is thinking...")
            full_response = ""
            context = cm.build_context(SYSTEM_PROMPT)

            try:
                full_response = llm.generate_sync(context)
            except Exception as e:
                full_response = f"Error: {e}"

            loading.empty()
            display = full_response.replace("\n", "<br>")
            st.markdown(
                f'<div class="chat-msg assistant">'
                f'<div class="chat-role"> Jarvis</div>'
                f'<div class="chat-content">{display}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
            cm.add_assistant_message(full_response)
