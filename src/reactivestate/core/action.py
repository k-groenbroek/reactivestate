import threading
from typing import Any, Callable, Dict, Set, Tuple

from rx.subject import BehaviorSubject as RxBehaviorSubject
from reactivestate.core.signals import Signal, SignalValue


class ActionContextManager:
    def __init__(self):
        self.counter = 0
        self.state_changes: Dict[RxBehaviorSubject, Any] = {}

    def __enter__(self):
        self.counter += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.counter -= 1
        if self.counter == 0:
            self.flush_state_changes()

    def is_active(self):
        return self.counter > 0

    def report_stale(self, obs: RxBehaviorSubject):
        if obs not in self.state_changes:
            oldvalue = obs.value.value
            self.state_changes[obs] = oldvalue

    def flush_state_changes(self):
        for obs, oldvalue in self.state_changes.items():
            newvalue = obs.value.value
            # TODO: Comparators.
            if newvalue == oldvalue:
                obs.on_next(SignalValue(Signal.UNCHANGED, newvalue))
            else:
                obs.on_next(SignalValue(Signal.CHANGED, newvalue))
        self.state_changes.clear()


local = threading.local()
local.action = ActionContextManager()


def action() -> ActionContextManager:
    return local.action
