from pathlib import Path

from jarvis.tools.base import BaseTool
from jarvis.utils.logger import JarvisLogger


class FilesystemTool(BaseTool):
    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.filesystem")

    def name(self) -> str:
        return "filesystem"

    def description(self) -> str:
        return "Read, write, list files and directories"

    async def execute(self, **kwargs) -> str:
        action = kwargs.get("action", "list")
        path = kwargs.get("path", ".")

        try:
            if action == "list":
                p = Path(path)
                if not p.exists():
                    return f"Path does not exist: {path}"
                if p.is_dir():
                    items = "\n".join(str(x.name) for x in p.iterdir())
                    return f"Contents of {path}:\n{items}"
                return f"Not a directory: {path}"

            elif action == "read":
                p = Path(path)
                if not p.exists():
                    return f"File not found: {path}"
                content = p.read_text(encoding="utf-8", errors="replace")
                return content

            elif action == "write":
                p = Path(path)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(kwargs.get("content", ""), encoding="utf-8")
                return f"Written to {path}"

            elif action == "exists":
                return str(Path(path).exists())

            else:
                return f"Unknown action: {action}"

        except Exception as e:
            self.logger.error(f"Filesystem error: {e}")
            return f"Error: {e}"
