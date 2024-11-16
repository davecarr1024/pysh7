from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Self, override

from pysh.core.processor.result_builder import ResultBuilder


@dataclass(frozen=True)
class ListBuilder[Result](ResultBuilder[Sequence[Result], Result]):
    results: Sequence[Result] = field(default_factory=list)

    @override
    def reset(self) -> "ListBuilder[Result]":
        return ListBuilder[Result]()

    @override
    def add(self, child_result: Result) -> "ListBuilder[Result]":
        return ListBuilder[Result](list(self.results) + [child_result])

    @override
    def get(self) -> Sequence[Result]:
        return self.results
