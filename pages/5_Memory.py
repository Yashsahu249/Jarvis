import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Memory - Jarvis", page_icon="", layout="wide")

from jarvis.memory.store import get_memory_store
from jarvis.memory.conversation import get_conversation_manager

store = get_memory_store()
cm = get_conversation_manager()

st.markdown("""
<style>
    .mem-card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .mem-key { color: #00BFA5; font-weight: 600; font-size: 0.9rem; }
    .mem-value { color: #ccc; font-size: 0.85rem; margin-top: 0.3rem; }
    .mem-meta { color: #666; font-size: 0.75rem; margin-top: 0.3rem; }
    .conv-msg {
        padding: 0.6rem 1rem;
        border-left: 3px solid #333;
        margin-bottom: 0.3rem;
        font-size: 0.85rem;
    }
    .conv-msg.user { border-left-color: #00BFA5; }
    .conv-msg.assistant { border-left-color: #888; }
    .conv-role { font-size: 0.75rem; font-weight: 600; color: #666; }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Memory Explorer")
st.markdown("Conversation history, stored memories, and system data")

tab1, tab2, tab3 = st.tabs([" Stored Memories", " Conversation History", " Database Info"])

with tab1:
    st.markdown("### Saved Memories")

    col1, col2 = st.columns([2, 1])
    with col1:
        search_q = st.text_input("Search memories", placeholder="Search by key or value...")
    with col2:
        category_filter = st.selectbox("Category", ["All", "general", "preferences", "project", "user"])

    cat = None if category_filter == "All" else category_filter
    if search_q:
        results = store.search_memories(search_q, category=cat)
    else:
        results = store.search_memories("", category=cat)

    if results:
        st.markdown(f"**{len(results)} memories found**")
        for mem in results:
            st.markdown(
                f'<div class="mem-card">'
                f'<div class="mem-key">{mem["key"]}</div>'
                f'<div class="mem-value">{mem["value"][:200]}</div>'
                f'<div class="mem-meta">{mem["category"]} · {mem["timestamp"][:19]}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No memories found. Memories are created during conversations.")

    st.markdown("---")
    st.markdown("### Add Memory Manually")
    with st.form("add_memory"):
        mkey = st.text_input("Key")
        mval = st.text_area("Value")
        mcat = st.selectbox("Category", ["general", "preferences", "project", "user"])
        if st.form_submit_button("Save Memory"):
            if mkey and mval:
                store.save_memory(mkey, mval, mcat)
                st.success(f"Saved: {mkey}")
                st.rerun()

with tab2:
    st.markdown(f"### Current Session: `{cm.session_id[:8]}...`")

    history = cm.get_history()
    if history:
        st.markdown(f"**{len(history)} messages** in current session")
        for msg in history[-20:]:
            role = msg["role"]
            content = msg["content"][:300]
            st.markdown(
                f'<div class="conv-msg {role}">'
                f'<div class="conv-role">{role.upper()}</div>'
                f'{content}'
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No conversation history in current session")

    if st.button(" Clear Session History", type="secondary"):
        cm.clear()
        st.success("History cleared")
        st.rerun()

with tab3:
    st.markdown("### Database")
    st.markdown(f"**DB Path:** `{store.db_path}`")
    st.markdown(f"**DB Exists:** `{store.db_path.exists()}`")

    try:
        size = store.db_path.stat().st_size
        st.markdown(f"**DB Size:** {size:,} bytes ({size/1024:.1f} KB)")
    except Exception:
        st.markdown("**DB Size:** N/A")

    st.markdown("---")
    st.markdown("### Summary")
    summary = store.get_latest_summary(cm.session_id)
    if summary:
        st.markdown(f"**Latest Summary:** {summary}")
    else:
        st.info("No summary available yet")
