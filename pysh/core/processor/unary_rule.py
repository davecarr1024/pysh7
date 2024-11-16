from dataclasses import dataclass
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult


@dataclass(frozen=True, kw_only=True)
class UnaryRule[State, Result, ChildResult](Rule[State, Result]):
    child: Rule[State, ChildResult]

    def _call_child(self, state: State) -> StateAndResult[State, ChildResult]:
        return self._try(lambda: self.child(state), msg="failed to call child")
