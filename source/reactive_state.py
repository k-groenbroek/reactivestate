from typing import TypeVar
from rx.subject import BehaviorSubject

from source.core.tracking import report_observed
from source.core.action import action


T = TypeVar("T")


def reactive(cls: T) -> T:
    class ReactiveState(cls):
        def __setattr__(self, name, value):
            if name in self.__dict__:
                assert action().in_action(), (
                    f"ReactiveState attributes can only be changed with actions. "
                    f"Tried to change '{cls.__name__}.{name}'."
                )
                self.__dict__[name].on_next(value)
            else:
                self.__dict__[name] = BehaviorSubject(value)

        def __getattribute__(self, name):
            obj = super().__getattribute__(name)
            if not isinstance(obj, BehaviorSubject):
                return obj
            else:
                report_observed(obj)
                return obj.value

    return ReactiveState
