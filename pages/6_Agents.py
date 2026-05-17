import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Agents - Jarvis", page_icon="", layout="wide")

from jarvis.utils.async_utils import run_async

from jarvis.agents.orchestrator import get_orchestrator
from jarvis.tools.registry import get_tool_registry

orchestrator = get_orchestrator()
tools = get_tool_registry()

st.markdown("""
<style>
    .agent-card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .agent-name { color: #00BFA5; font-weight: 600; }
    .result-box {
        background: #0d0d0d;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Agent System")
st.markdown("Multi-agent task delegation & orchestration")

if "agent_results" not in st.session_state:
    st.session_state.agent_results = {}

col1, col2 = st.columns([2, 1.5])

with col2:
    st.markdown("### Available Agents")
    for name, agent in orchestrator.agents.items():
        st.markdown(
            f'<div class="agent-card">'
            f'<div class="agent-name">{name.capitalize()} Agent</div>'
            f'<div style="font-size: 0.8rem; color: #888; margin-top: 0.2rem;">'
            f'{agent.system_prompt[:100]}...</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Agent Routing Rules")
    st.markdown("""
    - **Coding** → write, code, program, script, implement
    - **Browser** → google, website, navigate, open url
    - **Memory** → remember, recall, store
    - **Research** → research, investigate, study
    - **Execution** → run, execute, shell, command
    - **Planner** → everything else
    """)

with col1:
    st.markdown("### Delegate Task")

    agent_choice = st.selectbox(
        "Target Agent (auto = let Jarvis decide)",
        ["auto", "planner", "coder", "browser", "memory", "research", "execution"],
    )

    task = st.text_area(
        "Task Description",
        placeholder="Write a Python script to organize my Downloads folder by file type...",
        height=150,
    )

    context_input = st.text_area(
        "Additional Context (optional)",
        placeholder="The Downloads folder is at ~/Downloads. Sort files into subfolders: Images, Documents, Code, Archives, Others.",
        height=80,
    )

    if st.button(" Execute Task", use_container_width=True, type="primary"):
        if not task:
            st.error("Please describe a task")
        else:
            with st.spinner(f"{'Auto-selecting agent' if agent_choice == 'auto' else f'Running {agent_choice} agent'}..."):
                try:
                    agent_name = None if agent_choice == "auto" else agent_choice
                    context_list = (
                        [{"role": "system", "content": f"Context: {context_input}"}]
                        if context_input
                        else None
                    )

                    result = run_async(
                        orchestrator.delegate(task, agent_name=agent_name)
                    )

                    used_agent = agent_choice if agent_choice != "auto" else "auto-selected"
                    st.session_state.agent_results[task[:50]] = {
                        "agent": used_agent,
                        "task": task,
                        "result": result,
                    }
                    st.success(f"Task completed by {used_agent} agent")
                except Exception as e:
                    st.error(f"Task failed: {e}")

    st.markdown("### Results")
    if st.session_state.agent_results:
        for key, data in reversed(list(st.session_state.agent_results.items())):
            with st.expander(f"[{data['agent']}] {key}..."):
                st.markdown(f"**Agent:** {data['agent']}")
                st.markdown(f"**Task:** {data['task']}")
                st.markdown(
                    f'<div class="result-box">{data["result"]}</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.info("No results yet. Delegate a task to see results here.")
