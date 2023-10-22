import logging
import socket

import json_log_formatter
from django.utils import timezone


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra["message"] = message

        # Include builtins
        extra["level"] = record.levelname
        extra["name"] = record.name

        if "time" not in extra:
            extra["time"] = timezone.now()

        if "service" not in extra:
            extra["service"] = "maag-om"

        if "hostname" not in extra:
            extra["hostname"] = socket.gethostname()

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
