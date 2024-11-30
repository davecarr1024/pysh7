from dataclasses import dataclass, field
from typing import MutableSequence, Sequence, override
from pysh.core.errors.error import Error
from pysh.core.processor.unary_rule import UnaryRule


class ZeroOrMore[State, ChildResult](
    UnaryRule[State, Sequence[ChildResult], ChildResult]
):
    @override
    def __call__(self, state: State) -> tuple[State, Sequence[ChildResult]]:
        child_results: MutableSequence[ChildResult] = []
        while True:
            try:
                state, result = self._try_child(state)
                child_results.append(result)
            except Error:
                return state, child_results
