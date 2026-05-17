import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import subprocess
import tempfile

st.set_page_config(page_title="Python Lab - Jarvis", page_icon="", layout="wide")

from jarvis.utils.async_utils import run_async

from jarvis.tools.python_tool import PythonTool

py_tool = PythonTool()

st.markdown("""
<style>
    .py-output {
        background: #0d0d0d;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Python Lab")
st.markdown("Write and execute Python code in a sandboxed environment")

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Safety Notes")
    st.markdown("""
    - Code runs in isolated subprocess
    - 30-second timeout
    - Blocked modules: `os`, `subprocess`, `shutil`, `eval`, `exec`
    - File system access is restricted
    """)

    st.markdown("### Quick Templates")
    template = st.selectbox(
        "Load template",
        ["", "Hello World", "File Organizer", "Data Analysis", "Web Scraper"],
    )

    if template == "Hello World":
        default_code = '''print("Hello from Jarvis Python Lab!")
print(f"2 + 2 = {2 + 2}")
print(f"Pi is approximately {3.14159:.4f}")'''
    elif template == "File Organizer":
        default_code = '''import pathlib
import shutil
from collections import Counter

path = pathlib.Path("./")
extensions = Counter()
for f in path.iterdir():
    if f.is_file():
        ext = f.suffix or "no_ext"
        extensions[ext] += 1

print("File type distribution:")
for ext, count in extensions.most_common():
    print(f"  .{ext}: {count} files")'''
    elif template == "Data Analysis":
        default_code = '''# Sample data analysis
data = {
    "Python": 45,
    "JavaScript": 38,
    "TypeScript": 28,
    "Go": 15,
    "Rust": 12,
}

total = sum(data.values())
print("Language Distribution:")
for lang, count in sorted(data.items(), key=lambda x: -x[1]):
    pct = (count / total) * 100
    bar = "#" * int(pct)
    print(f"{lang:12s} | {bar} {pct:.1f}%")'''
    elif template == "Web Scraper":
        default_code = '''# Simple HTTP request example
# Note: use the Browser tool for real web scraping
import urllib.request
import json

try:
    with urllib.request.urlopen("https://httpbin.org/get", timeout=5) as resp:
        data = json.loads(resp.read())
        print(f"Status: {resp.status}")
        print(f"Headers: {dict(resp.headers)}")
        print(f"Origin: {data.get('origin', 'unknown')}")
except Exception as e:
    print(f"Error: {e}")'''
    else:
        default_code = ""

    st.markdown("### History")
    if "py_history" not in st.session_state:
        st.session_state.py_history = []
    for entry in st.session_state.py_history[-5:]:
        st.text(f"  {entry}")

with col1:
    code = st.text_area(
        "Python Code",
        value=st.session_state.get("py_code", default_code),
        height=400,
        font="monospace",
        key="py_code",
    )

    run_col1, run_col2, run_col3 = st.columns([1, 1, 4])
    with run_col1:
        if st.button(" Run", use_container_width=True, type="primary"):
            if code.strip():
                with st.spinner("Executing..."):
                    result = run_async(py_tool.execute(code=code))
                st.session_state.py_output = result
                st.session_state.py_history.append(
                    f"Ran {len(code.splitlines())} lines"
                )
                st.rerun()

    with run_col2:
        if st.button(" Clear", use_container_width=True):
            st.session_state.py_code = ""
            st.session_state.py_output = ""
            st.rerun()

    st.markdown("### Output")
    output = st.session_state.get("py_output", "")
    if output:
        st.markdown(
            f'<div class="py-output">{output}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="py-output" style="color: #555;">Results appear here...</div>',
            unsafe_allow_html=True,
        )
