import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Browser - Jarvis", page_icon="", layout="wide")

from jarvis.utils.async_utils import run_async

from jarvis.tools.browser_tool import BrowserTool

browser = BrowserTool()

st.markdown("""
<style>
    .browser-view {
        background: #1e1e1e;
        border-radius: 8px;
        border: 1px solid #333;
        padding: 0;
        overflow: hidden;
    }
    .browser-url {
        background: #0d0d0d;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #333;
        font-family: monospace;
        font-size: 0.85rem;
    }
    .browser-content {
        padding: 1rem;
        font-size: 0.85rem;
        max-height: 600px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("##  Browser Automation")
st.markdown("Control a web browser via Playwright")

if "browser_url" not in st.session_state:
    st.session_state.browser_url = ""
if "browser_content" not in st.session_state:
    st.session_state.browser_content = ""
if "browser_log" not in st.session_state:
    st.session_state.browser_log = []

col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Actions")
    action = st.selectbox(
        "Action",
        ["Navigate", "Search", "Extract Text", "Screenshot", "Click", "Type", "Get HTML", "Close"],
    )

    if action == "Navigate":
        url = st.text_input("URL", placeholder="https://example.com")
        if st.button(" Go", use_container_width=True):
            result = run_async(
                browser.execute(action="navigate", url=url)
            )
            st.session_state.browser_log.append(f"Navigated to {url}")
            st.session_state.browser_content = result

    elif action == "Search":
        query = st.text_input("Search query", placeholder="what is AI?")
        if st.button(" Search", use_container_width=True):
            result = run_async(
                browser.execute(action="search", query=query)
            )
            st.session_state.browser_log.append(f"Searched: {query}")
            st.session_state.browser_content = result[:5000]

    elif action == "Extract Text":
        selector = st.text_input("CSS Selector (optional)", placeholder="body")
        if st.button(" Extract", use_container_width=True):
            result = run_async(
                browser.execute(action="extract", selector=selector)
            )
            st.session_state.browser_log.append("Extracted text")
            st.session_state.browser_content = result[:5000]

    elif action == "Screenshot":
        path = st.text_input("Save path", value="screenshot.png")
        if st.button(" Capture", use_container_width=True):
            result = run_async(
                browser.execute(action="screenshot", path=path)
            )
            st.session_state.browser_log.append(f"Screenshot: {path}")
            st.markdown(f"![]({path})")

    elif action == "Click":
        selector = st.text_input("Selector to click")
        if st.button(" Click", use_container_width=True):
            result = run_async(
                browser.execute(action="click", selector=selector)
            )
            st.session_state.browser_log.append(f"Clicked: {selector}")
            st.session_state.browser_content = result

    elif action == "Type":
        selector = st.text_input("Selector")
        text = st.text_input("Text to type")
        if st.button(" Type", use_container_width=True):
            result = run_async(
                browser.execute(action="type", selector=selector, text=text)
            )
            st.session_state.browser_log.append(f"Typed into: {selector}")
            st.session_state.browser_content = result

    elif action == "Get HTML":
        if st.button(" Get HTML", use_container_width=True):
            result = run_async(browser.execute(action="get_html"))
            st.session_state.browser_log.append("Got page HTML")
            st.session_state.browser_content = result[:5000]

    elif action == "Close":
        if st.button(" Close Browser", use_container_width=True):
            run_async(browser.close())
            st.session_state.browser_log.append("Browser closed")
            st.session_state.browser_content = ""

    st.markdown("### Activity Log")
    for entry in st.session_state.browser_log[-10:]:
        st.text(f"  {entry}")

with col1:
    st.markdown("### Browser View")

    if st.session_state.browser_content:
        st.markdown(
            f'<div class="browser-view">'
            f'<div class="browser-content">{st.session_state.browser_content}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("Use the controls to interact with the browser")
        st.markdown("""
        **Tips:**
        - Start with **Navigate** to open a URL
        - Use **Search** for Google searches
        - **Extract Text** to read page content
        - **Screenshot** to capture the page
        - **Click** interacts with page elements
        """)
