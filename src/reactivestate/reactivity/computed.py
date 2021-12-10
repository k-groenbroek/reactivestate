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


class ComputedDescriptor:
    def __init__(self, fn):
        self.fn = fn
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None):
        assert self.name is not None, (
            f"Computed prop cannot be assigned after class instantiation. "
            f"Check the computed props on '{obj.__class__.__name__}'."
        )
        assert tracking().is_active(), (
            f"Computed prop cannot be accessed outside of reactive context. "
            f"Tried to access '{obj.__class__.__name__}.{self.name}'."
        )
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = ComputedValue(lambda: self.fn(obj))
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        raise RuntimeError(
            f"Computed props are read-only. "
            f"Tried to set '{obj.__class__.__name__}.{self.name}'."
        )


def computed(fn):
    return ComputedDescriptor(fn)
