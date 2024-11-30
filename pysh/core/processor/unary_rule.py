from dataclasses import dataclass
from pysh.core.processor.rule import Rule


@dataclass(frozen=True, kw_only=True)
class UnaryRule[State, Result, ChildResult](Rule[State, Result]):
    child: Rule[State, ChildResult]

    def _try_child(self, state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: self.child(state))
