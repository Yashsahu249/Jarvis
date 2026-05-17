import asyncio
import subprocess
import time
from fastapi import APIRouter, HTTPException
from loguru import logger
from app.core.security import validate_command, RiskLevel
from app.core.config import settings
from app.models.schemas import ToolInfo, CommandExecuteRequest, CommandExecuteResponse

router = APIRouter(prefix="/tools", tags=["tools"])

AVAILABLE_TOOLS = [
    ToolInfo(
        id="terminal",
        name="Terminal",
        description="Execute shell commands in the system terminal",
        category="system",
        parameters={"command": {"type": "string", "description": "Command to execute"}, "timeout": {"type": "integer", "default": 30}},
        risk_level=RiskLevel.MEDIUM,
    ),
    ToolInfo(
        id="read_file",
        name="Read File",
        description="Read contents of a file",
        category="filesystem",
        parameters={"path": {"type": "string", "description": "Path to file"}},
        risk_level=RiskLevel.SAFE,
    ),
    ToolInfo(
        id="write_file",
        name="Write File",
        description="Write content to a file",
        category="filesystem",
        parameters={"path": {"type": "string", "description": "Path to file"}, "content": {"type": "string", "description": "Content to write"}},
        risk_level=RiskLevel.MEDIUM,
    ),
    ToolInfo(
        id="list_dir",
        name="List Directory",
        description="List files and directories",
        category="filesystem",
        parameters={"path": {"type": "string", "default": "."}},
        risk_level=RiskLevel.SAFE,
    ),
    ToolInfo(
        id="web_search",
        name="Web Search",
        description="Search the web for information",
        category="web",
        parameters={"query": {"type": "string", "description": "Search query"}},
        risk_level=RiskLevel.SAFE,
    ),
    ToolInfo(
        id="web_fetch",
        name="Web Fetch",
        description="Fetch content from a URL",
        category="web",
        parameters={"url": {"type": "string", "description": "URL to fetch"}},
        risk_level=RiskLevel.SAFE,
    ),
    ToolInfo(
        id="code_analyze",
        name="Code Analysis",
        description="Analyze code for bugs, style, and improvements",
        category="development",
        parameters={"code": {"type": "string", "description": "Code to analyze"}, "language": {"type": "string"}},
        risk_level=RiskLevel.SAFE,
    ),
    ToolInfo(
        id="browser",
        name="Browser Automation",
        description="Control a web browser",
        category="automation",
        parameters={"action": {"type": "string"}, "url": {"type": "string", "optional": True}},
        risk_level=RiskLevel.MEDIUM,
    ),
]


@router.get("", response_model=list[ToolInfo])
async def list_tools():
    return AVAILABLE_TOOLS


@router.post("/execute", response_model=CommandExecuteResponse)
async def execute_tool(req: CommandExecuteRequest):
    is_valid, message, risk = validate_command(req.command)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    auto_safe = settings.AUTO_EXECUTE_SAFE
    require_confirm = settings.REQUIRE_CONFIRMATION

    if risk == RiskLevel.HIGH and require_confirm and not req.shell:
        return CommandExecuteResponse(
            exit_code=-1,
            stdout="",
            stderr="",
            risk_level=risk,
            confirmed=False,
            duration=0,
        )

    start = time.time()
    try:
        if req.shell:
            proc = subprocess.run(
                req.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=req.timeout,
                cwd=req.workdir,
                env=req.env,
            )
        else:
            parts = req.command.split()
            proc = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=req.timeout,
                cwd=req.workdir,
                env=req.env,
            )

        duration = time.time() - start
        return CommandExecuteResponse(
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            risk_level=risk,
            confirmed=True,
            duration=duration,
        )
    except subprocess.TimeoutExpired:
        return CommandExecuteResponse(
            exit_code=-1,
            stdout="",
            stderr=f"Command timed out after {req.timeout}s",
            risk_level=risk,
            confirmed=True,
            duration=req.timeout,
        )
    except FileNotFoundError as e:
        return CommandExecuteResponse(
            exit_code=-1,
            stdout="",
            stderr=str(e),
            risk_level=risk,
            confirmed=True,
            duration=time.time() - start,
        )
    except Exception as e:
        logger.error(f"Command execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
