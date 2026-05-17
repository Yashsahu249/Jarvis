import subprocess
from pathlib import Path

from jarvis.tools.base import BaseTool
from jarvis.utils.logger import JarvisLogger


class GitTool(BaseTool):
    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.git")

    def name(self) -> str:
        return "git"

    def description(self) -> str:
        return "Clone, status, log, diff, and manage git repositories"

    async def execute(self, **kwargs) -> str:
        action = kwargs.get("action", "status")
        repo_path = kwargs.get("path", ".")
        url = kwargs.get("url", "")

        try:
            if action == "clone":
                if not url:
                    return "URL required for clone"
                target = kwargs.get("target", "")
                cmd = f"git clone {url}"
                if target:
                    cmd += f" {target}"
                result = subprocess.run(
                    cmd, shell=True, check=True, capture_output=True, text=True, timeout=120
                )
                return result.stdout.strip()

            elif action == "status":
                result = subprocess.run(
                    f"git -C {repo_path} status",
                    shell=True, check=True, capture_output=True, text=True, timeout=30
                )
                return result.stdout.strip()

            elif action == "log":
                count = kwargs.get("count", 10)
                result = subprocess.run(
                    f"git -C {repo_path} log --oneline -{count}",
                    shell=True, check=True, capture_output=True, text=True, timeout=30
                )
                return result.stdout.strip()

            elif action == "diff":
                result = subprocess.run(
                    f"git -C {repo_path} diff",
                    shell=True, check=True, capture_output=True, text=True, timeout=30
                )
                return result.stdout.strip()

            elif action == "branches":
                result = subprocess.run(
                    f"git -C {repo_path} branch -a",
                    shell=True, check=True, capture_output=True, text=True, timeout=30
                )
                return result.stdout.strip()

            else:
                return f"Unknown git action: {action}"

        except subprocess.TimeoutExpired:
            return "Git command timed out"
        except Exception as e:
            self.logger.error(f"Git error: {e}")
            return f"Error: {e}"
