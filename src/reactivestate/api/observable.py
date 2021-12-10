from typing import TypeVar

from reactivestate.core.action import action
from reactivestate.core.atom import ObservableAtom
from reactivestate.core.observablevalue import ObservableValue


T = TypeVar("T")


def observable(cls: T) -> T:
    def _setattr(self, name, value):
        if name in self.__dict__:
            assert action().is_active(), (
                f"Observable attributes can only be changed with actions. "
                f"Tried to change '{cls.__name__}.{name}'."
            )
            self.__dict__[name].set(value)
        else:
            self.__dict__[name] = ObservableValue(value)

    def _getattribute(self, name):
        obj = super(cls, self).__getattribute__(name)
        if isinstance(obj, ObservableAtom):
            return obj.get()
        else:
            return obj

    cls.__setattr__ = _setattr
    cls.__getattribute__ = _getattribute
    return cls
