from datetime import datetime

from jarvis.utils.logger import JarvisLogger


class AuditLogger:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("safety.audit")

    def log_execution(
        self,
        tool: str,
        action: str,
        user: str = "user",
        status: str = "executed",
        details: str = "",
    ):
        self.logger.info(
            f"AUDIT|{tool}|{action}|{status}|{user}|{details}"
        )

    def log_permission_denied(
        self, tool: str, action: str, reason: str, user: str = "user"
    ):
        self.logger.warning(
            f"AUDIT|DENIED|{tool}|{action}|{reason}|{user}"
        )
