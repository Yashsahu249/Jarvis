from jarvis.tools.base import BaseTool
from jarvis.tools.filesystem import FilesystemTool
from jarvis.tools.shell import ShellTool
from jarvis.tools.git_tool import GitTool
from jarvis.tools.code import CodeTool
from jarvis.tools.browser_tool import BrowserTool
from jarvis.tools.python_tool import PythonTool
from jarvis.utils.logger import JarvisLogger


class ToolRegistry:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.registry")
        self._tools: dict[str, BaseTool] = {}
        self._register_defaults()

    def _register_defaults(self):
        tools = [
            FilesystemTool(),
            ShellTool(),
            GitTool(),
            CodeTool(),
            BrowserTool(),
            PythonTool(),
        ]
        for tool in tools:
            self.register(tool)

    def register(self, tool: BaseTool):
        self._tools[tool.name()] = tool
        self.logger.debug(f"Registered tool: {tool.name()}")

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        return [t.to_dict() for t in self._tools.values()]

    def get_all(self) -> dict[str, BaseTool]:
        return dict(self._tools)


_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry
