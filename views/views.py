from collections.abc import Iterator, Sequence
from typing import Any, Optional, SupportsIndex, TypeVar, final, overload

__all__ = ["View"]

T    = TypeVar("T")
Self = TypeVar("Self", bound="View")


def clamp(x: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, x))


@final
class View(Sequence[T]):
    """A dynamically-sized, read-only view into a `Sequence[T]` object

    Views are thin wrappers around a reference to some `Sequence[T]` (called
    the "target"), and a `range` of indices to view from it (called the
    "window"). Alterations made to the target are reflected by its views.

    At creation time, a window can be provided to define the view object's
    boundaries. Views can shrink and expand, but only within the space alloted
    by the window. The view will only contain values if the window's starting
    index is within range of the target.
    """

    NULL_WINDOW: range = range(0, 0, 1)

    __slots__ = ("_target", "_window")

    def __init__(self, target: Sequence[T], window: Optional[range] = None) -> None:
        self._target = target
        self._window = range(len(target)) if window is None else window

    def __repr__(self) -> str:
        """Return a canonical representation of the view"""
        return f"{self.__class__.__name__}(target={self._target!r}, window={self._window!r})"

    __str__ = __repr__

    def __len__(self) -> int:
        """Return the number of currently viewable items"""
        return len(self.subwindow())

    @overload
    def __getitem__(self: Self, key: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self: Self, key: slice) -> Self: ...

    def __getitem__(self, key):
        """Return the element or sub-view corresponding to `key`

        Note that slicing is performed relative to the "complete" window, as
        opposed to the active sub-window.

        Since a new `View` instance is made for slice arguments, this method
        guarantees constant-time performance.
        """
        target = self._target
        window = self._window[key]
        if isinstance(key, slice):
            return self.__class__(target, window)
        return target[window]

    def __iter__(self) -> Iterator[T]:
        """Return an iterator that yields the currently viewable items"""
        yield from map(self._target.__getitem__, self.subwindow())

    def __reversed__(self) -> Iterator[T]:
        """Return an iterator that yields the currently viewable items in
        reverse order
        """
        yield from map(self._target.__getitem__, reversed(self.subwindow()))

    def __contains__(self, value: Any) -> bool:
        """Return true if the currently viewable items contains `value`,
        otherwise false
        """
        return any(map(lambda x: x is value or x == value, self))

    def __deepcopy__(self: Self, memo: Optional[dict[int, Any]] = None) -> Self:
        """Return the view"""
        return self

    __copy__ = __deepcopy__

    def __eq__(self, other: Any) -> bool:
        """Return true if the two views are equal, otherwise false

        Views are considered equal if they refer to the same target and have
        equal windows.
        """
        if isinstance(other, View):
            return (
                self._target is other._target
                and
                self._window == other._window
            )
        return NotImplemented

    @property
    def window(self) -> range:
        """A range of potential indices to use in retrieval of target items"""
        return self._window

    def full(self) -> bool:
        """Return true if the view is at full capacity, otherwise false

        Equivalent to `len(view.window) == len(view)`.
        """
        return len(self._window) == len(self)

    def subwindow(self) -> range:
        """Return a range of indices currently viewable from the window

        If the window's starting index is out of range of the target,
        `range(0, 0)` is returned.
        """
        target = self._target
        window = self._window

        length = len(target)

        start = window.start

        if start < -length or start >= length:
            return self.NULL_WINDOW

        stop = clamp(window.stop, lower=-length - 1, upper=length)
        step = window.step

        return range(start, stop, step)
