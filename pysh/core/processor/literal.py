from dataclasses import dataclass
from typing import override

from pysh.core.processor.rule import Rule


@dataclass(frozen=True)
class Literal[State, Result](Rule[State, Result]):
    result: Result

    @override
    def __call__(self, state: State) -> tuple[State, Result]:
        return state, self.result
