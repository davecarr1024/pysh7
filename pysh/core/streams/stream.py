from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, Self, Sequence, Sized, TypeVar, override

from pysh.core.errors import Error
from pysh.core.errors.errorable import Errorable

_Item = TypeVar("_Item")


@dataclass(frozen=True)
class Stream(
    Generic[_Item],
    Sized,
    Iterable[_Item],
    Errorable,
):
    class Error(Error): ...

    class EmptyError(Error): ...

    _items: Sequence[_Item] = field(default_factory=list)

    @override
    def __len__(self) -> int:
        return len(self._items)

    @override
    def __iter__(self) -> Iterator[_Item]:
        return iter(self._items)

    def empty(self) -> bool:
        return len(self) == 0

    def head(self) -> _Item:
        if self.empty():
            raise self._error(
                type=self.EmptyError,
                msg="getting head from empty stream",
            )
        return self._items[0]

    def tail(self) -> Self:
        if self.empty():
            raise self._error(
                type=self.EmptyError,
                msg="getting tail from empty stream",
            )
        return self.__class__(self._items[1:])
