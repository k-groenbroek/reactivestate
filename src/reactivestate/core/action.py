import threading
from blinker import Signal


class ActionContextManager:
    on_exit = Signal()

    def __init__(self):
        self.counter = 0

    def __enter__(self):
        self.counter += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.counter -= 1
        if self.counter == 0:
            self.on_exit.send(self)

    def is_active(self):
        return self.counter > 0


local = threading.local()
local.action = ActionContextManager()


def action() -> ActionContextManager:
    return local.action
