# views-py

Views and related utilities for generic sequence types.

Contains a simplistic, dynamically-sized, windowed view class for generic Python sequences.

## Getting Started

This project is available through pip (requires Python 3.10 or higher):

```
pip install views-py
```

Documentation can be found below.

## Contributing

This project is currently maintained by [Braedyn L](https://github.com/braedynl). Feel free to report bugs or make a pull request through this repository.

## License

Distributed under the MIT license. See the [LICENSE](LICENSE) file for more details.

## Quickstart

Due to the simplicity of this library, the following is considered the "official" documentation of the API. Classes and associated functions may contain further details in their docstrings.

Under this library's definition, a *view* is a thin wrapper around a reference to some `Sequence[T]` (called the "target"), and a `range` of indices to view from it (called the "window"). Alterations made to the target are reflected by its views.

Views are a useful alternative to copies, as a view takes significantly less space in memory for larger sequence objects, and cost next to nothing to construct.

```python
>>> from views import View
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> view = View(target)
>>> print(view)
View(target=['a', 'b', 'c', 'd', 'e'], window=range(0, 5))
>>>
>>> for x in view: print(x)
...
a
b
c
d
e
```

The `View` class that comes packaged with this library has a few interesting properties. For one, it is strictly *read-only* - retrieval of items is allowed, but any form of mutation is disallowed (at least through the `View` instance, that is - more on mutations shortly).

With this property, a `View` instance can be safely returned by a class that wishes to expose its mutable data "immutably", for example:

```python
from collections.abc import Iterable, Sequence
from typing import TypeVar

from views import View

T = TypeVar("T")


class Vector(Sequence[T]):

    __slots__ = ("_data",)

    def __init__(self, data: Iterable[T]) -> None:
        self._data = list(data)

    ...

    @property
    def data(self) -> View[T]:   # Avoids the need to copy while also
        return View(self._data)  # preventing unwanted changes to our _data

    ...
```

While the `View` object is read-only, it's important to remember (and should often be advised in documentation) that it may change at any point in time when the target itself can change. Sequences that derive from `collections.abc.MutableSequence` implement an `append()` and `pop()` method (among others) that can add or remove elements from its associated views:

```python
>>> target = ['a', 'b', 'c', 'd', 'e']  # Lists are mutable...
>>>
>>> view = View(target)  # and thus, this view is subject to change.
>>>
>>> print(list(view))  # We have all of the items, now...
['a', 'b', 'c', 'd', 'e']
>>>
>>> target.pop()
'e'
>>>
>>> print(list(view))  # but we may not have them later.
['a', 'b', 'c', 'd']
```
