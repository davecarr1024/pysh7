import dataclasses
from typing import Any

from pysh.core.errors.errorable import Errorable


@dataclasses.dataclass(frozen=True)
class DataclassField[Value](Errorable):
    name: str

    def _assert_is_dataclass(self, object: Any):
        if not dataclasses.is_dataclass(object):
            raise self._error(msg=f"non-dataclass {object}")

    def _assert_has_field(self, object: Any):
        if not any(field.name == self.name for field in dataclasses.fields(object)):
            raise self._error(msg=f"unknown field {self.name} in dataclass {object}")

    def _validate(self, object: Any):
        self._assert_is_dataclass(object)
        self._assert_has_field(object)

    def get(self, object: Any) -> Value:
        self._validate(object)
        return getattr(object, self.name)

    def set[Object](self, object: Object, value: Value) -> Object:
        self._validate(object)
        return dataclasses.replace(
            object,  # type: ignore
            **{self.name: value},
        )

    def setter(self, value: Value) -> "DataclassFieldSetter[Value]":
        return DataclassFieldSetter[Value](self, value)


@dataclasses.dataclass(frozen=True)
class DataclassFieldSetter[Value]:
    field: DataclassField[Value]
    value: Value

    def get(self, object: Any) -> Value:
        return self.field.get(object)

    def set[Object](self, object: Object) -> Object:
        return self.field.set(object, self.value)
