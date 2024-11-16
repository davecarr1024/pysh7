from dataclasses import dataclass
from typing import Sequence, override
from pysh.core.processor.list_builder import ListBuilder
from pysh.core.processor.nary_rule import NaryRule
from pysh.core.processor.result_builder import ResultBuilder
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult


@dataclass(frozen=True, kw_only=True)
class And[State, Result, ChildResult](NaryRule[State, Result, ChildResult]):
    result_builder: ResultBuilder[Result, ChildResult]

    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        result_builder = self.result_builder.reset()
        for child in self:
            child_state_and_result = self._try(
                lambda: child(state),
                msg=f"failed to call child {child}",
            )
            state = child_state_and_result.state
            result_builder = result_builder.add(child_state_and_result.result)
        return StateAndResult[State, Result](state, result_builder.get())


def and_[
    State, Result, ChildResult
](
    result_builder: ResultBuilder[Result, ChildResult],
    *children: Rule[State, ChildResult],
) -> And[State, Result, ChildResult]:
    return And[State, Result, ChildResult](
        children=list(children),
        result_builder=result_builder,
    )


def and_list[
    State, ChildResult
](*children: Rule[State, ChildResult]) -> And[
    State, Sequence[ChildResult], ChildResult
]:
    return and_(ListBuilder[ChildResult](), *children)
