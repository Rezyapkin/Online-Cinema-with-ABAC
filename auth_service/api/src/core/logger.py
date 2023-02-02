import logging
import sys
from pathlib import Path

from flask import Flask
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def configure_logger(application: Flask, log_level: str, log_folder: Path | None = None):
    log_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{function}:{line} | {message}"
    logger.add(sys.stderr, level=log_level)
    if log_folder:
        logger.add(
            log_folder / "log.log",
            format=log_format,
            level=log_level,
            rotation="10 MB",
        )

    application.logger.addHandler(InterceptHandler())
