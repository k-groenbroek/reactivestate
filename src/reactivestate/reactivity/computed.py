from rx.subject.behaviorsubject import BehaviorSubject as RxBehaviorSubject

from reactivestate.core.tracking import tracking


DIRTY = object()


class Computed:
    def __init__(self, fn):
        self.fn = fn
        self.obsvalue = RxBehaviorSubject(DIRTY)
        self.subscription = None

    def __set_name__(self, owner, name):
        self.propname = f"{owner.__name__}.{name}"

    def __get__(self, obj, type=None):
        assert tracking().is_active(), (
            f"Computed prop cannot be accessed outside of reactive context. "
            f"Tried to access '{self.propname}'."
        )
        if self.obsvalue.value is DIRTY:
            with tracking() as t:
                self.obsvalue.on_next(self.fn(obj))
                obs = t.get_observed()
            self.subscription = obs.subscribe(lambda v: self._invalidate())
            self.dirty = False
        return self.obsvalue

    def _invalidate(self):
        self.subscription.dispose()
        self.obsvalue.on_next(DIRTY)


def computed(fn):
    return Computed(fn)