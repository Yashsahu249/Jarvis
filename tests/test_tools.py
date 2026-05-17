import pytest

from jarvis.tools.registry import ToolRegistry
from jarvis.tools.filesystem import FilesystemTool
from jarvis.tools.shell import ShellTool
from jarvis.tools.git_tool import GitTool
from jarvis.tools.code import CodeTool
from jarvis.tools.python_tool import PythonTool


def test_tool_registry():
    registry = ToolRegistry()
    tools = registry.list_tools()
    assert len(tools) >= 5

    names = [t["name"] for t in tools]
    assert "filesystem" in names
    assert "shell" in names
    assert "git" in names
    assert "code" in names
    assert "python" in names


@pytest.mark.asyncio
async def test_filesystem_tool_list():
    tool = FilesystemTool()
    result = await tool.execute(action="list", path=".")
    assert "Error" not in result


@pytest.mark.asyncio
async def test_filesystem_tool_invalid_path():
    tool = FilesystemTool()
    result = await tool.execute(action="list", path="/nonexistent_path_xyz")
    assert "does not exist" in result


def test_shell_tool_classification():
    tool = ShellTool()
    assert tool._classify("ls -la") == "safe"
    assert tool._classify("rm file.txt") == "confirm"
    assert tool._classify("shutdown -h now") == "blocked"


@pytest.mark.asyncio
async def test_shell_tool_no_command():
    tool = ShellTool()
    result = await tool.execute()
    assert "No command" in result


@pytest.mark.asyncio
async def test_code_tool_no_filepath():
    tool = CodeTool()
    result = await tool.execute(action="read")
    assert "No filepath" in result


@pytest.mark.asyncio
async def test_python_tool_no_code():
    tool = PythonTool()
    result = await tool.execute()
    assert "No code" in result


def test_tool_base_class():
    tool = ShellTool()
    d = tool.to_dict()
    assert "name" in d
    assert "description" in d
    assert d["name"] == "shell"
