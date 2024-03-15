import logging
from logging import Logger
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Optional, Dict, Any

from logging_loki import LokiHandler



class IBBCoreLogger:
    """
    A class for setting up a logger that sends logs to a Loki server.
    
    Attributes:
        LOKI_URL (str): The URL of the Loki server to send logs to.
        app_name (str): The name of the application using the logger.
        is_debug (bool): Flag indicating if the logger is in debug mode.
        logger (Logger): The configured logger instance.
    """

    def __init__(self, APP_NAME: str, IS_DEBUG: bool, LOKI_URL: str):
        """
        Initializes the CoreLogger with the application name and debug flag.
        
        Parameters:
            APP_NAME (str): The name of the application.
            IS_DEBUG (bool): True if debug logging is enabled, False otherwise.
        """
        self.app_name: str = APP_NAME
        self.is_debug: bool = IS_DEBUG
        self.LOKI_URL: str = LOKI_URL
        self.logger: Logger = self._setup_logger()

    def _setup_logger(self) -> Logger:
        """
        Sets up and returns a logger configured to send logs to Loki.
        
        Returns:
            Logger: The configured logger instance.
        """
        queue: Queue = Queue(-1)
        handler: QueueHandler = QueueHandler(queue)

        tags: Dict[str, str] = {"Application": self.app_name, "Environment": "Debug" if self.is_debug else "Production"}
        handler_loki: LokiHandler = LokiHandler(url=self.LOKI_URL, tags=tags, version="1")

        listener: QueueListener = QueueListener(queue, handler_loki)
        listener.start()

        logger: Logger = logging.getLogger(self.app_name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if self.is_debug else logging.INFO)
        return logger

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs an informational message."""
        self.logger.info(message, extra=extra)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs a debug message."""
        self.logger.debug(message, extra=extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs a warning message."""
        self.logger.warning(message, extra=extra)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs an error message."""
        self.logger.error(message, extra=extra)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs a critical message."""
        self.logger.critical(message, extra=extra)