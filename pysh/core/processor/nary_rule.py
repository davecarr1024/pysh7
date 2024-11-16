from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized, override

from pysh.core.processor.rule import Rule


@dataclass(frozen=True, kw_only=True)
class NaryRule[State, Result, ChildResult](
    Rule[State, Result],
    Sized,
    Iterable[Rule[State, ChildResult]],
):
    children: Sequence[Rule[State, ChildResult]] = field(default_factory=list)

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator[Rule[State, ChildResult]]:
        return iter(self.children)
