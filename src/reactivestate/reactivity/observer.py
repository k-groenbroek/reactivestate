from typing import Callable

from reactivestate.core.tracking import tracking
from reactivestate.core.action import action


class Observer:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.__call__()

    def __call__(self):
        with tracking() as t:
            self.fn()
            obsdependency = t.get_observed()
        assert obsdependency is not None, (
            f"Observer must have at least one dependency. "
            f"Nothing was observed while running '{self.fn.__name__}'."
        )
        obsdependency.subscribe(
            lambda v: action().report_dirty_sink(self)
        )  # Subscription is disposed of automatically.


def observe(fn: Callable[[], None]) -> Callable[[], None]:
    return Observer(fn)
