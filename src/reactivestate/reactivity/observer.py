from typing import Callable

from reactivestate.core.tracking import get_obs_dependency_changed, tracking


class Observer:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.__call__()

    def __call__(self):
        with tracking() as t:
            self.fn()
            dependencies = t.get_dependencies()
        assert len(dependencies) > 0, (
            f"Observer must have at least one dependency. "
            f"Nothing was observed while running '{self.fn.__name__}'."
        )
        obs = get_obs_dependency_changed(dependencies)
        obs.subscribe(lambda v: self())  # Subscription is disposed of automatically.


def observe(fn: Callable[[], None]) -> Callable[[], None]:
    return Observer(fn)
