import threading
from collections import deque

from rx import Observable


class TrackingContextManager:
    def __init__(self):
        self.tracked_observables = deque()

    def __enter__(self):
        self.tracked_observables.append(set())
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tracked_observables.pop()

    def report_observed(self, obs: Observable):
        try:
            self.tracked_observables[-1].add(obs)
        except IndexError:
            # Nothing is currently being tracked.
            pass

    def get_observed(self) -> set[Observable]:
        return self.tracked_observables[-1]


local = threading.local()
local.tracking = TrackingContextManager()


def tracking() -> TrackingContextManager:
    return local.tracking


def report_observed(obs: Observable):
    local.tracking.report_observed(obs)
