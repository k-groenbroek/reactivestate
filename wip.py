import asyncio

from source.reactive_state import reactive
from source.core.action import action
from source.derivations import Autorun

# TODO: observable lists?
# TODO: support delete attr?
# TODO: threading support, lock ReactiveState object during action?


@reactive
class Store:
    def __init__(self):
        self.a = 1
        self.b = "test"

    @property
    def bigb(self):
        return self.b.capitalize()


async def test():
    print("start")

    store = Store()
    with action():
        store.b = "hoi!"
        store.a = -1

    @Autorun
    def myfunc():
        print({"a": store.a, "b": store.b})

    myfunc()

    with action():
        store.a = -1
        store.b = "hoi!"

    with action():
        store.b = "hoi?"

    #    with action():
    #        store.a = 1
    #        store.a = 1

    print("done")


if __name__ == "__main__":
    asyncio.run(test())
