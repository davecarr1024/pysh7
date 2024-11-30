from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, override

from pysh.core.processor.rule import Rule
from pysh.core.processor.unary_rule import UnaryRule


class Transformer[State, Result, ChildResult](UnaryRule[State, Result, ChildResult]):
    @abstractmethod
    def _transform(self, child_result: ChildResult) -> Result: ...

    @override
    def __call__(self, state: State) -> tuple[State, Result]:
        state, child_result = self._try_child(state)
        result = self._try(lambda: self._transform(child_result))
        return state, result


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
