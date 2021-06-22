from typing import Callable, Any

from rx.subject import BehaviorSubject

from source.core.tracking import tracking
from source.core.action import combine_action


class Autorun:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.subscription = None

    def __call__(self):
        if self.subscription is not None:
            self.subscription.dispose()
        with tracking() as t:
            result = self.fn()
            dependencies = t.get_observed()
        # TODO: Comparer.
        obs = combine_action()(dependencies)
        self.subscription = obs.subscribe(lambda v: self())
        return result


NOT_COMPUTED = object()


class ComputedValue:
    def __init__(self, fn: Callable[[], Any]):
        self.fn = fn
        self.subscription = None
        self.obs_value = BehaviorSubject(NOT_COMPUTED)

    def compute(self):
        if self.subscription is not None:
            self.subscription.dispose()
        with tracking() as t:
            result = self.fn()
            dependencies = t.get_observed()
        # self.subscription = ??
        self.obs_value.on_next(result)

    def __get__(self):
        # report observed.
        return self.obs_value.value
