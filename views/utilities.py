import operator
from abc import abstractmethod
from typing import NamedTuple, Optional, Protocol, SupportsIndex

__all__ = ["RangeLike", "RangeLikeTuple", "indices"]


class RangeLike(Protocol):
    """A protocol containing abstract properties for a `start`, `stop`, and
    `step` index
    """

    @property
    @abstractmethod
    def start(self) -> Optional[int]: ...
    @property
    @abstractmethod
    def stop(self) -> Optional[int]: ...
    @property
    @abstractmethod
    def step(self) -> Optional[int]: ...  # XXX: integer values should try to be non-zero


class RangeLikeTuple(NamedTuple):
    """A named tuple containing a `start`, `stop`, and `step` index,
    convertable to a built-in `range` or `slice` object
    """

    start: int
    stop: int
    step: int

    def range(self) -> range:
        """Return a `range` of the tuple's indices"""
        return range(self.start, self.stop, self.step)

    def slice(self) -> slice:
        """Return a `slice` of the tuple's indices"""
        return slice(self.start, self.stop, self.step)


def indices(rng: RangeLike, len: SupportsIndex) -> RangeLikeTuple:
    """Return a `start`, `stop`, and `step` tuple currently applicable to a
    sequence of `len`, with the properties of `rng`

    This function is a near-direct translation of `slice.indices()` (originally
    implemented in C), with the starting value calculated based on the step of
    `rng`, rather than a simple numeric clamp.
    """
    start, stop, step = rng.start, rng.stop, rng.step

    len = operator.index(len)

    if step is None:
        step = 1
        reverse = False
    else:
        if not step:
            raise ValueError("step must be non-zero")
        reverse = step < 0

    lower, upper = (-1, len - 1) if reverse else (0, len)

    if start is None:
        start = upper if reverse else lower
    else:
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
        if stop < 0:
            stop += len
            if stop < lower:
                stop = lower
        else:
            if stop > upper:
                stop = upper

    return RangeLikeTuple(start, stop, step)
