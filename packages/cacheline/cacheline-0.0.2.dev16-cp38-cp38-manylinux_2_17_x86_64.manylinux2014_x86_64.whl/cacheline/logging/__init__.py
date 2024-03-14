import atexit
import logging
import multiprocessing
import queue
import sys
import time
from typing import Callable, Optional
from urllib.parse import quote, urljoin

import colorlog
import requests
from pythonjsonlogger import jsonlogger

if sys.version_info >= (3, 12) and ("taskName" not in jsonlogger.RESERVED_ATTRS):
    jsonlogger.RESERVED_ATTRS = ("taskName", *jsonlogger.RESERVED_ATTRS)


_DEFAULT_FORMAT = "%(asctime)s %(name)s %(levelname)s %(process)d %(thread)d %(filename)s %(funcName)s %(levelno)s"
_COLOR_FORMATTER = colorlog.ColoredFormatter(
    "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s %(reset)s%(pathname)s:%(lineno)d ",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={
        "message": {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        }
    },
    style="%",
)


def getLogger(
    name: str,
    *,
    format_str: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
):
    _logger = logging.getLogger(name)
    _logger.propagate = False
    if handler is None:
        handler = logging.StreamHandler(sys.stderr)
        formatter = (
            _COLOR_FORMATTER if format_str is None else logging.Formatter(format_str)
        )
        handler.setFormatter(formatter)
    else:
        if format_str is not None:
            formatter = jsonlogger.JsonFormatter(format_str)
            handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


logger = getLogger(
    "cacheline.logging",
)


class LoggerLauncher(logging.Handler):
    def __init__(self, push_function: Callable[[str], None]):
        super().__init__()
        self._push_function = push_function

    def emit(self, record):
        self._push_function(self.format(record))

    def getLogger(self, name: str):
        _logger = getLogger(name, handler=self, format_str=_DEFAULT_FORMAT)
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(_COLOR_FORMATTER)
        _logger.addHandler(stream_handler)
        return _logger


def consumer(queue, server, key):
    while True:
        item = queue.get()
        try:
            requests.get(
                urljoin(server, f"LPUSH/{key}/{quote(item)}"),
                timeout=3,
            )
        except requests.RequestException as err:
            logger.exception("Failed to push log to webdis, error: %s", err)


class WebdisLoggerLauncher(LoggerLauncher):
    def __init__(self, server: str, key: str, queue_size=4096, timeout=3):
        super().__init__(self.push)
        self._url = server
        self._key = quote(key)
        self._timeout = timeout
        _queue = multiprocessing.Queue(queue_size)
        self._queue = _queue

        self._process = multiprocessing.Process(
            target=consumer, args=(_queue, server, key)
        )
        self._process.start()

        def wait_finish():
            while not self._queue.empty() and self._process.is_alive():
                time.sleep(1)
                logger.info("Waiting for consumer")
            self._process.terminate()

        atexit.register(wait_finish)

    def push(self, row: str):
        try:
            self._queue.put(row, timeout=self._timeout)
        except queue.Full:
            logger.exception(
                "Failed to push log to webdis, queue is full, dropping log %s", row
            )
