import operator
from abc import abstractmethod
from typing import NamedTuple, Optional, Protocol, SupportsIndex

__all__ = [
    "SupportsRangeProperties",
    "RangeProperties",
    "indices",
]


class SupportsRangeProperties(Protocol):
    """A protocol containing abstract properties for a ``start``, ``stop``, and
    ``step`` index
    """

    @property
    @abstractmethod
    def start(self) -> Optional[SupportsIndex]: ...
    @property
    @abstractmethod
    def stop(self) -> Optional[SupportsIndex]: ...
    @property
    @abstractmethod
    def step(self) -> Optional[SupportsIndex]: ...


class RangeProperties(NamedTuple):
    """A named tuple containing a ``start``, ``stop``, and ``step`` index,
    convertable to a built-in ``range`` or ``slice`` object
    """

    start: int
    stop: int
    step: int

    def range(self) -> range:
        """Return a ``range`` of the tuple's indices"""
        return range(self.start, self.stop, self.step)

    def slice(self) -> slice:
        """Return a ``slice`` of the tuple's indices"""
        return slice(self.start, self.stop, self.step)


def indices(rng: SupportsRangeProperties, len: SupportsIndex) -> RangeProperties:
    """Return a start, stop, and step tuple currently applicable to a sequence
    of size ``len``, with the properties of ``rng``

    This function is a near-direct translation of ``slice.indices()``
    (originally implemented in C), with the starting value calculated based on
    the step of ``rng``, rather than a simple numeric clamp. See the
    ``_PySlice_GetLongIndices()`` function of sliceobject.c here:
    https://github.com/python/cpython/blob/main/Objects/sliceobject.c

    Raises ``ValueError`` if the step of ``rng`` is 0.
    """
    start = rng.start
    stop  = rng.stop
    step  = rng.step

    len = operator.index(len)

    if step is None:
        step = 1
        reverse = False
    else:
        step = operator.index(step)
        if not step:
            raise ValueError("step must be non-zero")
        reverse = step < 0

    lower, upper = (-1, len - 1) if reverse else (0, len)

    if start is None:
        start = upper if reverse else lower
    else:
        start = operator.index(start)
        if start < 0:
            start += len
            if start < lower:
                shift = lower - start
                start = start + shift + (step - r if (r := shift % step) else 0)
        else:
            if start > upper:
                shift = upper - start
                start = start + shift + (step - r if (r := shift % step) else 0)

    if stop is None:
        stop = lower if reverse else upper
    else:
        stop = operator.index(stop)
        if stop < 0:
            stop += len
            if stop < lower:
                stop = lower
        else:
            if stop > upper:
                stop = upper

    return RangeProperties(start, stop, step)
