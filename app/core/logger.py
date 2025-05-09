"""
Implementation of the LogSetupper class.
The logger is configured using the value of the ENV environment variable.
"""

import atexit
import datetime as dt
import json
import logging.config
import os
import pathlib
import traceback
from typing import override

from app.middlewares.request_id_middleware import correlation_id

LOCAL_DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


def setup_logging() -> None:
    config_file = pathlib.Path("./app/log_config.json")
    with open(config_file, "r") as f_in:
        config = json.load(f_in)

    if os.environ.get("ENVIRONMENT") == "local":
        config["handlers"]["queue_handler"]["handlers"] = ["stdout_local"]
    else:
        config["handlers"]["queue_handler"]["handlers"] = ["stdout_cloud"]

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore


class SimpleFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord):
        extra_labels = getattr(record, "extra_labels", {})
        return "[{timestamp}] [{request_id}] {level}: {msg} ({filename}:{lineno}) {extra}".format(
            timestamp=dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).strftime(LOCAL_DATETIME_FORMAT_STRING),
            request_id=record.request_id,  # type: ignore
            level=record.levelname,
            msg=record.getMessage(),
            filename=record.filename,
            lineno=record.lineno,
            extra="--- Extra: {}".format(json.dumps(extra_labels))
            if extra_labels
            else "",
        )


class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        # Handle exception info if present
        exc_text = None
        if record.exc_info:
            # Don't let parent formatter add exception to message
            exc_text = self.formatException(record.exc_info)
            # This is important - save original message
            record.exc_text = exc_text

        # Prepare the log dict with the original message
        message_dict = self._prepare_log_dict(record)
        return json.dumps(message_dict, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": f"{record.levelname.upper()} --- {record.funcName}:{record.lineno} - {record.getMessage()} ({record.filename})",
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)
            always_fields["traceback"] = "".join(
                traceback.format_exception(*record.exc_info)
            )

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = correlation_id.get()
        return True
