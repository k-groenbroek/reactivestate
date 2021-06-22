import threading
from typing import Iterable

from rx import Observable, combine_latest
from rx.subject import BehaviorSubject
import rx.operators as op


class ActionContextManager:
    def __init__(self):
        self.obs_counter = BehaviorSubject(0)
        obs = op.pairwise()(self.obs_counter)
        self.obs_action_start = op.filter(lambda pair: pair[0] == 0)(obs)
        self.obs_action_end = op.filter(lambda pair: pair[1] == 0)(obs)

    def __enter__(self):
        self.obs_counter.on_next(self.obs_counter.value + 1)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.obs_counter.on_next(self.obs_counter.value - 1)

    def in_action(self):
        return self.obs_counter.value > 0


local = threading.local()
local.action = ActionContextManager()


def action() -> ActionContextManager:
    return local.action


def combine_action():
    """
    Returns an operator. The operator combines a list of observables into a single observable that only
    emits during action end, and only if any of the source observables is different compared to previous
    action end.
    """

    def operator(observables: Iterable[Observable]):
        obs = combine_latest(*observables)
        obs_first = op.first()(obs)
        obs_sampled = op.sample(local.action.obs_action_end)(obs)
        obs = op.merge(obs_first)(obs_sampled)
        # TODO: comparer.
        obs = op.distinct_until_changed()(obs)
        obs = op.skip(1)(obs)
        return obs

    return operator
