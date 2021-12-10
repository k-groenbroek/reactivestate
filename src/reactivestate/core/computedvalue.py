from weakref import WeakSet

from reactivestate.core.atom import ObservableAtom
from reactivestate.core.tracking import tracking


class ComputedValue(ObservableAtom):
    def __init__(self, fn):
        super().__init__(None)
        self.fn = fn
        self.dependencies: WeakSet[ObservableAtom] = WeakSet()
        self.changed_confirmed = False
        self._compute()  # TODO: Wait until observed?

    def _compute(self):
        with tracking() as t:
            newvalue = self.fn()
            observed = t.get_observed()
        ObservableAtom.on_stale.disconnect(self._handle_dep_stale)
        ObservableAtom.on_ready.disconnect(self._handle_dep_ready)
        self.dependencies.clear()
        for d in observed:
            ObservableAtom.on_stale.connect(self._handle_dep_stale, d)
            ObservableAtom.on_ready.connect(self._handle_dep_ready, d)
            self.dependencies.add(d)
        self.set(newvalue)
        self.ready()

    def _handle_dep_stale(self, *args):
        self.set(self.value)

    def _handle_dep_ready(self, *args, changed: bool):
        self.changed_confirmed |= changed
        if any(d.stale for d in self.dependencies):
            return
        if self.changed_confirmed:
            self._compute()
        else:
            self.ready()
        self.changed_confirmed = False
