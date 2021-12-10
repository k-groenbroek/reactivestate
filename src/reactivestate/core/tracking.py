import threading
from collections import deque
from typing import Deque, Set

from reactivestate.core.atom import ObservableAtom


class TrackingContextManager:
    def __init__(self):
        self.observed: Deque[Set[ObservableAtom]] = deque()

    def __enter__(self):
        if not self.observed:
            ObservableAtom.on_observed.connect(self._add_observed)
        self.observed.append(set())
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.observed.pop()
        if not self.observed:
            ObservableAtom.on_observed.disconnect(self._add_observed)

    def _add_observed(self, v: ObservableAtom):
        self.observed[-1].add(v)

    def is_active(self):
        return len(self.observed) > 0

    def get_observed(self):
        return self.observed[-1]


local = threading.local()
local.tracking = TrackingContextManager()


def tracking() -> TrackingContextManager:
    return local.tracking
