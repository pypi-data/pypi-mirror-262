import logging
import os
from logging import Logger
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Optional, Dict, Any

from logging_loki import LokiHandler

class LokiLogger:
    """
    A class for setting up a logger that sends logs to a Loki server.
    """

    def __init__(self, app_name: str, is_debug: Optional[bool] = None, loki_url: Optional[str] = None) -> None:
        """
        Initializes the LokiLogger with the application name, debug flag, and Loki URL.
        If the debug flag is not provided, it will be read from the LOG_DEBUG environment variable.
        If the Loki URL is not provided, it will be read from the LOKI_URL environment variable.
        """
        self.app_name: str = app_name
        self.is_debug: bool = is_debug if is_debug is not None else os.getenv('LOG_DEBUG', 'False').lower() in ('true', '1')
        self.loki_url: str = loki_url if loki_url else os.getenv('LOKI_URL', 'http://localhost:3100')
        self.logger: Logger = self._setup_logger()

    def _setup_logger(self) -> Logger:
        """
        Sets up and returns a logger configured to send logs to Loki.
        """
        try:
            queue: Queue = Queue(-1)
            handler: QueueHandler = QueueHandler(queue)

            tags: Dict[str, str] = {"Application": self.app_name, "Environment": "Debug" if self.is_debug else "Production"}
            handler_loki: LokiHandler = LokiHandler(url=self.loki_url, tags=tags, version="1")

            listener: QueueListener = QueueListener(queue, handler_loki, respect_handler_level=True)
            listener.start()

            logger: Logger = logging.getLogger(self.app_name)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG if self.is_debug else logging.INFO)
            return logger
        except Exception as e:
            logging.error("Failed to set up Loki logger: %s", e)
            raise

    def _log(self, level: str, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """
        Generic logging method.
        """
        if tags is None:
            tags = {}
        else:
            tags = tags.copy()
        tags.update({"level": level})
        getattr(self.logger, level)(message, extra={"tags": tags})

    def info(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        self._log("info", message, tags)

    def debug(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        self._log("debug", message, tags)

    def warning(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        self._log("warning", message, tags)

    def error(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        self._log("error", message, tags)

    def critical(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        self._log("critical", message, tags)

    def shutdown(self) -> None:
        """
        Shuts down the logger and ensures all logs are flushed.
        """
        logging.shutdown()