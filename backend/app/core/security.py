from enum import Enum
import re
import os
from pathlib import Path


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


SAFE_COMMANDS = {
    "ls", "pwd", "echo", "cat", "head", "tail", "wc", "sort",
    "uniq", "cut", "tr", "grep", "find", "locate", "which",
    "date", "cal", "df", "du", "ps", "top", "htop", "whoami",
    "id", "uname", "env", "printenv", "history", "clear",
    "tree", "stat", "file", "type", "time", "help", "man",
}

MEDIUM_COMMANDS = {
    "mkdir", "rmdir", "touch", "cp", "mv", "rm", "chmod",
    "chown", "ln", "tar", "gzip", "gunzip", "zip", "unzip",
    "make", "gcc", "g++", "python", "python3", "node", "npm",
    "pip", "pip3", "cargo", "rustc", "go", "deno", "bun",
    "git", "docker", "docker-compose", "curl", "wget",
    "ping", "nslookup", "dig", "nmap", "netstat", "ss",
    "kill", "killall", "pkill", "nohup", "screen", "tmux",
    "crontab", "at", "batch", "systemctl", "service",
    "journalctl", "dmesg", "lsblk", "mount", "umount",
}

HIGH_COMMANDS = {
    "sudo", "su", "passwd", "adduser", "useradd", "deluser",
    "userdel", "groupadd", "groupdel", "usermod", "chsh",
    "mkfs", "fdisk", "parted", "dd", "shutdown", "reboot",
    "halt", "poweroff", "init", "grub", "lilo", "modprobe",
    "insmod", "rmmod", "iptables", "ufw", "firewall-cmd",
    "visudo", "scp", "ssh", "telnet", "expect",
    "wpa_passphrase", "iwconfig", "ifconfig", "ip",
    "route", "arp", "ethtool", "iwlist",
}

BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"mkfs\.",
    r"dd\s+if=",
    r">\s*/dev/sd",
    r":\(\)\s*\{",
    r"\|\s*sh\s*$",
    r"\|\s*bash\s*$",
    r"curl\s+.*\|\s*sh",
    r"wget\s+.*\|\s*sh",
    r"eval\s",
    r"exec\s",
    r"source\s+\/dev",
    r"<\s*/dev/sd",
]


def assess_risk(command: str) -> RiskLevel:
    if check_blocked_pattern(command):
        return RiskLevel.HIGH

    base_cmd = command.strip().split()[0].lower() if command.strip() else ""
    base_cmd = os.path.basename(base_cmd)

    if base_cmd in HIGH_COMMANDS:
        return RiskLevel.HIGH
    if base_cmd in MEDIUM_COMMANDS:
        return RiskLevel.MEDIUM
    if base_cmd in SAFE_COMMANDS:
        return RiskLevel.SAFE

    return RiskLevel.MEDIUM


def check_blocked_pattern(command: str) -> bool:
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            return True
    return False


def check_path_traversal(path: str) -> bool:
    resolved = Path(path).resolve()
    home = Path.home()
    allowed_dirs = [home, Path("/tmp"), Path("/var/tmp")]
    for allowed in allowed_dirs:
        if str(resolved).startswith(str(allowed)):
            return False
    return False


def validate_command(command: str) -> tuple[bool, str, RiskLevel]:
    if not command or not command.strip():
        return False, "Command cannot be empty", RiskLevel.SAFE

    risk = assess_risk(command)
    if risk == RiskLevel.HIGH and not check_blocked_pattern(command):
        pass

    if check_blocked_pattern(command):
        return False, "Command contains blocked patterns", RiskLevel.HIGH

    paths = re.findall(r'/[^\s\'"]+', command)
    for p in paths:
        if check_path_traversal(p):
            return False, f"Path traversal detected: {p}", RiskLevel.HIGH

    return True, "Command validated", risk
