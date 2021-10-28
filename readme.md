# ReactiveState

Simple, reactive state management for Python.

~~~shell
pip install reactivestate
~~~


## Quick example

These are the basic building blocks.
~~~python
from reactivestate import (
    observable, observe, computed, action
)
~~~

First create some observable data. Let's also add a computed property.
~~~python
@observable
class MyState:
    def __init__(self):
        self.counter = 1

    @computed
    def text(self):
        return f"Counter = {self.counter}."

state = MyState()
~~~

Define a function that uses the data.
~~~python
def print_text():
    print(state.text)
~~~

Now we're ready to start observing. 
~~~python
observe(print_text)

[Output] "Counter = 1"
~~~

Use actions to mutate state and trigger reactivity.
~~~python
with action():
    state.counter += 1

[Output] "Counter = 2"
~~~

When an action finishes, any affected computed 


state derivations (computed properties, observing functions) will rerun and the dependency tree is updated automatically. 



## API

### observable
Create observable state.

### computed
Add computed properties to observable state.

### observe
Run a function that depends on observable state. It will observe its dependencies and rerun when they change.

### action
Mutate observable state.


## TODO

First:
* isolate: to suppress tracking inside observer.
* observe: should return disposer.
* observable: support for add and delete attrs.
* observable: should work like dataclass?
* action: filter on change.

Later:
* threading support, lock observable during action?
* upload to pip.


## Internals

ReactiveState is heavily inspired by other reactive programming libraries. For a deeper understanding of the concepts, see: 
* R Shiny's [reactive engine](https://shiny.rstudio.com/articles/execution-scheduling.html). 
* Javascript's [MobX](https://mobx.js.org/the-gist-of-mobx.html).

The internals of ReactiveState actually build on the lower level observable sequences from ReactiveX.
* ReactiveX for Python [RxPy](https://rxpy.readthedocs.io/en/latest/)
