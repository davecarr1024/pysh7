import dataclasses
from typing import override

from pysh.core.errors.errorable import Errorable
from pysh.core.processor.result_builder import ResultBuilder


@dataclasses.dataclass(frozen=True)
class Field[Value](Errorable):
    name: str
    value: Value

    def set[Result](self, result: Result) -> Result:
        if not dataclasses.is_dataclass(result):
            raise self._error(msg=f"setting field on non-dataclass {result}")
        if not any(field.name == self.name for field in dataclasses.fields(result)):
            raise self._error(
                msg=f"trying to set unknown field {self.name} on dataclass {result}"
            )
        return dataclasses.replace(
            result,  # type: ignore
            **{self.name: self.value},
        )


@dataclasses.dataclass(frozen=True)
class DataclassBuilder[Result](ResultBuilder[Result, Field | None]):
    result: Result

    @override
    def reset(self) -> "DataclassBuilder[Result]":
        return DataclassBuilder[Result](
            dataclasses.replace(
                self.result,  # type: ignore
            ),
        )

    @override
    def add(self, child_result: Field | None) -> "DataclassBuilder[Result]":
        match child_result:
            case Field():
                return DataclassBuilder[Result](child_result.set(self.result))
            case None:
                return self

    @override
    def get(self) -> Result:
        return self.result
