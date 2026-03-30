from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from file_manager.config.settings import AppSettings


LOGGER_NAMES = [
    "app",
    "scan",
    "duplicates",
    "transfer",
    "ml",
    "archive",
    "errors",
]


def _build_handler(log_file: Path, level: int, max_bytes: int, backup_count: int) -> RotatingFileHandler:
    handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s | %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler


def setup_logging(settings: AppSettings) -> None:
    settings.log.log_dir.mkdir(parents=True, exist_ok=True)
    level = getattr(logging, settings.log.log_level.upper(), logging.INFO)

    for logger_name in LOGGER_NAMES:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.propagate = False
        if logger.handlers:
            continue
        handler = _build_handler(
            settings.log.log_dir / f"{logger_name}.log",
            level,
            settings.log.max_bytes,
            settings.log.backup_count,
        )
        logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
