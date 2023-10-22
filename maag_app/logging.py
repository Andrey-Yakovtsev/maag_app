import logging

import django
import json_log_formatter

from config.settings.base import BASE_DIR, DEBUG

LOG_DIR = BASE_DIR / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
SERVICE_NAME = "maag-om"


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra["message"] = message

        # Include builtins
        extra["level"] = record.levelname
        extra["name"] = record.name

        if "time" not in extra:
            extra["time"] = django.utils.timezone.now()

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "json_formatter": {(): CustomisedJSONFormatter()},
    },
    "handlers": {
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json_formatter",
            "filename": LOG_DIR / "maaglog.json",
            "maxBytes": 1024 * 1024 * 5,  # 5Mb
            "backupCount": 5,
        },
        "console": {
            "level": LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": True,
        }
    },
}

maag_logger = logging.config.dictConfig(LOGGING_CONFIG)
