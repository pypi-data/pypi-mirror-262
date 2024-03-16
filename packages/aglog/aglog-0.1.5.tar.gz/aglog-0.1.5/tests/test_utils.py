import logging
import os
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def temporary_env_var(key: str, value: str) -> Generator:
    original_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if original_value is None:
            del os.environ[key]
        else:
            os.environ[key] = original_value


class CunstomHandler(logging.Handler):
    def __init__(self, x: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.call_count = 0

    def emit(self, record: logging.LogRecord) -> None:
        self.call_count += 1
