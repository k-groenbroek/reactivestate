from reactivestate.core.computedvalue import ComputedValue
from reactivestate.core.tracking import tracking


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
