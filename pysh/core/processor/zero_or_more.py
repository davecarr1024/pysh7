from dataclasses import dataclass, field
from typing import MutableSequence, Sequence, override
from pysh.core.errors.error import Error
from pysh.core.processor.list_builder import ListBuilder
from pysh.core.processor.result_builder import ResultBuilder
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.processor.unary_rule import UnaryRule


@dataclass(frozen=True)
class ZeroOrMore[State, Result](UnaryRule[State, Sequence[Result], Result]):
    result_builder: ResultBuilder[Sequence[Result], Result] = field(
        default_factory=lambda: ListBuilder[Result]()
    )

    @override
    def __call__(self, state: State) -> StateAndResult[State, Sequence[Result]]:
        result_builder = self.result_builder.reset()
        while True:
            try:
                state_and_result = self._call_child(state)
                state = state_and_result.state
                result_builder = result_builder.add(state_and_result.result)
            except Error:
                return StateAndResult[State, Sequence[Result]](
                    state, result_builder.get()
                )
