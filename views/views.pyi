from collections.abc import Iterator, Sequence
from typing import Any, Literal, Optional, TypeVar, overload

__all__ = ["View", "WindowedView"]

T = TypeVar("T")
S = TypeVar("S")

Self = TypeVar("Self")


class View(Sequence[T]):

    __slots__: tuple[Literal["_target"]]

    def __init__(self: Self, target: Sequence[T]) -> None: ...
    def __repr__(self: Self) -> str: ...
    def __str__(self: Self) -> str: ...
    def __len__(self: Self) -> int: ...
    @overload
    def __getitem__(self: Self, key: int) -> T: ...
    @overload
    def __getitem__(self: Self, key: slice) -> WindowedView[T]: ...
    def __iter__(self: Self) -> Iterator[T]: ...
    def __reversed__(self: Self) -> Iterator[T]: ...
    def __contains__(self: Self, value: Any) -> bool: ...
    def __eq__(self: Self, other: Any) -> bool: ...


class WindowedView(View[T]):

    __slots__: tuple[Literal["_window"]]

    def __init__(self: Self, target: Sequence[T], window: Optional[Sequence[int]] = None) -> None: ...
    def __repr__(self: Self) -> str: ...
    def __len__(self: Self) -> int: ...
    @overload
    def __getitem__(self: Self, key: int) -> T: ...
    @overload
    def __getitem__(self: Self, key: slice) -> Self: ...
    def __iter__(self: Self) -> Iterator[T]: ...
    def __reversed__(self: Self) -> Iterator[T]: ...
    def __contains__(self: Self, value: Any) -> bool: ...

    @overload
    def get(self: Self, key: int) -> Optional[T]: ...
    @overload
    def get(self: Self, key: int, default: S) -> T | S: ...
    @overload
    def get_each(self: Self) -> Iterator[Optional[T]]: ...
    @overload
    def get_each(self: Self, default: S) -> Iterator[T | S]: ...