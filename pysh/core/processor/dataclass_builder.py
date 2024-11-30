import dataclasses
from typing import Sequence, Union, override

from pysh.core.processor import dataclass_field, rule, transformer

type _ChildResult = Union[dataclass_field.DataclassFieldSetter, None]
type _ChildResults = Sequence[_ChildResult]


@dataclasses.dataclass(frozen=True, kw_only=True)
class DataclassBuilder[State, Result](
    transformer.Transformer[State, Result, _ChildResults]
):
    result: Result

    @override
    def _transform(self, child_result: _ChildResults) -> Result:
        result = self.result
        for field in child_result:
            if field is not None:
                result = field.set(result)
        return result


def build_dataclass[
    State,
    Result,
](
    result: Result,
    *children: rule.Rule[State, _ChildResult],
) -> rule.Rule[
    State, Result
]:
    return DataclassBuilder[State, Result](result=result, child=and_.and_(*children))


from pysh.core.processor import and_
