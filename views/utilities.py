import copy
from collections.abc import Sequence
from typing import Generic, TypeVar

__all__ = ["LazySequence"]

T_co = TypeVar("T_co", covariant=True)
S_co = TypeVar("S_co", covariant=True)


class LazySequence(Sequence[T_co], Generic[T_co, S_co]):
    """A lazily-evaluated sequence with restricted domain

    Instances of `LazySequence` wrap a callable that maps the values of a
    domain to a new value of the sequence. Unlike some lazy sequence
    implementations, the mapper's results are not cached, as doing so can
    introduce additional memory cost for cheap mappers. To implement caching,
    use the `cache()` or `lru_cache()` decorator (from the built-in `functools`
    module) on the mapper.

    Lazy sequences can be particularly effective as windows to `WindowedView`
    instances, as a callable that generates windowing indices from a
    lazily-evaluated domain (such as a `range`) can preserve additional memory
    over a standard sequence type.
    """

    __slots__ = ("_mapper", "_domain")

    def __init__(self, mapper, domain):
        self._mapper = mapper
        self._domain = copy.copy(domain)

    def __len__(self):
        """Return the length of the sequence"""
        return len(self._domain)

    def __getitem__(self, key):
        """Return the element or subsequence corresponding to `key`"""
        mapper = self._mapper
        subkey = self._domain[key]
        if isinstance(key, slice):
            return self.__class__(mapper, subkey)
        return mapper(subkey)

    def __iter__(self):
        """Return an iterator that yields the sequence's items"""
        yield from map(self._mapper, self._domain)

    def __reversed__(self):
        """Return an iterator that yields the sequence's items in reverse order"""
        yield from map(self._mapper, reversed(self._domain))

    def __contains__(self, value):
        """Return true if the sequence contains `value`, otherwise false"""
        return any(map(lambda x: x is value or x == value, self))

    def __deepcopy__(self, memo=None):
        """Return a deep copy of the sequence"""
        cls = self.__class__

        new = cls.__new__(cls)
        new._mapper = self._mapper  # Callables are atomic
        new._domain = copy.deepcopy(self._domain, memo=memo)

        return new

    def __copy__(self):
        """Return a shallow copy of the sequence"""
        return self.__class__(self._mapper, self._domain)

    @property
    def mapper(self):
        """The function whose results compose the sequence's elements from the
        domain
        """
        return self._mapper

    @property
    def domain(self):
        """The sequence of valid arguments capable of being passed to the
        mapper
        """
        return self._domain
