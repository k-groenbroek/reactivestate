import asyncio

from source.reactive_source import reactive_source
from source.reactive_sink import reactive_sink
from source.reactive_conductor import reactive_conductor
from source.core.action import action

# TODO: observable lists?
# TODO: support delete attr?
# TODO: threading support, lock ReactiveState object during action?


@reactive_source
class MyStore:
    def __init__(self):
        self.a = 1
        self.b = "test"

    @reactive_conductor
    def c(self):
        return self.b.capitalize()


async def test():
    print("start")

    store = MyStore()

    @reactive_sink
    def print_store():
        print(f"store.c = {store.c}")
        # TODO: isolate()

    with action():
        store.a = -1
        store.b = "hoi!"

    # Error: store.a = 3
    # Error: print(store.c)

    print("done")


if __name__ == "__main__":
    asyncio.run(test())
