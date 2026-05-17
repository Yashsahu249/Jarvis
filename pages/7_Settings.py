import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Settings - Jarvis", page_icon="", layout="wide")

from jarvis.config.settings import get_settings
from jarvis.config.providers import get_available_providers, get_active_provider
from jarvis.llm.router import get_llm_router
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT
from jarvis.memory.store import get_memory_store
from jarvis.memory.export import get_storage_stats
from jarvis.memory.conversation import get_conversation_manager
from jarvis.tools.registry import get_tool_registry
from jarvis.agents.orchestrator import get_orchestrator

settings = get_settings()
llm = get_llm_router()
store = get_memory_store()
cm = get_conversation_manager()
tools = get_tool_registry()
orch = get_orchestrator()

providers = get_available_providers()
active_provider = get_active_provider()

st.markdown("""
<style>
    .card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
    }
    .card h3 { margin-top: 0; font-size: 0.95rem; color: #ccc; }
    .card h4 { margin: 0 0 0.5rem 0; font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
    .label { color: #888; font-size: 0.75rem; }
    .value { color: #e0e0e0; font-weight: 600; font-family: monospace; font-size: 0.85rem; }
    .badge-on { background: #00BFA5; color: #000; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; }
    .badge-off { background: #ff6b6b; color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; }
    .badge-warn { background: #ffd93d; color: #000; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; }
    .badge-idle { background: #555; color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700; }
    .provider-card { background: #1e1e1e; border: 1px solid #333; border-radius: 10px; padding: 1rem; margin-bottom: 0.5rem; }
    .provider-card.active { border-color: #00BFA5; background: #1a2a2a; }
    .stat-row { display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid #2a2a2a; }
    .metric-box { background: #252525; border-radius: 8px; padding: 1rem; text-align: center; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #00BFA5; }
    .metric-label { font-size: 0.7rem; color: #888; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Settings")
st.markdown("System configuration, health & status")

system_tab, providers_tab, tools_tab, memory_tab, about_tab = st.tabs([
    " System",
    " Providers",
    " Agents & Tools",
    " Memory",
    " About",
])

with system_tab:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{active_provider.capitalize()}</div><div class="metric-label">Active Provider</div></div>""", unsafe_allow_html=True)
    with col2:
        online_count = sum(providers.values())
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{online_count}/4</div><div class="metric-label">Providers Online</div></div>""", unsafe_allow_html=True)
    with col3:
        agent_count = len(orch.agents)
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{agent_count}</div><div class="metric-label">Active Agents</div></div>""", unsafe_allow_html=True)
    with col4:
        tool_count = len(tools.list_tools())
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{tool_count}</div><div class="metric-label">Registered Tools</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### General")
    items = [
        ("Host", settings.HOST),
        ("Port", str(settings.PORT)),
        ("Debug Mode", str(settings.DEBUG)),
        ("Data Directory", settings.DATA_DIR),
        ("Repo Directory", settings.REPO_DIR),
    ]
    for label, value in items:
        st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### LLM Configuration")
    items = [
        ("Provider", settings.LLM_PROVIDER),
        ("Ollama Model", settings.OLLAMA_MODEL),
        ("Ollama Fallback", settings.OLLAMA_FALLBACK_MODEL),
        ("Ollama Host", settings.OLLAMA_HOST),
        ("OpenRouter Model", settings.OPENROUTER_MODEL),
        ("Groq Model", settings.GROQ_MODEL),
        ("Gemini Model", settings.GEMINI_MODEL),
        ("Tavily API Key", f"{'Yes' if settings.TAVILY_API_KEY else 'No'}"),
    ]
    for label, value in items:
        st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Voice")
        items = [
            ("STT Model", settings.STT_MODEL_SIZE),
            ("Wake Word", settings.WAKE_WORD),
            ("Listen Timeout", f"{settings.LISTEN_TIMEOUT}s"),
            ("English TTS", Path(settings.TTS_ENGLISH_MODEL).name),
            ("Hindi TTS", Path(settings.TTS_HINDI_MODEL).name),
            ("Audio Device", str(settings.AUDIO_DEVICE)),
        ]
        for label, value in items:
            st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Browser")
        items = [
            ("Headless Mode", str(settings.BROWSER_HEADLESS)),
            ("Visible Mode", str(settings.BROWSER_VISIBLE)),
        ]
        for label, value in items:
            st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Safety")
        items = [
            ("Auto-execute Safe", str(settings.AUTO_EXECUTE_SAFE)),
            ("Require Confirmation", str(settings.REQUIRE_CONFIRMATION)),
            ("Sandbox Enabled", str(settings.SANDBOX_ENABLED)),
        ]
        for label, value in items:
            st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Memory")
    items = [
        ("Database", str(store.db_path)),
        ("DB Exists", str(store.db_path.exists())),
        ("Max History", str(settings.MEMORY_MAX_HISTORY)),
        ("Summarization Enabled", str(settings.MEMORY_ENABLE_SUMMARIZATION)),
    ]
    for label, value in items:
        st.markdown(f"""<div class="stat-row"><span class="label">{label}</span><span class="value">{value}</span></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with providers_tab:
    st.markdown("### Provider Status")
    st.markdown("Real-time availability of all LLM providers")

    for name in ["ollama", "groq", "openrouter", "gemini"]:
        available = providers.get(name, False)
        is_active = name == active_provider
        badge_class = "badge-on" if available else "badge-off"
        badge_text = "ONLINE" if available else "OFFLINE"
        border = "active" if is_active else ""

        model = llm.providers[name].model_name if name in llm.providers else "—"

        st.markdown(f"""<div class="provider-card {border}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{name.capitalize()}</strong>
                    {" <span style='color:#00BFA5;font-size:0.8rem;'>[ACTIVE]</span>" if is_active else ""}
                </div>
                <span class="{badge_class}">{badge_text}</span>
            </div>
            <div class="stat-row"><span class="label">Model</span><span class="value">{model}</span></div>
            <div class="stat-row"><span class="label">API Key</span><span class="value">{' Set' if available else ' Not Set'}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Fallback Chain")
    fallback_order = ["ollama", "groq", "openrouter", "gemini"]
    chain = " → ".join([f"{p.upper()}" for p in fallback_order])
    st.markdown(f"<div style='font-family:monospace;color:#00BFA5;'>{chain}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='label'>Active link: <span class='value'>{active_provider}</span></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### API Keys (Masked)")
    keys = {
        "OpenRouter": settings.OPENROUTER_API_KEY,
        "Groq": settings.GROQ_API_KEY,
        "Gemini": settings.GEMINI_API_KEY,
        "Tavily": settings.TAVILY_API_KEY,
    }
    for name, key in keys.items():
        if key:
            masked = key[:12] + "..." + key[-4:]
            st.markdown(f"""<div class="stat-row"><span class="label">{name}</span><span class="value">{masked}</span></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="stat-row"><span class="label">{name}</span><span style="color:#ff6b6b;">Not Set</span></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Quick Switch Provider")
    st.markdown("Edit `.env` file and restart to change. Or run:")
    st.code("""# Change active provider
export LLM_PROVIDER=groq
export LLM_PROVIDER=openrouter
export LLM_PROVIDER=gemini
export LLM_PROVIDER=ollama""")
    st.markdown('</div>', unsafe_allow_html=True)

with tools_tab:
    st.markdown("### Agent Registry")
    st.markdown(f"**{len(orch.agents)} agents registered**")
    agents_data = []
    for name, agent in orch.agents.items():
        agents_data.append({
            "Agent": name.capitalize(),
            "Class": agent.__class__.__name__,
        })
    st.dataframe(agents_data, use_container_width=True, hide_index=True)

    st.markdown("### Tool Registry")
    st.markdown(f"**{len(tools.list_tools())} tools registered**")
    tools_data = []
    for t in tools.list_tools():
        tools_data.append({
            "Tool": t["name"],
            "Description": t["description"],
        })
    st.dataframe(tools_data, use_container_width=True, hide_index=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Tool Safety Levels")
    st.markdown("""
| Level | Behavior | Tools |
|-------|----------|-------|
| Safe | Auto-execute | filesystem, code, git, python |
| Medium | Confirm required | shell (rm, chmod, apt), browser |
| Blocked | Never allowed | sudo, shutdown, mkfs, dd, fork bomb |
""")
    st.markdown("Audit log → `data/logs/safety_audit.log`")
    st.markdown('</div>', unsafe_allow_html=True)

with memory_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### HDD Chat Storage")
    hdd = get_storage_stats()
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{hdd['file_count']}</div><div class="metric-label">Chat Files</div></div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{hdd['total_size_mb']}MB</div><div class="metric-label">Total Size</div></div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{hdd['free_space_gb']}GB</div><div class="metric-label">Free Space</div></div>""", unsafe_allow_html=True)
    with col_d:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">Auto</div><div class="metric-label">Save Mode</div></div>""", unsafe_allow_html=True)
    st.markdown(f"**Location:** `{hdd['path']}`")
    with st.expander("Saved Chat Files"):
        for fname in hdd['files'][-20:]:
            st.markdown(f"- {fname}")
        if len(hdd['files']) > 20:
            st.markdown(f"... and {len(hdd['files']) - 20} more files")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Database Status")
    col1, col2, col3, col4 = st.columns(4)
    session_count = len(store.get_all_sessions()) if hasattr(store, 'get_all_sessions') else 0
    try:
        with open(store.db_path, 'rb') as f:
            db_bytes = len(f.read())
        db_mb = db_bytes / (1024 * 1024)
    except Exception:
        db_bytes = 0
        db_mb = 0

    with col1:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{store.db_path.exists()}</div><div class="metric-label">DB Exists</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{db_mb:.2f}MB</div><div class="metric-label">DB Size</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{settings.MEMORY_MAX_HISTORY}</div><div class="metric-label">Max History</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-box"><div class="metric-value">{'ON' if settings.MEMORY_ENABLE_SUMMARIZATION else 'OFF'}</div><div class="metric-label">Summarization</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Database Path")
    st.code(str(store.db_path.absolute()))
    st.markdown("Session ID", unsafe_allow_html=True)
    st.code(cm.session_id)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Data Files")
    data_dir = Path(settings.DATA_DIR)
    if data_dir.exists():
        for f in sorted(data_dir.rglob("*")):
            if f.is_file() and "__pycache__" not in str(f):
                size = f.stat().st_size
                unit = "KB" if size > 1024 else "B"
                size_disp = size / 1024 if size > 1024 else size
                st.markdown(f"""<div class="stat-row"><span class="label">{f.relative_to(data_dir.parent)}</span><span class="value">{size_disp:.1f} {unit}</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("`data/` directory not found")
    st.markdown('</div>', unsafe_allow_html=True)

with about_tab:
    st.markdown("### Jarvis v1.0.0")
    st.markdown("**Local AI Operating System Assistant**")

    st.markdown("#### Features")
    features = [
        "LLM Provider Abstraction (Ollama, Groq, OpenRouter, Gemini)",
        "Persistent SQLite Memory & Summarization",
        "Voice I/O (faster-whisper + Piper TTS + gTTS fallback)",
        "Multi-Agent Orchestration (6 agents: planner, coder, browser, memory, research, execution)",
        "Browser Automation (Playwright)",
        "Strategic Reasoning Layer (thinker, critic, planner)",
        "Safety-First Architecture (permissions, sandbox, audit)",
        "Streamlit Web UI (9 pages)",
        "FastAPI REST API with streaming",
        "Multi-language Support (English, Hindi, Hinglish)",
    ]
    for f in features:
        st.markdown(f"- {f}")

    st.markdown("#### System Prompt")
    with st.expander("View System Prompt"):
        st.text(SYSTEM_PROMPT)

    st.markdown("#### Environment")
    env_info = {
        "Python": sys.version.split()[0],
        "Platform": sys.platform,
        "CWD": os.getcwd(),
        "Env File": ".env exists" if Path(".env").exists() else ".env missing",
    }
    for k, v in env_info.items():
        st.markdown(f"""<div class="stat-row"><span class="label">{k}</span><span class="value">{v}</span></div>""", unsafe_allow_html=True)

    st.markdown("#### Key Dependencies")
    deps = ["streamlit", "fastapi", "openai", "ollama", "groq", "piper-tts", "faster-whisper", "playwright", "pygame", "gtts"]
    for dep in deps:
        try:
            mod = __import__(dep.replace("-", "_").replace(".", "_"))
            ver = getattr(mod, "__version__", "unknown")
            st.markdown(f"""<div class="stat-row"><span class="label">{dep}</span><span class="value">{ver}</span></div>""", unsafe_allow_html=True)
        except Exception:
            st.markdown(f"""<div class="stat-row"><span class="label">{dep}</span><span style="color:#ff6b6b;">Not Installed</span></div>""", unsafe_allow_html=True)

    st.markdown("#### Source")
    st.markdown("[GitHub Repository](https://github.com/anomalyco/opencode)")
