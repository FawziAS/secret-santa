"""logging utilities."""

import logging
from enum import StrEnum, auto
from typing import Optional


class LoggingLevel(StrEnum):
    """App supported logging levels."""

    critical = auto()
    error = auto()
    warning = auto()
    info = auto()
    debug = auto()


LOGGING_LEVEL_TO_NUMBER: dict[LoggingLevel, int] = {
    LoggingLevel.critical: logging.CRITICAL,
    LoggingLevel.error: logging.ERROR,
    LoggingLevel.warning: logging.WARNING,
    LoggingLevel.info: logging.INFO,
    LoggingLevel.debug: logging.DEBUG,
}


def logging_level_to_number(log_level: LoggingLevel) -> int:
    """Logging level to number."""
    return logging.getLevelNamesMapping()[str(log_level).upper()]


class CustomLogFormatter(logging.Formatter):
    """A super class of ``logging.Formatter`` solemnly for custom log message formatting."""

    def format(self, record: logging.LogRecord) -> str:
        """Override ``logging.Formatter.format`` to add a custom log message format."""
        record.message = record.getMessage()
        location = f"{record.module}.{record.name}().{record.funcName}"
        msg = f'{f"[{record.levelname}]".ljust(10)} {location.ljust(39)} : {record.message}'
        record.msg = msg
        return super().format(record)


def get_common_handler() -> logging.Handler:
    """Initialize a ``logging.Handler`` with the custom formatting defined in ``LoggingUtils``.

    Returns:
        A logging handler with the custom formatter specified in LoggingUtils.

    """
    formatter = CustomLogFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


def get_logger(
    name: Optional[str] = None,
    handlers: Optional[list[logging.Handler]] = None,
    add_common_handler: bool = True,
) -> logging.Logger:
    """Get a logger named according to the ``name`` and attach the handlers passed from the caller to it.

    Args:
        name: The name of the logger to retrieve.
            In case the name is not specified, the root logger will be retrieved (Defaults to None).
        handlers: A list of handlers to attach to the logger retrieved (Defaults to None).
        add_common_handler: If True, the program's common handler will be attached to the logger retrieved
            (Defaults to True).

    Returns:
        The logger with the name of the ``name`` param, with the handlers passed attached to it.

    """
    # Retrieve the logger
    logger = logging.getLogger(name)
    # The logger's main logging level will be set by the root logger

    # If no handlers has been passed, set handlers to be an empty list
    if not handlers:
        handlers = []

    if add_common_handler:
        # Add the program's common handler
        handlers.append(get_common_handler())

    # Attach the handlers to the loggers
    for handler in handlers:
        logger.addHandler(handler)

    return logger
