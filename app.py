import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Jarvis Workspace",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

from pathlib import Path

from jarvis.config.settings import get_settings
from jarvis.llm.router import get_llm_router
from jarvis.tools.registry import get_tool_registry
from jarvis.utils.logger import JarvisLogger

logger = JarvisLogger.get_logger("app")

settings = get_settings()
llm = get_llm_router()
tools = get_tool_registry()

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; margin-bottom: 0; }
    .sub-title { color: #00BFA5; font-size: 0.9rem; margin-bottom: 2rem; }
    .stat-card {
        background: #1E1E1E;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #333;
    }
    .stat-value { font-size: 2rem; font-weight: 700; color: #00BFA5; }
    .stat-label { font-size: 0.8rem; color: #888; }
    .quick-action {
        background: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .quick-action:hover {
        border-color: #00BFA5;
        background: #252525;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Jarvis Workspace</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Local AI Operating System — Intelligent Work Environment</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{llm.active_provider}</div>
        <div class="stat-label">Active Provider</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{llm.get_provider().model_name}</div>
        <div class="stat-label">Active Model</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(tools.list_tools())}</div>
        <div class="stat-label">Available Tools</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">v1.0</div>
        <div class="stat-label">System Version</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Quick Actions")
pages_dir = Path(__file__).parent / "pages"

quick_actions = [
    (" Chat", "Start a conversation", "1_Chat"),
    (" Workspace", "Browse & edit files", "2_Workspace"),
    (" Terminal", "Run shell commands", "3_Terminal"),
    (" Browser", "Web automation", "4_Browser"),
]

qa_cols = st.columns(len(quick_actions))
for i, (icon, label, page_name) in enumerate(quick_actions):
    with qa_cols[i]:
        page_path = pages_dir / f"{page_name}.py"
        if page_path.exists():
            st.page_link(
                str(page_path),
                label=f"{icon}  {label}",
                use_container_width=True,
            )

st.markdown("### Tool Overview")
tool_cols = st.columns(3)
all_tools = tools.list_tools()
for i, tool in enumerate(all_tools):
    with tool_cols[i % 3]:
        st.markdown(f"""
        <div class="stat-card" style="margin-bottom: 0.5rem;">
            <div style="font-weight: 600; color: #00BFA5;">{tool['name']}</div>
            <div style="font-size: 0.8rem; color: #888;">{tool['description'][:60]}...</div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown("## Jarvis")
st.sidebar.markdown("---")

st.sidebar.page_link("app.py", label=" Dashboard", use_container_width=True)
st.sidebar.page_link("pages/1_Chat.py", label=" Chat", use_container_width=True)
st.sidebar.page_link("pages/9_Voice_Chat.py", label=" Voice Chat", use_container_width=True)
st.sidebar.page_link("pages/2_Workspace.py", label=" Workspace", use_container_width=True)
st.sidebar.page_link("pages/3_Terminal.py", label=" Terminal", use_container_width=True)
st.sidebar.page_link("pages/4_Browser.py", label=" Browser", use_container_width=True)
st.sidebar.page_link("pages/5_Memory.py", label=" Memory", use_container_width=True)
st.sidebar.page_link("pages/6_Agents.py", label=" Agents", use_container_width=True)
st.sidebar.page_link("pages/8_Python_Lab.py", label=" Python Lab", use_container_width=True)
st.sidebar.page_link("pages/7_Settings.py", label=" Settings", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Provider:** {llm.active_provider}")
st.sidebar.markdown(f"**Model:** {llm.get_provider().model_name}")
st.sidebar.markdown("---")

st.sidebar.markdown("### System")
st.sidebar.markdown(f"Debug: {'ON' if settings.DEBUG else 'OFF'}")
st.sidebar.markdown(f"Sandbox: {'ON' if settings.SANDBOX_ENABLED else 'OFF'}")
st.sidebar.markdown(f"Auto-execute: {'ON' if settings.AUTO_EXECUTE_SAFE else 'OFF'}")
st.sidebar.markdown("---")
st.sidebar.markdown("v1.0.0")
