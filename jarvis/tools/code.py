from pathlib import Path

from jarvis.tools.base import BaseTool
from jarvis.utils.logger import JarvisLogger


class CodeTool(BaseTool):
    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.code")

    def name(self) -> str:
        return "code"

    def description(self) -> str:
        return "Read, edit, create code files with safety checks"

    async def execute(self, **kwargs) -> str:
        action = kwargs.get("action", "read")
        filepath = kwargs.get("filepath", "")
        content = kwargs.get("content", "")
        line_start = kwargs.get("line_start")
        line_end = kwargs.get("line_end")

        if not filepath:
            return "No filepath provided"

        path = Path(filepath).resolve()

        try:
            if action == "read":
                if not path.exists():
                    return f"File not found: {filepath}"
                text = path.read_text(encoding="utf-8", errors="replace")
                lines = text.splitlines()
                if line_start is not None:
                    s = max(0, line_start - 1)
                    e = line_end if line_end else s + 50
                    text = "\n".join(lines[s:e])
                return text

            elif action == "write":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                return f"Written {len(content)} chars to {filepath}"

            elif action == "edit":
                if not path.exists():
                    return f"File not found: {filepath}"
                old = kwargs.get("old_string", "")
                new = kwargs.get("new_string", "")
                if not old:
                    return "old_string required for edit"
                text = path.read_text(encoding="utf-8")
                if old not in text:
                    return "old_string not found in file"
                text = text.replace(old, new, 1)
                path.write_text(text, encoding="utf-8")
                return f"Edited {filepath}"

            elif action == "insert":
                if not path.exists():
                    return f"File not found: {filepath}"
                insert_line = kwargs.get("line", 0)
                insert_content = kwargs.get("content", "")
                text = path.read_text(encoding="utf-8")
                lines = text.splitlines()
                lines.insert(max(0, insert_line - 1), insert_content)
                path.write_text("\n".join(lines), encoding="utf-8")
                return f"Inserted at line {insert_line} in {filepath}"

            else:
                return f"Unknown action: {action}"

        except Exception as e:
            self.logger.error(f"Code tool error: {e}")
            return f"Error: {e}"
