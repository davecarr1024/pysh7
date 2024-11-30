from dataclasses import dataclass

import pytest

from pysh.core.errors.error import Error
from pysh.core.processor.dataclass_field import DataclassField, DataclassFieldSetter


@dataclass(frozen=True, kw_only=True)
class Object:
    i: int = 0
    s: str = ""


def test_field_get():
    object = Object()
    assert DataclassField[int]("i").get(object) == object.i
    assert DataclassField[str]("s").get(object) == object.s


def test_field_get_fail():
    with pytest.raises(Error):
        DataclassField[int]("i").get(int())
    with pytest.raises(Error):
        DataclassField[int]("j").get(Object())


def test_field_set():
    object = Object()
    assert DataclassField[int]("i").set(object, 1) == Object(i=1)
    assert DataclassField[str]("s").set(object, "a") == Object(s="a")


def test_setter_get():
    object = Object()
    assert (
        DataclassFieldSetter[int](
            DataclassField[int]("i"),
            1,
        ).get(object)
        == object.i
    )
    assert (
        DataclassFieldSetter[str](
            DataclassField[str]("s"),
            "a",
        ).get(object)
        == object.s
    )


def test_setter_set():
    object = Object()
    assert DataclassFieldSetter[int](
        DataclassField[int]("i"),
        1,
    ).set(
        object
    ) == Object(i=1)
    assert DataclassFieldSetter[str](
        DataclassField[str]("s"),
        "a",
    ).set(
        object
    ) == Object(s="a")
