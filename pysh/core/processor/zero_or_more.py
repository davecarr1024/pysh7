from dataclasses import dataclass, field
from typing import MutableSequence, Sequence, override
from pysh.core.errors.error import Error
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.processor.unary_rule import UnaryRule


class ZeroOrMore[State, ChildResult](
    UnaryRule[State, Sequence[ChildResult], ChildResult]
):
    @override
    def __call__(self, state: State) -> StateAndResult[State, Sequence[ChildResult]]:
        child_results: MutableSequence[ChildResult] = []
        while True:
            try:
                child_state_and_result = self._call_child(state)
                state = child_state_and_result.state
                child_results.append(child_state_and_result.result)
            except Error:
                return StateAndResult[State, Sequence[ChildResult]](
                    state, child_results
                )
