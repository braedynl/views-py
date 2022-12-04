import reprlib
import typing
from collections.abc import Iterator, Sequence
from typing import Any, Optional, SupportsIndex, TypeVar

__all__ = ["View"]

T    = TypeVar("T")
Self = TypeVar("Self", bound="View")


class View(Sequence[T]):
    """A dynamically-sized, read-only view into a `Sequence[T]` object

    Views are thin wrappers around a reference to some `Sequence[T]` (called
    the "target"), and a `slice` of indices to view from it (called the
    "window"). Alterations made to the target are reflected by its views.

    At creation time, a window can be provided to define the view object's
    boundaries. Views may shrink if its target shrinks - they may also expand
    if the window defines non-integral boundaries. The window may only contain
    integral or `NoneType` values.
    """

    __slots__ = ("_target", "_window")

    def __init__(self, target: Sequence[T], window: slice = slice(None)) -> None:
        self._target = target
        self._window = window

    @reprlib.recursive_repr(fillvalue="...")
    def __repr__(self) -> str:
        """Return a canonical representation of the view"""
        return f"{self.__class__.__name__}(target={self._target!r}, window={self._window!r})"

    __str__ = __repr__

    def __len__(self) -> int:
        """Return the number of currently viewable items"""
        return len(range(*self.indices()))

    @typing.overload
    def __getitem__(self: Self, key: SupportsIndex) -> T: ...
    @typing.overload
    def __getitem__(self: Self, key: slice) -> Self: ...

    def __getitem__(self, key):
        """Return the element or sub-view corresponding to `key`

        Note that slicing is performed relative to the currently viewable
        items, rather than the "potential" selection of items defined by the
        window.

        Since a new `View` instance is made for slice arguments, this method
        guarantees constant-time performance.
        """
        if isinstance(key, slice):
            return self.__class__(self, key)
        subkeys = range(*self.indices())
        try:
            subkey = subkeys[key]
        except IndexError as error:
            raise IndexError(f"index out of range of window") from error
        else:
            result = self._target[subkey]
            return result

    def __iter__(self) -> Iterator[T]:
        """Return an iterator that yields the currently viewable items"""
        subkeys = range(*self.indices())
        yield from map(self._target.__getitem__, subkeys)

    def __reversed__(self) -> Iterator[T]:
        """Return an iterator that yields the currently viewable items in
        reverse order
        """
        subkeys = range(*self.indices())
        yield from map(self._target.__getitem__, reversed(subkeys))

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

        Views compare equal if they are element-wise equivalent, independent of
        their target classes.
        """
        if isinstance(other, View):
            self_subkeys, other_subkeys = (
                range( *self.indices()),
                range(*other.indices()),
            )
            if len(self_subkeys) != len(other_subkeys):
                return False
            return all(map(
                lambda x, y: x is y or x == y,
                map(
                     self._target.__getitem__,
                     self_subkeys,
                ),
                map(
                    other._target.__getitem__,
                    other_subkeys,
                ),
            ))
        return NotImplemented

    @property
    def window(self) -> slice:
        """A slice of potential indices to use in retrieval of target items"""
        return self._window

    def indices(self) -> tuple[int, int, int]:
        """Return the start, stop, and step indices that currently form the
        viewable selection of the target

        Internally, these values are simply calculated from the window's
        `indices()` method, using the length of the target sequence as its
        argument.
        """
        return self._window.indices(len(self._target))
