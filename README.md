# views-py

Views and related utilities for generic sequence types.

Defines a dynamic, read-only sequence view with contiguous windowing capabilities, alongside some utilities for defining custom ones.

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

Under this library's definition, a *view* is a thin wrapper around a reference to some [`Sequence[T]`](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes) (called the "target"), and a [`slice`](https://docs.python.org/3/library/functions.html#slice) of indices to view from it (called the "window"). Alterations made to the target are reflected by its views. Views are, themselves, a type of `Sequence[T]`, and do not offer much in terms of extra functionality.

Views are a useful alternative to copies, as an instance of one takes significantly less space in memory for larger sequences, and does not induce much runtime overhead on construction or copy. The `View` class that comes with this library is read-only, but dynamic - meaning that the target can change its items and length, but the view itself cannot be modified (similar to the objects returned by `dict.keys()`, `dict.values()`, and `dict.items()`):

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

Without specifying a window at construction time, views will default to a window that encompasses all of the target's content (equivalent to setting a window of `slice(None, None)`), expanding and contracting when necessary.

The window of a `View` allows for contiguous subsets of a target sequence to be captured. This functionality can be invoked manually, but is best interfaced by a sequence's `__getitem__()` implementation:

```python
>>> from views import View
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> view = View(target, slice(1, 4))
>>> print(list(view))
['b', 'c', 'd']
>>>
>>> view = View(target, slice(None, None, -1))
>>> print(list(view))
['e', 'd', 'c', 'b', 'a']
>>>
>>> view = View(target, slice(6, 10))
>>> print(list(view))
[]
>>>
>>> view = View(target, slice(5, None, -2))
>>> print(list(view))
['d', 'b']
```

The window may or may not overlap with the target's indices. If the window captures a range of indices beyond what is available, then the view is considered empty (but may not always be if the target sequence expands at a later moment in time).

When the target indices and window *do* overlap, the window is "narrowed" to only include the indices that are visible. The narrowed window is calculated similar to how `slice.indices()` calculates its start, stop, and step tuple - the start, however, is computed in a manner that is consistent with the slice's step value:

```python
>>> from views import indices as view_indices
>>>
>>> def slice_indices(slc: slice, len: int) -> tuple[int, int, int]:
...     return slc.indices(len)
...
>>>
>>> target = ['a', 'b', 'c', 'd', 'e']
>>>
>>> slc = slice(5, None, -2)  # Note that index 5 is one space out-of-range
>>>
>>> x = range( *view_indices(slc, len(target)))
>>> y = range(*slice_indices(slc, len(target)))
>>>
>>> # View indices are calculated in a manner that preserves other items of the
>>> # subset, as if some items are "hidden" from us
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

This `indices()` utility is exposed as a free function, and interfaced as a method of the same name under the `View` class. Note that its values in certain edge cases can be hard to judge - particularly with "bad" slices (e.g., a slice whose start precedes its stop, but has negative step). The values in such cases are guaranteed to produce a zero-length `range` when converted to one, however - this is done for performance benefits.

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

This particular `View` implementation is immensely useful in `__getitem__()` methods. The `View` class is, itself, a type of `Sequence[T]`, allowing for compliance with classes that are implementing the `Sequence[T]` interface:

```python
...

class List(MutableSequence[T]):

    ...

    @overload
    def __getitem__(self, key: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self, key: slice) -> View[T]: ...

    def __getitem__(self, key):

        # Provide a view on ourself, with the user's slice as the window -
        # everything else is handled for you, as long as your sequence type
        # follows Python conventions (i.e., indices begin at 0, last index is
        # `len(self) - 1`, each index between is defined, etc.)

        # It's often the case that a user-defined sequence composes a built-in
        # one (like `list` or `tuple`). You may, alternatively, return a view
        # on that attribute directly for performance benefits.

        if isinstance(key, slice):
            return View(self, key)

        ...

    ...
```

You may often want to return a `View` that implements a common interface. In such cases, you can define a set of applicable [mixins](https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-is-it-useful), and use `View` as a base class. A [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) can be used to group classes together without explicitly inheriting.

Custom views may not always want the attributes that come from the concrete `View` class. An abstract base class, `SequenceView`, is provided for scenarios like this. It extends `collections.abc.Sequence`, and does not add or implement anything.
