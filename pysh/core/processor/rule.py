from abc import ABC, abstractmethod
from typing import Callable, Generic, Sequence, TypeVar, Union, overload
from pysh.core.errors.errorable import Errorable
from pysh.core.processor.state_and_result import StateAndResult

_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)


class Rule(Generic[_State, _Result], ABC, Errorable):
    @abstractmethod
    def __call__(self, state: _State) -> StateAndResult[_State, _Result]: ...

    def transform[
        TransformResult
    ](
        self, func: Callable[[_Result], TransformResult]
    ) -> "Transformer[_State,TransformResult,_Result]":
        return transformer(child=self, func=func)

    def zero_or_more(self) -> "ZeroOrMore[_State,_Result]":
        return ZeroOrMore[_State, _Result](child=self)

    def drop_result(self) -> "Rule[_State,None]":
        return self.transform(lambda _: None)

    def as_field(self, name: str) -> "Rule[_State,Field[_Result]]":
        return self.transform(lambda result: Field[_Result](name, result))

    def __and__[
        RhsResult
    ](self, rhs: "Rule[_State,RhsResult]") -> "And[_State,_Result|RhsResult]":
        match rhs:
            case And():
                return and_(self, *rhs.children)
            case Rule():
                return and_(self, rhs)


from pysh.core.processor.transformer import Transformer, transformer
from pysh.core.processor.zero_or_more import ZeroOrMore
from pysh.core.processor.dataclass_builder import Field
from pysh.core.processor.and_ import and_, And
