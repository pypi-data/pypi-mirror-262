import logging
import time

import pytest
from test_utils import CunstomHandler

import aglog.handler.queue_listener_handler as target
from aglog.loader.loader import load_dict_config


class DummyHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.call_count = 0

    def emit(self: "DummyHandler", record: logging.LogRecord) -> None:
        self.call_count += 1


def test_queue_handler_listener():
    logger = logging.getLogger("test")
    dummy_handler = DummyHandler()
    lister = target.QueueListenerHandler(handlers=[dummy_handler], stop_timeout=0.1)
    lister.start()

    logger.addHandler(lister)
    logger.error("test")
    logger.error("test")
    lister.stop()

    assert dummy_handler.call_count == 2


def test_queue_handler_listener_with_uninitialized_handler_in_handlers():
    with pytest.raises(ValueError, match="Handler"):
        target.QueueListenerHandler(handlers=["uninitialized_handler"], stop_timeout=0.1)


def test_dict_config_queue_handler_listener():
    config = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s %(name)s [%(levelname)s]: %(message)s",
            },
        },
        "handlers": {
            "custom_handler": {
                "()": "test_utils.CunstomHandler",
                "x": 1,
                "formatter": "simple",
            },
            "default_handler": {
                "class": "logging.NullHandler",
                "formatter": "simple",
            },
            "z_queue_listener_handler": {
                "()": "aglog.handler.queue_listener_handler.QueueListenerHandler",
                "handlers": [
                    "custom_handler",
                    "default_handler",
                ],
            },
        },
        "loggers": {
            "test_dict_config_queue_listener_handler": {
                "handlers": ["z_queue_listener_handler", "custom_handler"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
    load_dict_config(config)
    logger = logging.getLogger("test_dict_config_queue_listener_handler")
    logger.info("test message")

    time.sleep(0.001)

    queue_listener = logger.handlers[0]
    assert isinstance(queue_listener, target.QueueListenerHandler)
    custom_handler_in_queue = queue_listener.handlers[0]
    assert isinstance(custom_handler_in_queue, CunstomHandler)
    assert custom_handler_in_queue.call_count == 2
    assert custom_handler_in_queue.formatter is not None
    assert custom_handler_in_queue.formatter._fmt == "%(asctime)s %(name)s [%(levelname)s]: %(message)s"

    custom_handler = logger.handlers[1]
    assert isinstance(custom_handler, CunstomHandler)
    assert custom_handler_in_queue is custom_handler
