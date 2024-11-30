from typing import override
from pysh.core.processor.rule import Rule
from pysh.core.streams.stream import Stream


class Head[State: Stream, Result](Rule[State, Result]):
    @override
    def __call__(self, state: State) -> tuple[State, Result]:
        return state.tail(), state.head()
