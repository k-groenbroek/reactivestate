from enum import Enum, auto
from typing import Any, NamedTuple


class Signal(Enum):
    STALE = auto()
    UNCHANGED = auto()
    CHANGED = auto()


class SignalValue(NamedTuple):
    signal: Signal
    value: Any
