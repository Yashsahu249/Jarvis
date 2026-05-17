import subprocess
import tempfile
from pathlib import Path

from jarvis.tools.base import BaseTool
from jarvis.utils.logger import JarvisLogger


class PythonTool(BaseTool):
    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.python")

    def name(self) -> str:
        return "python"

    def description(self) -> str:
        return "Execute Python code in an isolated subprocess"

    async def execute(self, **kwargs) -> str:
        code = kwargs.get("code", "")
        filepath = kwargs.get("filepath", "")
        timeout = min(int(kwargs.get("timeout", 30)), 60)

        if filepath:
            code = Path(filepath).read_text(encoding="utf-8", errors="replace")

        if not code:
            return "No code provided"

        blocked_patterns = [
            "import os", "import subprocess", "import shutil",
            "__import__('os')", "eval(", "exec(", "compile(",
            "open(", "file(",
        ]
        for pattern in blocked_patterns:
            if pattern in code:
                return f"Blocked unsafe pattern: {pattern}"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as f:
                f.write(code)
                f.flush()
                fname = f.name

            result = subprocess.run(
                ["python3", fname],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={"PYTHONIOENCODING": "utf-8"},
            )

            Path(fname).unlink(missing_ok=True)

            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output.strip()

        except subprocess.TimeoutExpired:
            Path(fname).unlink(missing_ok=True)
            return f"Execution timed out after {timeout}s"
        except Exception as e:
            self.logger.error(f"Python execution error: {e}")
            return f"Error: {e}"
