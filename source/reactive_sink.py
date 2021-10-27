from typing import Callable

from source.core.tracking import tracking
from source.core.action import action


class ReactiveSink:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.subscription = None
        self.__call__()

    def __call__(self):
        with tracking() as t:
            self.fn()
            obs = t.get_observed()
        assert obs is not None, (
            f"ReactiveSink must have at least one dependency. "
            f"Nothing was observed while running '{self.fn.__name__}'."
        )
        self.subscription = obs.subscribe(lambda v: self._invalidate())

    def _invalidate(self):
        self.subscription.dispose()
        action().report_dirty_sink(self)


def reactive_sink(fn: Callable[[], None]) -> Callable[[], None]:
    return ReactiveSink(fn)
