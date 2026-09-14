# src/utils/logger.py
import logging
import sys

from prefect.logging.handlers import APILogHandler
from pythonjsonlogger import jsonlogger


def _setup_app_logger() -> logging.Logger:
    app_logger = logging.getLogger("app")

    if not app_logger.handlers:
        # Output clean JSON to terminal/stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(module)s %(lineno)d %(message)s"
        )
        stream_handler.setFormatter(formatter)
        app_logger.addHandler(stream_handler)

        # Forward logs directly to Prefect server / UI
        app_logger.addHandler(APILogHandler())

        app_logger.setLevel(logging.INFO)

        # Prevent propagating to root logger to eliminate duplicate console logs
        app_logger.propagate = False

    return app_logger


logger = _setup_app_logger()

# prefect config set PREFECT_LOGGING_EXTRA_LOGGERS="['app']"

# prefect config set PREFECT_LOGGING_TO_SERIALIZED="true"
