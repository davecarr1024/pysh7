from dataclasses import dataclass
from pysh.core.processor.and_ import and_, and_list
from pysh.core.processor.dataclass_builder import DataclassBuilder
from pysh.core.processor.literal import Literal
from pysh.core.processor.state_and_result import StateAndResult


def test_and_list():
    assert and_list(
        Literal(1),
        Literal(2),
        Literal(3),
    )(
        None
    ).result == [1, 2, 3]


def test_and_dataclass():
    @dataclass(frozen=True, kw_only=True)
    class Object:
        i: int = 0
        s: str = ""

    assert and_(
        DataclassBuilder(Object()),
        Literal(1).as_field("i"),
        Literal(None),
        Literal("a").as_field("s"),
    )(None).result == Object(i=1, s="a")
