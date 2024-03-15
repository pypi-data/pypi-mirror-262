import logging
from logging import Logger
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Optional, Dict, Any

from logging_loki import LokiHandler

class CreateLogger:
    """
    A class for setting up a logger that sends logs to a Loki server.
    
    Attributes:
        app_name (str): The name of the application using the logger.
        is_debug (bool): Flag indicating if the logger is in debug mode.
        loki_url (str): The URL of the Loki server to send logs to.
        logger (Logger): The configured logger instance.
    """

    def __init__(self, app_name: str, is_debug: bool, loki_url: str) -> None:
        """
        Initializes the LokiLogger with the application name, debug flag, and Loki URL.
        
        Parameters:
            app_name (str): The name of the application.
            is_debug (bool): True if debug logging is enabled, False otherwise.
            loki_url (str): The URL of the Loki server to send logs to.
        """
        self.app_name: str = app_name
        self.is_debug: bool = is_debug
        self.loki_url: str = loki_url
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
        handler_loki: LokiHandler = LokiHandler(url=self.loki_url, tags=tags, version="1")

        listener: QueueListener = QueueListener(queue, handler_loki)
        listener.start()

        logger: Logger = logging.getLogger(self.app_name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if self.is_debug else logging.INFO)
        return logger

    def info(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """Logs an informational message."""
        self.logger.info(message, extra={"tags": tags})

    def debug(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """Logs a debug message."""
        self.logger.debug(message, extra={"tags": tags})

    def warning(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """Logs a warning message."""
        self.logger.warning(message, extra={"tags": tags})

    def error(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """Logs an error message."""
        self.logger.error(message, extra={"tags": tags})

    def critical(self, message: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """Logs a critical message."""
        self.logger.critical(message, extra={"tags": tags})