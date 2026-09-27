import logging
import os
import sys
from pathlib import Path

from prefect.logging.formatters import JsonFormatter, PrefectFormatter
from prefect.logging.handlers import (
    APILogHandler,
    PrefectConsoleHandler,
)

from core.config import settings

LOG_STYLE = {
    "log.info_level": "cyan",
    "log.warning_level": "yellow3",
    "log.error_level": "red3",
    "log.critical_level": "bright_red",
    "log.completed_state": "green",
    "log.failed_state": "red3",
    "log.flow_name": "bold magenta",
}


# Configurable Log Level (Env var > Settings > Default INFO)
def resolve_log_level(level_name: str | None = None) -> int:
    """Resolve a user-provided log level safely."""
    candidate = (
        level_name
        or os.getenv("LOG_LEVEL")
        or getattr(settings, "log_level", "INFO")
    ).upper()

    level = logging.getLevelNamesMapping().get(candidate)

    if level is None:
        raise ValueError(
            f"Invalid LOG_LEVEL={candidate!r}. "
            "Expected DEBUG, INFO, WARNING, ERROR, CRITICAL, or a valid logging level."
        )

    return level


def setup_logger(
    name: str = settings.app_name,
    level: str | None = None,
    force_reconfigure: bool = False,
) -> logging.Logger:
    """Configures and returns a context-aware logger.

    Args:
        name: Logger name (supports sub-names like f"{settings.app_name}.db").
        level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
        force_reconfigure: If True, resets existing handlers (useful in unit tests).
    """
    app_logger = logging.getLogger(name)

    app_logger.setLevel(resolve_log_level(level))
    app_logger.propagate = False

    # Allow tests or reloading processes to reset state cleanly
    if force_reconfigure:
        app_logger.handlers.clear()

    # 1. UI Handler (APILogHandler) - only add if absent
    if not any(
        isinstance(handler, APILogHandler)
        for handler in app_logger.handlers
    ):
        app_logger.addHandler(APILogHandler())

    # 2. Console Handler (PrefectConsoleHandler) - only add if absent
    if not any(
        isinstance(handler, PrefectConsoleHandler)
        for handler in app_logger.handlers
    ):
        formatter_mode = os.getenv(
            "PREFECT_LOGGING_HANDLERS_CONSOLE_FORMATTER",
            "standard"
        ).lower()

        if formatter_mode == "json":
            # Empty styles for pure, clean JSON (no ANSI escape codes)
            console_handler = PrefectConsoleHandler(
                stream=sys.stderr,
                styles={}
            )

            # JsonFormatter expect value in fmt, dmft, style
            console_handler.setFormatter(
                JsonFormatter("default", "%Y-%m-%d %H:%M:%S", "%")
            )
        else:
            # Colorized Rich styles for terminal development
            console_handler = PrefectConsoleHandler(
                stream=sys.stderr,
                styles=LOG_STYLE
            )

            console_handler.setFormatter(
                PrefectFormatter(
                    format="%(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s - %(message)s",
                    datefmt="%H:%M:%S",
                )
            )

        app_logger.addHandler(console_handler)

    return app_logger


# Shared application logger
logger = setup_logger()


def get_logger(module_name: str | None = None) -> logging.Logger:
    """Returns a module-scoped child logger under settings.app_name."""
    if not module_name or module_name == "__main__":
        # Fallback: resolve real filename if run as the entrypoint
        main_file = Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else None
        module_name = main_file if main_file else None

    if not module_name:
        return logger

    scoped_name = f"{settings.app_name}.{module_name}"

    child_logger = logging.getLogger(scoped_name)

    # Child loggers must propagate to parent so the root handlers process the records
    child_logger.propagate = True

    return child_logger


def get_logger_(module_name: str | None = None) -> logging.Logger:
    """Returns a module-scoped child logger under settings.app_name.

    If module_name is omitted, it automatically inspects the caller's frame.
    """
    if module_name is None:
        # Inspect caller's module name automatically
        caller_frame = sys._getframe(1)
        module_name = caller_frame.f_globals.get("__name__", "app")

    if module_name == "__main__":
        main_file = Path(sys.argv[0]).stem if sys.argv and sys.argv[0] else None
        module_name = main_file if main_file else "app"

    scoped_name = f"{settings.app_name}.{module_name}"
    child_logger = logging.getLogger(scoped_name)
    child_logger.propagate = True

    return child_logger
