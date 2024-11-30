from typing import MutableSequence, Sequence, TypeVar, override
from pysh.core.processor import nary_rule, rule

_State = TypeVar("_State")
_ChildResult = TypeVar("_ChildResult", covariant=True)


class And(nary_rule.NaryRule[_State, Sequence[_ChildResult], _ChildResult]):
    @override
    def __call__(self, state: _State) -> tuple[_State, Sequence[_ChildResult]]:
        child_results: MutableSequence[_ChildResult] = []
        for child in self:
            state, child_result = self._try(lambda: child(state))
            child_results.append(child_result)
        return state, child_results

    @override
    def __and__[
        RhsResult
    ](self, rhs: "rule.Rule[_State,RhsResult]") -> "And[_State,_ChildResult|RhsResult]":
        match rhs:
            case And():
                return and_(*self.children, *rhs.children)
            case rule.Rule():
                return and_(*self.children, rhs)


def and_[
    State, ChildResult
](*children: rule.Rule[State, ChildResult]) -> And[State, ChildResult]:
    return And[State, ChildResult](children=list(children))
