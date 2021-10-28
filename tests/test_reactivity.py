from unittest.mock import MagicMock

from reactivestate import (
    observable,
    observe,
    computed,
    action,
)



@observable
class MyStore:
    def __init__(self):
        self.a = 1
        self.b = "first"

    @computed
    def c(self):
        return self.b.capitalize()


class TestReactivity:
    def test_observe_attr(self):
        store = MyStore()
        mock = MagicMock()

        def depends_on_a():
            mock(store.a)

        observe(depends_on_a)
        mock.assert_called_once_with(1)
        mock.reset_mock()
        with action():
            store.a = 2
        mock.assert_called_once_with(2)
        mock.reset_mock()
        with action():
            store.b = "second"
        mock.assert_not_called()

    def test_observe_computed(self):
        store = MyStore()
        mock = MagicMock()

        def depends_on_c():
            mock(store.c)

        observe(depends_on_c)
        mock.assert_called_once_with("First")
        mock.reset_mock()
        with action():
            store.a = 2
            store.b = "second"
        mock.assert_called_once_with("Second")
        mock.reset_mock()
        with action():
            store.a = 3
        mock.assert_not_called()
