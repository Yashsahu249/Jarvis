import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Workspace - Jarvis", page_icon="", layout="wide")

from jarvis.utils.async_utils import run_async

from jarvis.tools.filesystem import FilesystemTool
from jarvis.tools.code import CodeTool
from jarvis.utils.validators import is_safe_filename

filesystem = FilesystemTool()
code_tool = CodeTool()

st.markdown("""
<style>
    .file-item {
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: background 0.2s;
    }
    .file-item:hover { background: #2a2a2a; }
    .file-item.dir { color: #00BFA5; font-weight: 600; }
    .file-item.file { color: #ccc; }
    .editor-area { font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Workspace")
st.markdown("File browser & code editor")

if "workspace_path" not in st.session_state:
    st.session_state.workspace_path = "."
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "file_content" not in st.session_state:
    st.session_state.file_content = ""

col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### Files")

    path_input = st.text_input("Path", value=st.session_state.workspace_path, key="ws_path")
    if path_input != st.session_state.workspace_path:
        st.session_state.workspace_path = path_input
        st.session_state.current_file = None
        st.rerun()

    result = run_async(
        filesystem.execute(action="list", path=st.session_state.workspace_path)
    )

    if "Error" in result or "does not exist" in result:
        st.error(result)
    else:
        lines = result.split("\n")[1:] if result.startswith("Contents") else result.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            is_dir = line.endswith("/") or line.endswith("/")
            display = line
            if st.button(
                display,
                key=f"file_{line}",
                use_container_width=True,
                type="secondary" if not is_dir else "primary",
            ):
                full_path = str(Path(st.session_state.workspace_path) / line.rstrip("/"))
                p = Path(full_path)
                if p.is_dir():
                    st.session_state.workspace_path = str(p)
                    st.session_state.current_file = None
                else:
                    st.session_state.current_file = str(p)
                st.rerun()

    st.markdown("---")
    st.markdown("### Quick Actions")

    new_file = st.text_input("New file name", placeholder="file.py", key="new_file_name")
    if st.button("+ Create File", use_container_width=True) and new_file:
        if is_safe_filename(new_file):
            fpath = Path(st.session_state.workspace_path) / new_file
            if not fpath.exists():
                fpath.write_text("")
                st.session_state.current_file = str(fpath)
                st.rerun()
            else:
                st.warning("File exists")
        else:
            st.error("Invalid filename")

with col2:
    st.markdown("### Editor")

    if st.session_state.current_file:
        fpath = st.session_state.current_file

        tab1, tab2 = st.tabs(["Edit", "Info"])

        with tab1:
            content = run_async(
                code_tool.execute(action="read", filepath=fpath)
            )
            if "Error" in content and "not found" in content:
                st.error(content)
            else:
                edited = st.text_area(
                    f"Editing: {fpath}",
                    value=content,
                    height=500,
                    key="code_editor",
                )

                save_col1, save_col2, save_col3 = st.columns([1, 1, 4])
                with save_col1:
                    if st.button(" Save", use_container_width=True):
                        result = run_async(
                            code_tool.execute(
                                action="write",
                                filepath=fpath,
                                content=edited,
                            )
                        )
                        if "Error" in result:
                            st.error(result)
                        else:
                            st.success("Saved")
                with save_col2:
                    if st.button(" Run", use_container_width=True):
                        if fpath.endswith(".py"):
                            import subprocess
                            r = subprocess.run(
                                ["python3", fpath],
                                capture_output=True,
                                text=True,
                                timeout=10,
                            )
                            output = r.stdout
                            if r.stderr:
                                output += f"\nSTDERR:\n{r.stderr}"
                            st.code(output, language="bash")
                        else:
                            st.info("Run only works for .py files")

        with tab2:
            p = Path(fpath)
            st.markdown(f"**Path:** `{fpath}`")
            st.markdown(f"**Size:** {p.stat().st_size} bytes")
            st.markdown(f"**Modified:** {p.stat().st_mtime}")
            st.markdown(f"**Extension:** {p.suffix}")

            if st.button(" Delete File", type="secondary", use_container_width=True):
                p.unlink(missing_ok=True)
                st.session_state.current_file = None
                st.rerun()
    else:
        st.info("Select a file from the browser to start editing")
