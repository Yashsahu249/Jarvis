import asyncio
import base64
from pathlib import Path
from typing import Any
from loguru import logger
from app.core.config import settings


class BrowserService:
    def __init__(self):
        self.browser = None
        self.context = None
        self.pages: dict[str, Any] = {}
        self.active_page_id: str | None = None
        self._lock = asyncio.Lock()

    async def launch(self, headless: bool | None = None, user_data_dir: str | None = None) -> dict:
        async with self._lock:
            if self.browser:
                return {"status": "already_running", "pages": len(self.pages)}

            try:
                from playwright.async_api import async_playwright

                self._playwright = await async_playwright().start()
                launch_options = {"headless": headless if headless is not None else settings.BROWSER_HEADLESS}
                if user_data_dir:
                    launch_options["user_data_dir"] = user_data_dir

                self.browser = await self._playwright.chromium.launch(**launch_options)
                self.context = await self.browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                )
                page = await self.context.new_page()
                page_id = str(id(page))
                self.pages[page_id] = page
                self.active_page_id = page_id

                logger.info(f"Browser launched with {len(self.pages)} page(s)")
                return {"status": "launched", "page_id": page_id, "pages": len(self.pages)}
            except Exception as e:
                logger.error(f"Browser launch error: {e}")
                raise

    async def navigate(self, url: str, page_id: str | None = None) -> dict:
        page = await self._get_page(page_id)
        if not page:
            raise ValueError("No active browser page")
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        title = await page.title()
        return {"url": page.url, "title": title, "status_code": resp.status if resp else None}

    async def screenshot(self, page_id: str | None = None, full_page: bool = False) -> dict:
        page = await self._get_page(page_id)
        if not page:
            raise ValueError("No active browser page")
        screenshot_bytes = await page.screenshot(full_page=full_page)
        b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        output_dir = Path(settings.MEMORY_DB_PATH).parent / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = str(output_dir / f"screenshot_{id(page)}.png")
        with open(file_path, "wb") as f:
            f.write(screenshot_bytes)
        return {"base64": b64, "file_path": file_path}

    async def click(self, selector: str, page_id: str | None = None) -> dict:
        page = await self._get_page(page_id)
        if not page:
            raise ValueError("No active browser page")
        await page.click(selector)
        return {"selector": selector, "url": page.url}

    async def type_text(self, selector: str, text: str, page_id: str | None = None) -> dict:
        page = await self._get_page(page_id)
        if not page:
            raise ValueError("No active browser page")
        await page.fill(selector, text)
        return {"selector": selector, "text_length": len(text), "url": page.url}

    async def get_tabs(self) -> list[dict]:
        tabs = []
        for pid, page in self.pages.items():
            try:
                title = await page.title()
                url = page.url
                tabs.append({"page_id": pid, "title": title, "url": url, "active": pid == self.active_page_id})
            except Exception:
                tabs.append({"page_id": pid, "title": "unknown", "url": "unknown", "active": pid == self.active_page_id})
        return tabs

    async def new_tab(self, url: str = "about:blank") -> dict:
        if not self.context:
            raise ValueError("Browser not launched")
        page = await self.context.new_page()
        if url != "about:blank":
            await page.goto(url, wait_until="domcontentloaded")
        page_id = str(id(page))
        self.pages[page_id] = page
        self.active_page_id = page_id
        return {"page_id": page_id, "url": page.url}

    async def close_page(self, page_id: str | None = None) -> dict:
        if page_id and page_id in self.pages:
            page = self.pages.pop(page_id)
            await page.close()
        if self.active_page_id == page_id or not page_id:
            self.active_page_id = next(iter(self.pages.keys())) if self.pages else None
        return {"closed": page_id, "remaining_pages": len(self.pages)}

    async def close_browser(self) -> dict:
        async with self._lock:
            for pid, page in list(self.pages.items()):
                try:
                    await page.close()
                except Exception:
                    pass
            self.pages.clear()
            self.active_page_id = None
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            if hasattr(self, "_playwright") and self._playwright:
                await self._playwright.stop()
            logger.info("Browser closed")
            return {"status": "closed"}

    async def _get_page(self, page_id: str | None = None) -> Any | None:
        if page_id and page_id in self.pages:
            return self.pages[page_id]
        if self.active_page_id and self.active_page_id in self.pages:
            return self.pages[self.active_page_id]
        return None


browser_service = BrowserService()
