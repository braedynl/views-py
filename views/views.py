from __future__ import annotations

from collections.abc import Iterator, Sequence
from copy import copy
from typing import Any, Optional, TypeVar, overload

__all__ = ["View", "WindowingIndexError", "WindowedView"]

T = TypeVar("T")


class View(Sequence[T]):
    """A read-only view on a `Sequence[T]` object

    Similar to the objects returned by `dict.keys()` and `dict.values()`,
    alterations made to the wrapped sequence (called the "target") are
    reflected by the view instance.
    """

    __slots__ = ("_target",)

    Self = TypeVar("Self", bound="View")

    def __init__(self: Self, target: Sequence[T]) -> None:
        """Construct a view from its target"""
        self._target = target

    def __repr__(self: Self) -> str:
        """Return a canonical representation of the view"""
        return f"{self.__class__.__name__}(target={self._target!r})"

    def __str__(self: Self) -> str:
        """Return a string representation of the view"""
        return f"<{', '.join(map(str, self))}>"

    def __len__(self: Self) -> int:
        """Return the length of the view"""
        return len(self._target)

    @overload
    def __getitem__(self: Self, key: int) -> T: ...
    @overload
    def __getitem__(self: Self, key: slice) -> WindowedView[T]: ...

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
            n = len(self)
            raise IndexError(f"target has length {n}, but index is {key}") from error
        else:
            return value

    def __iter__(self: Self) -> Iterator[T]:
        """Return an iterator that yields the view's items"""
        yield from map(self.__getitem__, range(len(self)))

    def __reversed__(self: Self) -> Iterator[T]:
        """Return an iterator that yields the view's items in reverse order"""
        yield from map(self.__getitem__, reversed(range(len(self))))

    def __contains__(self: Self, value: Any) -> bool:
        """Return true if the view contains `value`, otherwise false"""
        return any(map(lambda x: x is value or x == value, self))


class WindowingIndexError(LookupError):
    """Raised when a windowing index is out of range"""
    ...


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

    Self = TypeVar("Self", bound="WindowedView")

    def __init__(self: Self, target: Sequence[T], window: Optional[Sequence[int]] = None) -> None:
        """Construct a windowed view from its target and window

        If `window` is unspecified or `None`, it defaults to
        `range(len(target))`, making a window that simply views the target as a
        whole. If a view on the whole target is needed, using a basic `View` is
        recommended.
        """
        self._target = target
        self._window = range(len(target)) if window is None else copy(window)

    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}(target={self._target!r}, window={self._window!r})"

    def __len__(self: Self) -> int:
        return len(self._window)

    @overload
    def __getitem__(self: Self, key: int) -> T: ...
    @overload
    def __getitem__(self: Self, key: slice) -> Self: ...

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
            n = len(self)
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
