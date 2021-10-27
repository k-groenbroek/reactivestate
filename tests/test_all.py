from reactivestate import (
    reactive_source,
    reactive_conductor,
    reactive_sink,
    action,
)

# TODO: observable lists?
# TODO: support delete attr?
# TODO: threading support, lock ReactiveState object during action?


class TestReactivity:
    def test_ok(self):
        pass

    def test_store(self):
        @reactive_source
        class MyStore:
            def __init__(self):
                self.a = 1
                self.b = "test"

            @reactive_conductor
            def c(self):
                return self.b.capitalize()

        store = MyStore()

        @reactive_sink
        def print_store():
            print(f"store.c = {store.c}")
            # TODO: isolate()

        with action():
            store.a = -1
            store.b = "hoi!"
