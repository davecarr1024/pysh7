from typing import MutableSequence, override
from pysh.core.errors.error import Error
from pysh.core.processor import nary_rule, rule, state_and_result


class Or[State, Result](nary_rule.NaryRule[State, Result, Result]):
    @override
    def __call__(self, state: State) -> state_and_result.StateAndResult[State, Result]:
        errors: MutableSequence[Error] = []
        for child in self:
            try:
                return child(state)
            except Error as e:
                errors.append(e)
        raise self._error(children=errors)


def or_[State, Result](*children: rule.Rule[State, Result]) -> Or[State, Result]:
    return Or[State, Result](children=list(children))
