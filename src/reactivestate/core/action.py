import threading
from typing import Callable


class ActionContextManager:
    def __init__(self):
        self.counter = 0
        self.dirty_sinks = set()

    def __enter__(self):
        self.counter += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.counter -= 1
        if self.counter == 0:
            self.flush_sinks()

    def is_active(self):
        return self.counter > 0

    def report_dirty_sink(self, sink: Callable):
        self.dirty_sinks.add(sink)

    def flush_sinks(self):
        for sink in self.dirty_sinks:
            sink()
        self.dirty_sinks.clear()


local = threading.local()
local.action = ActionContextManager()


def action() -> ActionContextManager:
    return local.action
