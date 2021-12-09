import rx
from rx.subject.behaviorsubject import BehaviorSubject as RxBehaviorSubject

from reactivestate.core.tracking import (
    get_obs_dependency_changed,
    get_obs_dependency_stale,
    tracking,
)
from reactivestate.core.signals import SignalValue, Signal


class Computed:
    def __init__(self, fn):
        self.fn = fn
        self.name = None
        self.subscription = rx.never().subscribe()

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
        obs = obj.__dict__.get(self.name)
        if obs is None:
            obs = RxBehaviorSubject(SignalValue(Signal.STALE, None))
            obj.__dict__[self.name] = obs
            self.__compute__(obj)
        return obs

    def __compute__(self, obj):
        obs = obj.__dict__[self.name]
        oldvalue = obs.value.value
        with tracking() as t:
            newvalue = self.fn(obj)
            dependencies = t.get_dependencies()
        assert len(dependencies) > 0, (
            f"Computed prop must have at least one dependency. "
            f"Nothing was observed while running '{obj.__class__.__name__}.{self.name}'."
        )
        self.subscription.dispose()
        self.subscription = get_obs_dependency_stale(dependencies).subscribe(
            lambda v: obs.on_next(SignalValue(Signal.STALE, obs.value.value))
        )
        get_obs_dependency_changed(dependencies).subscribe(
            lambda v: self.__compute__(obj)
        )  # Subscription is disposed of automatically.
        if newvalue == oldvalue:
            # TODO: Comparer.
            obs.on_next(SignalValue(Signal.UNCHANGED, newvalue))
        else:
            obs.on_next(SignalValue(Signal.CHANGED, newvalue))

    def __set__(self, obj, value):
        raise RuntimeError(
            f"Computed props are read-only. "
            f"Tried to set '{obj.__class__.__name__}.{self.name}'."
        )


def computed(fn):
    return Computed(fn)
