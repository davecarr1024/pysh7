from dataclasses import dataclass
from pysh.core.processor.and_ import and_
from pysh.core.processor.dataclass_builder import DataclassBuilder
from pysh.core.processor.literal import Literal
from pysh.core.processor.state_and_result import StateAndResult


def test_and_list():
    assert and_(
        Literal(1),
        Literal(2),
        Literal(3),
    )(
        None
    ).result == [1, 2, 3]
