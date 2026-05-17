import asyncio

from jarvis.tools.base import BaseTool
from jarvis.config.settings import get_settings
from jarvis.utils.logger import JarvisLogger


class BrowserTool(BaseTool):
    def __init__(self):
        self.settings = get_settings()
        self.logger = JarvisLogger.get_logger("tools.browser")
        self._browser = None
        self._context = None
        self._page = None

    def name(self) -> str:
        return "browser"

    def description(self) -> str:
        return "Control a web browser: navigate, search, click, extract, screenshot"

    async def _ensure_browser(self):
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            headless = self.settings.BROWSER_HEADLESS
            if self.settings.BROWSER_VISIBLE:
                headless = False
            self._browser = await self._playwright.chromium.launch(
                headless=headless
            )
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            )
            self._page = await self._context.new_page()
            self.logger.info("Browser launched")

    async def execute(self, **kwargs) -> str:
        action = kwargs.get("action", "navigate")
        url = kwargs.get("url", "")
        query = kwargs.get("query", "")
        selector = kwargs.get("selector", "")

        try:
            await self._ensure_browser()

            if action == "navigate":
                if not url:
                    return "URL required"
                await self._page.goto(url, wait_until="domcontentloaded")
                return f"Navigated to {url}"

            elif action == "search":
                if not query:
                    return "Query required"
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                await self._page.goto(search_url, wait_until="domcontentloaded")
                text = await self._page.evaluate(
                    "() => document.body.innerText"
                )
                return text[:5000]

            elif action == "extract":
                if selector:
                    elements = await self._page.query_selector_all(selector)
                    texts = [await el.inner_text() for el in elements[:20]]
                    return "\n".join(texts)
                text = await self._page.evaluate(
                    "() => document.body.innerText"
                )
                return text[:5000]

            elif action == "screenshot":
                path = kwargs.get("path", "screenshot.png")
                await self._page.screenshot(path=path, full_page=True)
                return f"Screenshot saved to {path}"

            elif action == "click":
                if not selector:
                    return "Selector required"
                await self._page.click(selector)
                await self._page.wait_for_load_state("domcontentloaded")
                return f"Clicked {selector}"

            elif action == "type":
                if not selector:
                    return "Selector required"
                text = kwargs.get("text", "")
                await self._page.fill(selector, text)
                return f"Typed into {selector}"

            elif action == "get_html":
                html = await self._page.content()
                return html[:5000]

            elif action == "close":
                if self._browser:
                    await self._browser.close()
                    self._browser = None
                    self._page = None
                    self._context = None
                return "Browser closed"

            else:
                return f"Unknown action: {action}"

        except Exception as e:
            self.logger.error(f"Browser error: {e}")
            return f"Browser error: {e}"

    async def close(self):
        if self._browser:
            try:
                await self._browser.close()
            except Exception:
                pass
