from dataclasses import dataclass
from typing import override

from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult


@dataclass(frozen=True)
class Literal[State, Result](Rule[State, Result]):
    result: Result

    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        return StateAndResult[State, Result](state, self.result)
