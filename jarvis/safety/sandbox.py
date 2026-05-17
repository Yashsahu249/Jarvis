import subprocess
import tempfile
from pathlib import Path

from jarvis.utils.logger import JarvisLogger


class Sandbox:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("safety.sandbox")

    def execute_safe(self, code: str, language: str = "python") -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            if language == "python":
                script_path = tmpdir_path / "script.py"
                script_path.write_text(code, encoding="utf-8")
                try:
                    result = subprocess.run(
                        ["python3", "-c", code],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        cwd=tmpdir,
                    )
                    output = result.stdout
                    if result.stderr:
                        output += f"\nSTDERR:\n{result.stderr}"
                    return output
                except subprocess.TimeoutExpired:
                    return "Execution timed out"
                except Exception as e:
                    return f"Error: {e}"
            return f"Unsupported language: {language}"
