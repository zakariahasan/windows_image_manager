from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from file_manager.config.settings import AppSettings


def load_settings() -> AppSettings:
    load_dotenv()
    settings = AppSettings()

    log_dir = os.getenv("FM_LOG_DIR")
    if log_dir:
        settings.log.log_dir = Path(log_dir)

    output_dir = os.getenv("FM_OUTPUT_DIR")
    if output_dir:
        settings.output_dir = Path(output_dir)

    temp_dir = os.getenv("FM_TEMP_DIR")
    if temp_dir:
        settings.temp_dir = Path(temp_dir)

    log_level = os.getenv("FM_LOG_LEVEL")
    if log_level:
        settings.log.log_level = log_level.upper()

    model_dir = os.getenv("FM_MODEL_DIR")
    if model_dir:
        settings.ml.model_dir = Path(model_dir)

    return settings
