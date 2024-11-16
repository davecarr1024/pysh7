from typing import override
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.streams.stream import Stream


class Head[State: Stream, Result](Rule[State, Result]):
    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        return StateAndResult[State, Result](state.tail(), state.head())
