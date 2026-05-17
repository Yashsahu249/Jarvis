from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.models.schemas import BrowserAction, BrowserState, BrowserScreenshot
from app.services.browser_service import browser_service

router = APIRouter(prefix="/browser", tags=["browser"])


@router.post("/launch")
async def launch_browser(headless: bool | None = None, user_data_dir: str | None = None):
    try:
        result = await browser_service.launch(headless=headless, user_data_dir=user_data_dir)
        return result
    except Exception as e:
        logger.error(f"Browser launch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/navigate")
async def navigate(url: str, page_id: str | None = None):
    try:
        result = await browser_service.navigate(url, page_id=page_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Navigation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screenshot", response_model=BrowserScreenshot)
async def take_screenshot(page_id: str | None = None, full_page: bool = False):
    try:
        result = await browser_service.screenshot(page_id=page_id, full_page=full_page)
        return BrowserScreenshot(base64=result["base64"], file_path=result["file_path"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/click")
async def click_element(action: BrowserAction):
    try:
        result = await browser_service.click(action.selector)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Click error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/type")
async def type_text(action: BrowserAction):
    try:
        result = await browser_service.type_text(action.selector, action.value)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Type error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tabs")
async def list_tabs():
    try:
        tabs = await browser_service.get_tabs()
        return {"tabs": tabs}
    except Exception as e:
        logger.error(f"List tabs error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/new-tab")
async def new_tab(url: str = "about:blank"):
    try:
        result = await browser_service.new_tab(url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"New tab error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/close")
async def close_browser():
    try:
        result = await browser_service.close_browser()
        return result
    except Exception as e:
        logger.error(f"Browser close error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
