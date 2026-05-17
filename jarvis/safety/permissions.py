from jarvis.utils.logger import JarvisLogger


class PermissionSystem:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("safety.permissions")
        self._confirmed_commands: set[str] = set()

    def classify_tool(self, tool_name: str, action: str = "") -> str:
        safe_tools = {"filesystem", "code", "python", "git"}
        medium_tools = {"shell", "browser"}
        high_risk_actions = {
            "shell": ["rm", "mv", "chmod", "apt", "docker"],
            "filesystem": ["delete", "wipe"],
            "git": ["push", "force", "reset"],
        }

        if tool_name in safe_tools:
            return "safe"
        if tool_name in medium_tools:
            for risk_cmd in high_risk_actions.get(tool_name, []):
                if risk_cmd in action:
                    return "medium"
            return "safe"
        return "medium"

    def needs_confirmation(self, tool_name: str, action: str) -> bool:
        level = self.classify_tool(tool_name, action)
        return level == "medium"

    def confirm(self, command_key: str) -> bool:
        if command_key in self._confirmed_commands:
            return True
        return False

    def add_confirmation(self, command_key: str):
        self._confirmed_commands.add(command_key)

    def reset(self):
        self._confirmed_commands.clear()
