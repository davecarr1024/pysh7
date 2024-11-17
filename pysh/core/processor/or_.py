from typing import MutableSequence, TypeVar, override
from pysh.core.errors.error import Error
from pysh.core.processor import nary_rule, rule, state_and_result

_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)


class Or(nary_rule.NaryRule[_State, _Result, _Result]):
    @override
    def __call__(
        self, state: _State
    ) -> state_and_result.StateAndResult[_State, _Result]:
        errors: MutableSequence[Error] = []
        for child in self:
            try:
                return child(state)
            except Error as e:
                errors.append(e)
        raise self._error(children=errors)

    @override
    def __or__[
        RhsResult
    ](self, rhs: "rule.Rule[_State,RhsResult]") -> "Or[_State,_Result|RhsResult]":
        match rhs:
            case Or():
                return or_(*self.children, *rhs.children)
            case rule.Rule():
                return or_(*self.children, rhs)


def or_[State, Result](*children: rule.Rule[State, Result]) -> Or[State, Result]:
    return Or[State, Result](children=list(children))
