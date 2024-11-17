from dataclasses import dataclass
from typing import override

import pytest

from pysh.core.errors.error import Error
from pysh.core.processor.or_ import or_
from pysh.core.processor.rule import Rule
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.streams.stream import Stream


def test_or(subtests):
    @dataclass(frozen=True)
    class Eq(Rule[int, None]):
        value: int

        @override
        def __call__(self, state: int) -> StateAndResult[int, None]:
            if state != self.value:
                raise self._error(msg=f"got {state} expected {self.value}")
            return StateAndResult[int, None](state, None)

    for state, expected in [
        (1, 1),
        (2, 2),
        (3, None),
    ]:
        with subtests.test(state=state, expected=expected):
            rule = or_(Eq(1), Eq(2))
            if expected is None:
                with pytest.raises(Error):
                    rule(state)
            else:
                assert rule(state).state == expected
