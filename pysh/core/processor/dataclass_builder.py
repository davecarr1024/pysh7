import dataclasses
from typing import Sequence, override

from pysh.core.errors.errorable import Errorable
from pysh.core.processor.rule import Rule
from pysh.core.processor.transformer import Transformer


@dataclasses.dataclass(frozen=True)
class Field[Value](Errorable):
    name: str
    value: Value

    def set[Object](self, object: Object) -> Object:
        if not dataclasses.is_dataclass(object):
            raise self._error(msg=f"setting field on non-dataclass {object}")
        if not any(field.name == self.name for field in dataclasses.fields(object)):
            raise self._error(
                msg=f"trying to set unknown field {self.name} on dataclass {object}"
            )
        return dataclasses.replace(
            object,  # type: ignore
            **{self.name: self.value},
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class DataclassBuilder[State, Result](
    Transformer[State, Result, Sequence[Field | None]]
):
    result: Result

    @override
    def _transform(self, child_result: Sequence[Field | None]) -> Result:
        result = self.result
        for field in child_result:
            if field is not None:
                result = field.set(result)
        return result


def build_dataclass[
    State, Result
](result: Result, *children: Rule[State, Field | None]) -> Rule[State, Result]:
    return DataclassBuilder[State, Result](result=result, child=and_.and_(*children))


from pysh.core.processor import and_
