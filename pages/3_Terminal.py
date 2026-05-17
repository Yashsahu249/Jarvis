import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Terminal - Jarvis", page_icon="", layout="wide")

from jarvis.utils.async_utils import run_async

from jarvis.tools.shell import ShellTool
from jarvis.utils.validators import validate_command

shell = ShellTool()

st.markdown("""
<style>
    .terminal {
        background: #0d0d0d;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        border: 1px solid #333;
        min-height: 300px;
        max-height: 500px;
        overflow-y: auto;
    }
    .terminal-prompt { color: #00BFA5; }
    .terminal-output { color: #ccc; white-space: pre-wrap; }
    .terminal-error { color: #ff6b6b; }
    .terminal-cmd { background: #1a1a1a; border: 1px solid #333; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Terminal")
st.markdown("Execute shell commands with safety restrictions")

if "terminal_history" not in st.session_state:
    st.session_state.terminal_history = []
if "term_output" not in st.session_state:
    st.session_state.term_output = ""

col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Safety Rules")
    st.markdown("**Safe** (auto): ls, pwd, cat, echo, git, python, pip, curl, mkdir, cp, mv")
    st.markdown("**Confirm** required: rm, chmod, apt, docker")
    st.markdown("**Blocked**: sudo, shutdown, mkfs, dd, rm -rf /")

    st.markdown("---")
    st.markdown("### Command History")
    for i, cmd in enumerate(st.session_state.terminal_history[-10:]):
        st.text(f"$ {cmd}")

    if st.button(" Clear Terminal", use_container_width=True):
        st.session_state.terminal_history = []
        st.session_state.term_output = ""
        st.rerun()

with col1:
    st.markdown('<div class="terminal">', unsafe_allow_html=True)

    if st.session_state.term_output:
        st.markdown(
            f'<div class="terminal-output">{st.session_state.term_output}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    cmd = st.text_input(
        "$ command",
        placeholder="ls -la",
        key="terminal_input",
    )

    if cmd:
        if cmd.lower() in ("clear", "cls"):
            st.session_state.term_output = ""
            st.session_state.terminal_history.append(cmd)
            st.rerun()

        st.session_state.terminal_history.append(cmd)

        validation = validate_command(cmd)
        if validation:
            output = f"\n[BLOCKED] {validation}"
        else:
            try:
                result = run_async(shell.execute(command=cmd))
                output = result if result else "(no output)"
            except Exception as e:
                output = f"\n[ERROR] {e}"

        st.session_state.term_output += f"\n$ {cmd}\n{output}\n"
        st.rerun()
