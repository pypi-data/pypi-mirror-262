import atexit
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from typing_extensions import Self


class AutoStartQueueListener(QueueListener):
    def __init__(self: Self, queue: Queue, *handlers: logging.Handler, respect_handler_level: bool = False) -> None:
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        self.start()


class QueueListenerHandler(QueueHandler):
    def __init__(  # noqa: PLR0913
        self: Self,
        handlers: list[logging.Handler] | list[str],
        *,
        auto_run: bool = True,
        max_queue_size: int = -1,
        stop_timeout: float = 60,
        respect_handler_level: bool = False,
    ) -> None:
        self.stop_timeout = stop_timeout
        self.queue = Queue(maxsize=max_queue_size)
        self.handlers: list[logging.Handler] = []
        for h in handlers:
            if isinstance(h, str):
                handler = logging._handlers.get(h)  # noqa: SLF001 # pyright: ignore[reportAttributeAccessIssue]
                if handler is None:
                    msg = f"Handler `{h}` not found. Sometimes, renaming QueueHandlerListener in lexicographical order to be later can solve the issue."
                    raise ValueError(msg)
                self.handlers.append(handler)
            else:
                self.handlers.append(h)

        super().__init__(self.queue)
        Listener = AutoStartQueueListener if auto_run else QueueListener  # noqa: N806
        self.listener = Listener(self.queue, *self.handlers, respect_handler_level=respect_handler_level)
        atexit.register(self.stop)

    def start(self: Self) -> None:
        self.listener.start()

    def stop(self: Self) -> None:
        self.listener.enqueue_sentinel()
        thread = self.listener._thread  # noqa: SLF001
        if thread is not None:
            thread.join(timeout=self.stop_timeout)
            self.listener._thread = None  # noqa: SLF001
