# ReactiveState

Simple reactive state management for Python.

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

Calling `observe` will run the given function and then rerun it when any of its dependencies change. Use actions to mutate state. 
~~~python
with action():
    state.counter += 1

[Output] "Counter = 2"
~~~

When an action finishes, any affected observers will rerun. If they depend on computeds, those are recalculated. Computeds that are not depended on, won't recalculate. The dependency tree is updated behind the scenes and all reactive calculations run synchronously. This makes for a unidirectional and very predictable dataflow. 

In summary, actions mutate observable state. Computed properties react automatically to state changes, but only if they have to. Observers rerun when their dependencies change. They produce side effects like print, or update part of a user interface.

<img src="assets/gist.png" width=600/>


## API

### action
Mutate observable state.

### observable
Create observable state.

### computed
Add computed properties to observable state.

### observe
Run a function that depends on observable state. It will observe its dependencies and rerun when they change.   



## TODO

First: 
* untrack: to suppress tracking inside observer.
* observe: should return disposer.
* observable: support for add and delete attrs.
* observable: should work like dataclass?
* action: filter on change.
    * Perhaps the values should be tuples of (signal, value), where signal is in [maybe_changed, ready] like in mobx.

Later:
* threading support, lock observable during action?
* upload to pip.


## Internals

ReactiveState is heavily inspired by other reactive programming libraries. For a deeper understanding of the concepts, read: 
* [Reactive engine behind R-Shiny](https://shiny.rstudio.com/articles/execution-scheduling.html). 
* [The gist of MobX](https://mobx.js.org/the-gist-of-mobx.html).

The internals of ReactiveState actually build on the lower level observable sequences from ReactiveX, see [RxPy](https://rxpy.readthedocs.io/en/latest/).
