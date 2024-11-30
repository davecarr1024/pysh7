from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, override
from pysh.core.processor import dataclass_field, rule
from pysh.core.processor.state_and_result import StateAndResult


@dataclass(frozen=True, kw_only=True)
class StateExtractor[State, ChildState, Result](rule.Rule[State, Result]):
    child: rule.Rule[ChildState, Result]

    @abstractmethod
    def _get(self, state: State) -> ChildState: ...

    def _set(self, state: State, child_state: ChildState) -> State:
        del child_state
        return state

    @override
    def __call__(self, state: State) -> StateAndResult[State, Result]:
        child_state = self._get(state)
        child_state_and_result = self._try(lambda: self.child(child_state))
        state = self._set(state, child_state_and_result.state)
        return StateAndResult[State, Result](state, child_state_and_result.result)


@dataclass(frozen=True, kw_only=True)
class _FuncStateExtractor[State, ChildState, Result](
    StateExtractor[State, ChildState, Result]
):
    get: Callable[[State], ChildState]
    set: Optional[Callable[[State, ChildState], State]] = None

    @override
    def _get(self, state: State) -> ChildState:
        return self.get(state)

    @override
    def _set(self, state: State, child_state: ChildState) -> State:
        if self.set is not None:
            return self.set(state, child_state)
        else:
            return super()._set(state, child_state)


def state_extractor[
    State, ChildState, Result
](
    *,
    get: Callable[[State], ChildState],
    set: Optional[Callable[[State, ChildState], State]] = None,
    child: rule.Rule[ChildState, Result],
) -> StateExtractor[State, ChildState, Result]:
    return _FuncStateExtractor[State, ChildState, Result](
        child=child,
        get=get,
        set=set,
    )


@dataclass(frozen=True, kw_only=True)
class DataclassFieldStateExtractor[State, ChildState, Result](
    StateExtractor[State, ChildState, Result]
):
    field: dataclass_field.DataclassField[ChildState]

    @override
    def _get(self, state: State) -> ChildState:
        return self.field.get(state)

    @override
    def _set(self, state: State, child_state: ChildState) -> State:
        return self.field.set(state, child_state)
