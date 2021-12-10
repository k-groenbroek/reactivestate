from blinker import Signal


class ObservableAtom:
    on_observed = Signal()
    on_stale = Signal()
    on_ready = Signal()

    def __init__(self, value):
        self.value = value
        self.prev_value = None
        self.stale = False

    def get(self):
        self.on_observed.send(self)
        return self.value

    def set(self, value):
        if not self.stale:
            self.stale = True
            self.prev_value = self.value
            self.on_stale.send(self)
        self.value = value

    def ready(self):
        if not self.stale:
            return
        self.stale = False
        changed = self.value != self.prev_value  # TODO: comparator.
        self.prev_value = None
        self.on_ready.send(self, changed=changed)
