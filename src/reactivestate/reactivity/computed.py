from rx.subject.behaviorsubject import BehaviorSubject as RxBehaviorSubject

from reactivestate.core.tracking import tracking


DIRTY = object()


class Computed:
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
        obsvalue = obj.__dict__.get(self.name)
        if obsvalue is None:
            obsvalue = RxBehaviorSubject(DIRTY)
            obj.__dict__[self.name] = obsvalue
        if obsvalue.value is DIRTY:
            with tracking() as t:
                obsvalue.on_next(self.fn(obj))
                obsdependency = t.get_observed()
            obsdependency[0].subscribe(
                lambda v: obsvalue.on_next(DIRTY)
            )  # Subscription is disposed of automatically.
        return obsvalue

    def __set__(self, obj, value):
        raise RuntimeError(
            f"Computed props are read-only. "
            f"Tried to set '{obj.__class__.__name__}.{self.name}'."
        )


def computed(fn):
    return Computed(fn)
