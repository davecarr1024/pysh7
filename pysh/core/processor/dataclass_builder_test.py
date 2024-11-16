from dataclasses import dataclass

from pysh.core.processor.dataclass_builder import DataclassBuilder, Field


@dataclass(frozen=True)
class Object:
    i: int
    s: str


def test_field():
    assert Field("i", 2).set(Object(1, "a")) == Object(2, "a")


def test_dataclass_builder():
    assert DataclassBuilder(
        Object(1, "a"),
    ).reset().add(
        Field("i", 2),
    ).add(
        Field("s", "b"),
    ).get() == Object(2, "b")
