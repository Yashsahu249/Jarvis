import logging
import sys
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class JarvisLogger:
    _instances: dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str, level: str | None = None) -> logging.Logger:
        if name in cls._instances:
            return cls._instances[name]

        logger = logging.getLogger(name)
        logger.setLevel(level or "DEBUG")

        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        fh = logging.FileHandler(log_dir / f"{name.replace('.', '_')}.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        cls._instances[name] = logger
        return logger
