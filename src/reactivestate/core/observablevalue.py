from reactivestate.core.atom import ObservableAtom
from reactivestate.core.action import action


class ObservableValue(ObservableAtom):
    def __init__(self, value):
        super().__init__(value)
        action().on_exit.connect(self._handle_action_exit)

    def _handle_action_exit(self, *args):
        self.ready()
