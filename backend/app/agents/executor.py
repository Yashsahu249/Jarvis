import os
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Any
from loguru import logger
from app.core.security import validate_command, RiskLevel
from app.core.config import settings
from app.models.schemas import CommandExecuteResponse


class ExecutorAgent:
    def __init__(self):
        self.id = "executor"
        self.name = "Executor Agent"
        self.role = "executor"
        self.sandbox_dir = Path(tempfile.gettempdir()) / "jarvis_sandbox"
        if settings.SANDBOX_ENABLED:
            self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    async def execute_command(self, command: str, timeout: int = 30, workdir: str | None = None) -> CommandExecuteResponse:
        is_valid, message, risk = validate_command(command)
        if not is_valid:
            return CommandExecuteResponse(
                exit_code=-1, stdout="", stderr=message,
                risk_level=risk, confirmed=False, duration=0,
            )

        if risk == RiskLevel.HIGH and settings.REQUIRE_CONFIRMATION:
            return CommandExecuteResponse(
                exit_code=-1, stdout="", stderr="Command requires confirmation",
                risk_level=risk, confirmed=False, duration=0,
            )

        cwd = workdir or str(self.sandbox_dir if settings.SANDBOX_ENABLED else Path.cwd())

        import time
        start = time.time()
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env={**os.environ, "PATH": os.environ.get("PATH", "")},
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                return CommandExecuteResponse(
                    exit_code=-1, stdout="", stderr=f"Command timed out after {timeout}s",
                    risk_level=risk, confirmed=True, duration=time.time() - start,
                )

            duration = time.time() - start
            return CommandExecuteResponse(
                exit_code=proc.returncode or 0,
                stdout=stdout.decode("utf-8", errors="replace"),
                stderr=stderr.decode("utf-8", errors="replace"),
                risk_level=risk,
                confirmed=True,
                duration=duration,
            )
        except Exception as e:
            return CommandExecuteResponse(
                exit_code=-1, stdout="", stderr=str(e),
                risk_level=risk, confirmed=True, duration=time.time() - start,
            )

    async def run_python(self, code: str, timeout: int = 15) -> dict:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()
            filepath = f.name

        try:
            result = await self.execute_command(f"python3 {filepath}", timeout=timeout)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
                "success": result.exit_code == 0,
            }
        finally:
            os.unlink(filepath)

    async def read_file(self, path: str) -> dict:
        try:
            resolved = Path(path).resolve()
            content = resolved.read_text(encoding="utf-8", errors="replace")
            return {"path": path, "content": content, "size": resolved.stat().st_size, "success": True}
        except Exception as e:
            return {"path": path, "error": str(e), "success": False}

    async def write_file(self, path: str, content: str) -> dict:
        try:
            resolved = Path(path).resolve()
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(content, encoding="utf-8")
            return {"path": path, "size": len(content), "success": True}
        except Exception as e:
            return {"path": path, "error": str(e), "success": False}

    async def list_directory(self, path: str = ".") -> dict:
        try:
            resolved = Path(path).resolve()
            items = []
            for item in sorted(resolved.iterdir()):
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                })
            return {"path": str(resolved), "items": items, "count": len(items), "success": True}
        except Exception as e:
            return {"path": path, "error": str(e), "success": False}

    async def install_package(self, package: str, manager: str = "pip") -> dict:
        return await self.execute_command(f"{manager} install {package}", timeout=120)

    async def run_pipeline(self, steps: list[dict]) -> list[dict]:
        results = []
        for step in steps:
            action = step.get("action", "command")
            if action == "command":
                result = await self.execute_command(
                    step.get("command", ""),
                    timeout=step.get("timeout", 30),
                    workdir=step.get("workdir"),
                )
            elif action == "python":
                result = await self.run_python(step.get("code", ""), timeout=step.get("timeout", 15))
            elif action == "read":
                result = await self.read_file(step.get("path", ""))
            elif action == "write":
                result = await self.write_file(step.get("path", ""), step.get("content", ""))
            else:
                result = {"error": f"Unknown action: {action}", "success": False}

            results.append({"step": step, "result": result})
            if not result.get("success", True) and step.get("fail_fast", False):
                break
        return results


executor_agent = ExecutorAgent()
