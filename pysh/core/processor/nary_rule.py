from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized, override

from pysh.core.processor import rule


@dataclass(frozen=True, kw_only=True)
class NaryRule[State, Result, ChildResult](
    rule.Rule[State, Result],
    Sized,
    Iterable[rule.Rule[State, ChildResult]],
):
    children: Sequence[rule.Rule[State, ChildResult]] = field(default_factory=list)

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator[rule.Rule[State, ChildResult]]:
        return iter(self.children)
