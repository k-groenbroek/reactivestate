from weakref import WeakSet
from typing import Callable

from reactivestate.core.tracking import tracking
from reactivestate.core.atom import ObservableAtom


class Observer:
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn
        self.dependencies: WeakSet[ObservableAtom] = WeakSet()
        self.change_confirmed = False
        self.__call__()

    def __call__(self):
        with tracking() as t:
            self.fn()
            observed = t.get_observed()
        assert len(observed) > 0, (
            f"Observer must have at least one dependency. "
            f"Nothing was observed while running '{self.fn.__name__}'."
        )
        ObservableAtom.on_ready.disconnect(self._handle_dep_ready)
        self.dependencies.clear()
        for d in observed:
            ObservableAtom.on_ready.connect(self._handle_dep_ready, d, weak=False)
            self.dependencies.add(d)

    def _handle_dep_ready(self, *args, changed: bool):
        self.change_confirmed |= changed
        if any(d.stale for d in self.dependencies):
            return
        if self.change_confirmed:
            self.__call__()
            self.change_confirmed = False
