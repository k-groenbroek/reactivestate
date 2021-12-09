import threading
from collections import deque
from typing import Deque, Set

import rx
import rx.operators as op
from rx.subject import BehaviorSubject as RxBehaviorSubject

from reactivestate.core.signals import Signal


class TrackingContextManager:
    def __init__(self):
        self.tracked_observables: Deque[Set[RxBehaviorSubject]] = deque()

    def __enter__(self):
        self.tracked_observables.append(set())
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tracked_observables.pop()

    def is_active(self):
        return len(self.tracked_observables) > 0

    def report_observed(self, obs: RxBehaviorSubject):
        try:
            self.tracked_observables[-1].add(obs)
        except IndexError:
            # Nothing is currently being tracked.
            pass

    def get_dependencies(self):
        dependencies = self.tracked_observables[-1]
        return dependencies


local = threading.local()
local.tracking = TrackingContextManager()


def tracking() -> TrackingContextManager:
    return local.tracking


def get_obs_dependency_stale(dependencies) -> rx.Observable:
    """
    Return an observable that emits when a dependency goes stale.
    """
    signals = [op.map(lambda sv: sv.signal)(d) for d in dependencies]
    obs = rx.merge(*signals)
    obs = op.filter(lambda s: s == Signal.STALE)(obs)
    return obs


def get_obs_dependency_changed(dependencies) -> rx.Observable:
    """
    Return an observable that emits once, when no dependencies are stale and one has changed.
    """
    signals = [op.map(lambda sv: sv.signal)(d) for d in dependencies]
    obs = rx.combine_latest(*signals)
    obs = obs[1:]
    obs = op.filter(lambda signals: Signal.STALE not in signals)(obs)
    obs = op.filter(lambda signals: Signal.CHANGED in signals)(obs)
    return obs[0]
