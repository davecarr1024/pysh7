from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, override

from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.processor.unary_rule import UnaryRule


class Transformer[State, Result, ChildResult](UnaryRule[State, Result, ChildResult]):
    @abstractmethod
    def _transform(self, child_result: ChildResult) -> Result: ...

    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        child_state_and_result = self._call_child(state)
        result = self._try(lambda: self._transform(child_state_and_result.result))
        return StateAndResult[State, Result](child_state_and_result.state, result)


@dataclass(frozen=True, kw_only=True)
class _FuncTransformer[State, Result, ChildResult](
    Transformer[State, Result, ChildResult]
):
    func: Callable[[ChildResult], Result]

    @override
    def _transform(self, child_result: ChildResult) -> Result:
        return self.func(child_result)


def transformer[
    State, Result, ChildResult
](
    *,
    child: Rule[State, ChildResult],
    func: Callable[[ChildResult], Result],
) -> Transformer[State, Result, ChildResult]:
    return _FuncTransformer[State, Result, ChildResult](
        child=child,
        func=func,
    )
