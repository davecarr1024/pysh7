from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, override

from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult


class StateExtractor[State, Result](Rule[State, Result]):
    @abstractmethod
    def extract(self, state) -> Result: ...

    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        return StateAndResult[State, Result](state, self.extract(state))


@dataclass(frozen=True)
class _FuncStateExtractor[State, Result](StateExtractor[State, Result]):
    func: Callable[[State], Result]

    @override
    def extract(self, state) -> Result:
        return self.func(state)


def state_extractor[
    State, Result
](func: Callable[[State], Result]) -> StateExtractor[State, Result]:
    return _FuncStateExtractor[State, Result](func)
