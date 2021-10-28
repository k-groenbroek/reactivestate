import threading
from collections import deque

import rx


class TrackingContextManager:
    def __init__(self):
        self.tracked_observables = deque()

    def __enter__(self):
        self.tracked_observables.append(set())
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tracked_observables.pop()

    def is_active(self):
        return len(self.tracked_observables) > 0

    def report_observed(self, obs: rx.Observable):
        try:
            self.tracked_observables[-1].add(obs)
        except IndexError:
            # Nothing is currently being tracked.
            pass

    def get_observed(self) -> rx.Observable:
        dependencies = self.tracked_observables[-1]
        if len(dependencies) == 0:
            return None
        obs = rx.combine_latest(*dependencies)
        obs = obs[1:]
        return obs


local = threading.local()
local.tracking = TrackingContextManager()


def tracking() -> TrackingContextManager:
    return local.tracking
