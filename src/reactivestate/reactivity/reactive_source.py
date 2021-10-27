from typing import TypeVar
from rx.subject import BehaviorSubject

from reactivestate.core.tracking import tracking
from reactivestate.core.action import action


T = TypeVar("T")


def reactive_source(cls: T) -> T:
    class ReactiveSource(cls):
        def __setattr__(self, name, value):
            if name in self.__dict__:
                assert action().is_active(), (
                    f"ReactiveSource attributes can only be changed with actions. "
                    f"Tried to change '{cls.__name__}.{name}'."
                )
                self.__dict__[name].on_next(value)
            else:
                self.__dict__[name] = BehaviorSubject(value)

        def __getattribute__(self, name):
            obj = super().__getattribute__(name)
            if isinstance(obj, BehaviorSubject):
                tracking().report_observed(obj)
                return obj.value
            else:
                return obj

    return ReactiveSource
