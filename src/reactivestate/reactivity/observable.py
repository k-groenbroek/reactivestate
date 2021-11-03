from typing import TypeVar
from rx.subject import BehaviorSubject as RxBehaviorSubject

from reactivestate.core.tracking import tracking
from reactivestate.core.action import action


T = TypeVar("T")


def observable(cls: T) -> T:
    def _setattr(self, name, value):
        if name in self.__dict__:
            assert action().is_active(), (
                f"Observable attributes can only be changed with actions. "
                f"Tried to change '{cls.__name__}.{name}'."
            )
            self.__dict__[name].on_next(value)
        else:
            self.__dict__[name] = RxBehaviorSubject(value)

    def _getattribute(self, name):
        obj = super(cls, self).__getattribute__(name)
        if isinstance(obj, RxBehaviorSubject):
            tracking().report_observed(obj)
            return obj.value
        else:
            return obj

    cls.__setattr__ = _setattr
    cls.__getattribute__ = _getattribute
    return cls
