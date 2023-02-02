import os
import sys

from loguru import logger

from core.config import get_settings


def setup_logger() -> None:
    logger.remove()
    log_format = "{time:YYYY-MM-DD at HH:mm:ss,SSS} | {level} | {file}:{function}:{line} | {message}"
    logger.add(sys.stderr, format=log_format, level=get_settings().log_level, enqueue=True)

    if get_settings().log_folder:
        logger.add(
            os.path.join(get_settings().log_folder, get_settings().log_file),
            format=log_format,
            rotation="10 MB",
            enqueue=True,
        )

    logger.info("Logger set upped..")
