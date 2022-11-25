import copy
from collections.abc import Callable, Iterator, Sequence
from typing import Any, Generic, Optional, TypeVar, overload

T_co = TypeVar("T_co", covariant=True)
S_co = TypeVar("S_co", covariant=True)

Self = TypeVar("Self", bound="LazySequence")


class LazySequence(Sequence[T_co], Generic[T_co, S_co]):
    """A lazily-evaluated sequence with restricted domain

    Instances of `LazySequence` wrap a callable that maps the values of a
    domain to a new value of the sequence. Unlike some lazy sequence
    implementations, the mapper's results are not cached, as doing so can
    introduce additional memory cost for cheap mappers.

    To implement caching, use the `cache()` or `lru_cache()` decorator (from
    the built-in `functools` module) on the mapper.
    """

    __slots__ = ("_mapper", "_domain")

    def __init__(self, mapper: Callable[[S_co], T_co], domain: Sequence[S_co]) -> None:
        self._mapper = mapper
        self._domain = copy.copy(domain)

    def __len__(self) -> int:
        """Return the length of the sequence"""
        return len(self._domain)

    @overload
    def __getitem__(self: Self, key: int) -> T_co: ...
    @overload
    def __getitem__(self: Self, key: slice) -> Self: ...

    def __getitem__(self, key):
        """Return the element or subsequence corresponding to `key`"""
        mapper = self._mapper
        subkey = self._domain[key]
        if isinstance(key, slice):
            return self.__class__(mapper, subkey)
        return mapper(subkey)

    def __iter__(self) -> Iterator[T_co]:
        """Return an iterator that yields the sequence's items"""
        yield from map(self._mapper, self._domain)

    def __reversed__(self) -> Iterator[T_co]:
        """Return an iterator that yields the sequence's items in reverse order"""
        yield from map(self._mapper, reversed(self._domain))

    def __contains__(self, value: Any) -> bool:
        """Return true if the sequence contains `value`, otherwise false"""
        return any(map(lambda x: x is value or x == value, self))  # type: ignore[misc]

    def __deepcopy__(self: Self, memo: Optional[dict[int, Any]] = None) -> Self:
        """Return a deep copy of the sequence"""
        cls = self.__class__

        new = cls.__new__(cls)
        new._mapper = self._mapper  # Callables are atomic
        new._domain = copy.deepcopy(self._domain, memo=memo)

        return new

    def __copy__(self: Self) -> Self:
        """Return a shallow copy of the sequence"""
        return self.__class__(self._mapper, self._domain)

    @property
    def mapper(self) -> Callable[[S_co], T_co]:
        """The function whose results compose the sequence's elements from the
        domain
        """
        return self._mapper

    @property
    def domain(self) -> Sequence[S_co]:
        """The sequence of valid arguments capable of being passed to the
        mapper
        """
        return self._domain
