from typing import MutableSequence, Sequence, override
from pysh.core.processor.nary_rule import NaryRule
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult


class And[State, ChildResult](NaryRule[State, Sequence[ChildResult], ChildResult]):
    @override
    def __call__(self, state: State) -> StateAndResult[State, Sequence[ChildResult]]:
        child_results: MutableSequence[ChildResult] = []
        for child in self:
            child_state_and_result = self._try(lambda: child(state))
            state = child_state_and_result.state
            child_results.append(child_state_and_result.result)
        return StateAndResult[State, Sequence[ChildResult]](state, child_results)


def and_[
    State, ChildResult
](*children: Rule[State, ChildResult]) -> And[State, ChildResult]:
    return And[State, ChildResult](children=list(children))
