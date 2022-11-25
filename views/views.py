import copy
from collections.abc import Sequence
from typing import TypeVar

from .exceptions import WindowingIndexError

__all__ = ["View", "WindowedView"]

T = TypeVar("T")


class View(Sequence[T]):
    """A read-only view on a `Sequence[T]` object

    Similar to the objects returned by `dict.keys()` and `dict.values()`,
    alterations made to the wrapped sequence (called the "target") are
    reflected by its associated `View` instances.
    """

    __slots__ = ("_target",)

    def __init__(self, target):
        """Construct a view from its target"""
        self._target = target

    def __repr__(self):
        """Return a canonical representation of the view"""
        return f"{self.__class__.__name__}(target={self._target!r})"

    def __str__(self):
        """Return a string representation of the view"""
        return f"<{', '.join(map(str, self))}>"

    def __len__(self):
        """Return the length of the view"""
        return len(self._target)

    def __getitem__(self, key):
        """Return the element or subsequence corresponding to `key`

        If `key` is a slice, a sub-class of `View` (`WindowedView`) is
        returned. See its class documentation for more details.
        """
        target = self._target
        if isinstance(key, slice):
            return WindowedView(target, window=range(*key.indices(len(self))))
        try:
            value = target[key]
        except IndexError as error:
            n = len(target)
            raise IndexError(f"target has length {n}, but index is {key}") from error
        else:
            return value

    def __iter__(self):
        """Return an iterator that yields the view's items"""
        yield from iter(self._target)

    def __reversed__(self):
        """Return an iterator that yields the view's items in reverse order"""
        yield from reversed(self._target)

    def __contains__(self, value):
        """Return true if the view contains `value`, otherwise false"""
        return value in self._target

    def __eq__(self, other):
        """Return true if the views are equal, otherwise false

        Any non-`View` argument will emit `NotImplemented`. Views are
        considered equal if they are element-wise equivalent, regardless of the
        target's class.
        """
        if not isinstance(other, View):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(map(lambda x, y: x is y or x == y, self, other))


class WindowedView(View[T]):
    """A type of `View[T]` capable of viewing only a subset of items from the
    target sequence, rather than the whole

    Instances contain a "window", which is a sequence of indices used to tell
    the view where it should look within the target. These indices are called
    the "windowing indices".

    Unlike most views, windowed views will not shrink or expand themselves to
    fit the target. The window is constant, and the target is allowed to change
    from beneath, meaning that windowing indices can go in and out of range
    depending on actions performed by the target.

    If a windowing index goes out of range, `WindowingIndexError` is raised.
    This is a type of `LookupError` (not an `IndexError`!) that will only ever
    be raised by `__getitem__()` and its dependents.
    """

    __slots__ = ("_window",)

    def __init__(self, target, window=None):
        """Construct a windowed view from its target and window

        If `window` is unspecified or `None`, it defaults to
        `range(len(target))`, making a window that simply views the target as a
        whole. If a view on the whole target is needed, using a basic `View` is
        recommended.
        """
        self._target = target
        self._window = range(len(target)) if window is None else copy.copy(window)

    def __repr__(self):
        return f"{self.__class__.__name__}(target={self._target!r}, window={self._window!r})"

    def __len__(self):
        return len(self._window)

    def __getitem__(self, key):
        """Return the element or subsequence corresponding to `key`

        This method may raise one of two exceptions (both sub-classes of
        `LookupError`). `IndexError` is raised if `key` is out of range of the
        window. `WindowingIndexError` is raised if the "sub-key" that `key`
        maps to is out of range of the target.

        If a `WindowingIndexError` is raised, this often means that the target
        has reduced its length (assuming that the index was in-range at a prior
        moment in time). Windowing indices may become in-range again if the
        target grows in length.
        """
        window = self._window
        try:
            subkey = window[key]
        except IndexError as error:
            n = len(window)
            raise IndexError(f"window has length {n}, but index is {key}") from error
        else:
            target = self._target
            if isinstance(key, slice):
                return self.__class__(target, subkey)
            try:
                value = target[subkey]
            except IndexError as error:
                n = len(target)
                raise WindowingIndexError(f"target has length {n}, but windowing index is {subkey} (origin index {key})") from error
            else:
                return value

    def __iter__(self, *, iter=iter):
        window = self._window
        target = self._target
        for subkey in iter(window):
            try:
                value = target[subkey]
            except IndexError as error:
                n = len(target)
                raise WindowingIndexError(f"target has length {n}, but windowing index is {subkey}") from error
            else:
                yield value

    def __reversed__(self):
        yield from self.__iter__(iter=reversed)

    def __contains__(self, value):
        return any(map(lambda x: x is value or x == value, self))

    def get(self, key, default=None):
        """Return the element corresponding to `key`, or `default` if the
        windowing index is out of range

        Raises `IndexError` if `key` is out of range of the window.
        """
        window = self._window
        try:
            subkey = window[key]
        except IndexError as error:
            n = len(window)
            raise IndexError(f"window has length {n}, but index is {key}") from error
        else:
            target = self._target
            n = len(target)
            return target[subkey] if -n <= subkey < n else default

    def get_each(self, default=None):
        """Return an iterator that yields the view's items, or `default` if the
        windowing index is out of range
        """
        target = self._target
        window = self._window
        n = len(target)
        yield from map(lambda subkey: target[subkey] if -n <= subkey < n else default, window)