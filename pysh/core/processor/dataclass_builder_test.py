from dataclasses import dataclass

from pysh.core.processor.dataclass_builder import (
    build_dataclass,
)
from pysh.core.processor.literal import Literal


@dataclass(frozen=True, kw_only=True)
class Object:
    i: int = 0
    s: str = ""


def test_build_dataclass():
    assert build_dataclass(Object())(None).result == Object()
    assert build_dataclass(
        Object(),
        Literal(1).as_field("i"),
        Literal("a").as_field("s"),
    )(None).result == Object(i=1, s="a")
