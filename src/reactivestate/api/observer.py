from typing import Callable

from reactivestate.core.observer import Observer


def observer(fn: Callable[[], None]) -> Callable[[], None]:
    return Observer(fn)
