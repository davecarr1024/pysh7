from typing import MutableSequence, Sequence, TypeVar, override
from pysh.core.processor.nary_rule import NaryRule
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult

_State = TypeVar("_State")
_ChildResult = TypeVar("_ChildResult", covariant=True)


class And(NaryRule[_State, Sequence[_ChildResult], _ChildResult]):
    @override
    def __call__(self, state: _State) -> StateAndResult[_State, Sequence[_ChildResult]]:
        child_results: MutableSequence[_ChildResult] = []
        for child in self:
            child_state_and_result = self._try(lambda: child(state))
            state = child_state_and_result.state
            child_results.append(child_state_and_result.result)
        return StateAndResult[_State, Sequence[_ChildResult]](state, child_results)

    @override
    def __and__[
        RhsResult
    ](self, rhs: "Rule[_State,RhsResult]") -> "And[_State,_ChildResult|RhsResult]":
        match rhs:
            case And():
                return and_(*self.children, *rhs.children)
            case Rule():
                return and_(*self.children, rhs)


def and_[
    State, ChildResult
](*children: Rule[State, ChildResult]) -> And[State, ChildResult]:
    return And[State, ChildResult](children=list(children))
