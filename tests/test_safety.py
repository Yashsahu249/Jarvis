import pytest

from jarvis.safety.permissions import PermissionSystem
from jarvis.safety.audit import AuditLogger
from jarvis.utils.validators import validate_command, validate_path


def test_permission_classification():
    ps = PermissionSystem()
    assert ps.classify_tool("filesystem") == "safe"
    assert ps.classify_tool("shell") == "safe"
    assert ps.classify_tool("shell", "rm -rf /tmp") == "medium"
    assert ps.classify_tool("unknown_tool") == "medium"


def test_permission_confirmation():
    ps = PermissionSystem()
    assert ps.needs_confirmation("shell", "docker run") is True
    assert ps.needs_confirmation("filesystem", "read") is False


def test_command_validation():
    assert validate_command("ls -la") is None
    assert validate_command("rm -rf /") is not None
    assert validate_command("shutdown -h now") is not None
    assert validate_command("mkfs.ext4 /dev/sda") is not None
    assert validate_command("echo hello") is None


def test_path_validation():
    assert validate_path("/tmp") is None
    assert validate_path("/nonexistent_path_xyz_123") is not None


def test_audit_logger_creation():
    audit = AuditLogger()
    assert audit is not None
