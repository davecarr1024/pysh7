from typing import MutableSequence, Sequence, override
from pysh.core.errors.error import Error
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.processor.unary_rule import UnaryRule


class ZeroOrMore[State, Result](UnaryRule[State, Sequence[Result], Result]):
    @override
    def __call__(self, state: State) -> StateAndResult[State, Sequence[Result]]:
        results: MutableSequence[Result] = []
        while True:
            try:
                state_and_result = self._call_child(state)
                state = state_and_result.state
                results.append(state_and_result.result)
            except Error:
                return StateAndResult[State, Sequence[Result]](state, results)
