import subprocess
import shlex

from jarvis.tools.base import BaseTool
from jarvis.utils.logger import JarvisLogger
from jarvis.utils.validators import validate_command


class ShellTool(BaseTool):
    SAFE_COMMANDS = [
        "ls", "pwd", "whoami", "date", "cal", "echo", "cat", "head",
        "tail", "wc", "sort", "uniq", "cut", "find", "grep", "which",
        "python3", "python", "pip", "pip3", "node", "npm", "npx",
        "git", "curl", "wget", "mkdir", "touch", "cp", "mv",
    ]

    CONFIRM_COMMANDS = [
        "rm", "chmod", "chown", "apt", "apt-get", "docker", "systemctl",
        "service", "kill", "pkill", "ln",
    ]

    BLOCKED_PATTERNS = [
        "shutdown", "reboot", "mkfs", "dd", "sudo", "su",
        "chmod 777 /", "rm -rf /", ":(){:|:&};:", "> /dev/",
        "mkfs.ext4", "fdisk", "parted", "format",
    ]

    def __init__(self):
        self.logger = JarvisLogger.get_logger("tools.shell")

    def name(self) -> str:
        return "shell"

    def description(self) -> str:
        return "Execute shell commands (with safety restrictions)"

    def _classify(self, command: str) -> str:
        cmd = shlex.split(command)[0] if shlex.split(command) else ""
        if any(p in command for p in self.BLOCKED_PATTERNS):
            return "blocked"
        if cmd in self.CONFIRM_COMMANDS:
            return "confirm"
        if cmd in self.SAFE_COMMANDS:
            return "safe"
        return "unknown"

    async def execute(self, **kwargs) -> str:
        command = kwargs.get("command", "")
        if not command:
            return "No command provided"

        validation = validate_command(command)
        if validation:
            return validation

        classification = self._classify(command)
        if classification == "blocked":
            return f"Blocked dangerous command: {command}"
        if classification == "unknown":
            return f"Command not in allowed list: {shlex.split(command)[0]}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            if result.returncode != 0:
                output += f"\nExit code: {result.returncode}"
            return output.strip()
        except subprocess.TimeoutExpired:
            return "Command timed out (30s)"
        except Exception as e:
            self.logger.error(f"Shell error: {e}")
            return f"Error: {e}"
