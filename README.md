# views-py

Views and related utilities for generic sequence types.

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

Under this library's definition, a *view* is a thin wrapper around a reference to some `Sequence[T]` (called the "target"), and a `slice` of indices to view from it (called the "window"). Alterations made to the target are reflected by its views.

Views are a useful alternative to copies, as an instance of one takes significantly less space in memory for large sequences, and do not induce much runtime overhead on construction. The `View` class that comes with this library is read-only, but dynamic - meaning that the target can change its items and length, but the view itself cannot be modified:

```python
>>> from views import View
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> view = View(target)
>>> print(view)
View(target=['a', 'b', 'c', 'd', 'e'], window=slice(None, None, None))
>>>
>>> print(list(view))
['a', 'b', 'c', 'd', 'e']
>>>
>>> target.append('f')
>>>
>>> print(list(view))
['a', 'b', 'c', 'd', 'e', 'f']
```

Without specifying a window at construction time, views will default to a window that encompasses all of the target's content (equivalent to setting a window of `slice(None, None)`).

The window of a `View` allows for contiguous subsets of a target sequence to be captured. This functionality can be invoked manually, but is best interfaced by a sequence's `__getitem__()` implementation.

```python
>>> from views import View
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> view = View(target, window=slice(1, 4))
>>> print(list(view))
['b', 'c', 'd']
>>>
>>> view = View(target, window=slice(None, None, -1))
>>> print(list(view))
['e', 'd', 'c', 'b', 'a']
>>>
>>> view = View(target, window=slice(6, 10))
>>> print(list(view))
[]
>>>
>>> view = View(target, window=slice(5, None, -2))
>>> print(list(view))
['d', 'b']
```

The window may not overlap with the target's indices. If the window captures a range of indices beyond what is available, then the view is considered empty (but may not always be if the target sequence expands at a later moment in time).

When the target indices and window *do* overlap, the window is "narrowed" to only include the indices that are visible. The narrowed window is calculated similar to how `slice.indices()` calculates its start, stop, and step tuple - the start, however, is computed in a manner that is consistent with the slice's step value:

```python
>>> from views import indices
>>>
>>> def slice_indices(slc: slice, len: int) -> tuple[int, int, int]:
...     return slc.indices(len)
...
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> slc = slice(5, None, -2)  # Note that index 5 is one space out-of-range
>>>
>>> x = range(      *indices(slc, len(target)))
>>> y = range(*slice_indices(slc, len(target)))
>>>
>>> # View indices are calculated in a manner that preserves other items of the
>>> # subset
>>> for i in x: print(target[i])
...
d
b
>>> # The indices() method of built-in slice simply clamps the starting value,
>>> # which may include items that are not normally a part of the subset if all
>>> # indices of the slice were present
>>> for i in y: print(target[i])
...
e
c
a
```

### Examples

One common scenario in which a `View` may be desirable is in "immutable exposition" of mutable data:

```python
from collections.abc import Iterable, MutableSequence
from typing import TypeVar

from views import View

T = TypeVar("T")


class List(MutableSequence[T]):

    __slots__ = ("_data",)

    def __init__(self, data: Iterable[T]) -> None:
        self._data = list(data)

    ...

    @property
    def data(self) -> View[T]:
        return View(self._data)

    ...
```

We may not want the user to have direct access to our `_data` attribute, in this example, so we can instead provide a `View` of it. This avoids the need to copy, while being incredibly cheap to compute.
