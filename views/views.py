from abc import ABCMeta
from collections.abc import Iterator, Sequence
from reprlib import recursive_repr
from typing import Any, Optional, SupportsIndex, TypeVar, overload

from .utilities import RangeProperties, indices

__all__ = [
    "SequenceViewLike",
    "SequenceView",
    "SequenceWindow",
]

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
SequenceViewT = TypeVar("SequenceViewT", bound="SequenceView")


class SequenceViewLike(Sequence[T_co], metaclass=ABCMeta):
    """Abstract base class for all sequence views

    This class simply derives from ``collections.abc.Sequence`` with no
    additional abstracts, mixins, or implementations.
    """

    __slots__ = ()


class SequenceView(SequenceViewLike[T]):
    """A basic, read-only sequence view

    Views are thin wrappers around a reference to some ``Sequence[T]`` object,
    called the "target" (internally named ``_target``). Mutations to the
    underlying sequence are reflected by its views, but, views themselves
    cannot perform such mutations.
    """

    __slots__ = ("_target",)

    def __init__(self, target: Sequence[T]) -> None:
        self._target = target

    @recursive_repr("...")
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target={self._target!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SequenceView):
            if len(self) != len(other):
                return False
            return all(map(lambda x, y: x is y or x == y, self, other))
        return NotImplemented

    def __len__(self) -> int:
        return len(self._target)

    @overload
    def __getitem__(self, key: int) -> T: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[T]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SequenceWindow(self._target, key)
        return self._target[key]

    def __iter__(self) -> Iterator[T]:
        yield from iter(self._target)

    def __reversed__(self) -> Iterator[T]:
        yield from reversed(self._target)

    def __contains__(self, value: Any) -> bool:
        return value in self._target

    def __deepcopy__(self: SequenceViewT, memo: Optional[dict[int, Any]] = None) -> SequenceViewT:
        return self

    __copy__ = __deepcopy__


class SequenceWindow(SequenceView[T]):
    """A type of ``SequenceView`` capable of viewing only a subset of the
    target sequence, rather than the whole

    To ``SequenceView``, ``SequenceWindow`` adds a ``slice`` attribute whose
    parameters are used to define a "window" of the target sequence for which
    the view is capable of seeing. Instances of ``SequenceWindow`` otherwise
    behave identically to instances of ``SequenceView``.
    """

    __slots__ = ("_window",)

    def __init__(self, target: Sequence[T], window: slice = slice(None, None)) -> None:
        super().__init__(target)
        self._window = window

    @recursive_repr("...")
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target={self._target!r}, window={self._window!r})"

    def __len__(self) -> int:
        sub_keys = self.indices().range()
        return len(sub_keys)

    @overload
    def __getitem__(self, key: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[T]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SequenceWindow(self, key)
        sub_keys = self.indices().range()
        try:
            value = self._target[sub_keys[key]]
        except IndexError as error:
            raise IndexError("window index out of range") from error
        else:
            return value

    def __iter__(self) -> Iterator[T]:
        sub_keys = self.indices().range()
        yield from map(self._target.__getitem__, iter(sub_keys))

    def __reversed__(self) -> Iterator[T]:
        sub_keys = self.indices().range()
        yield from map(self._target.__getitem__, reversed(sub_keys))

    def __contains__(self, value: Any) -> bool:
        return any(map(lambda x: x is value or x == value, self))

    @property
    def window(self) -> slice:
        """A ``slice`` of potential indices to use in retrieval of target items"""
        return self._window

    def indices(self) -> RangeProperties:
        """Return a start, stop, and step tuple that currently form the
        visible selection of the target

        The returned tuple is, more specifically, a ``typing.NamedTuple`` that
        contains some convenience methods for conversion to a ``range`` or
        ``slice`` object.
        """
        return indices(rng=self._window, len=len(self._target))
