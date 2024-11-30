from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar
from pysh.core.errors.errorable import Errorable

_State = TypeVar("_State")
_Result = TypeVar("_Result", covariant=True)


class Rule(Generic[_State, _Result], ABC, Errorable):
    @abstractmethod
    def __call__(self, state: _State) -> tuple[_State, _Result]: ...

    def transform[
        TransformResult
    ](
        self, func: Callable[[_Result], TransformResult]
    ) -> "transformer.Transformer[_State,TransformResult,_Result]":
        return transformer.transformer(child=self, func=func)

    def zero_or_more(self) -> "zero_or_more.ZeroOrMore[_State,_Result]":
        return zero_or_more.ZeroOrMore[_State, _Result](child=self)

    def drop_result(self) -> "Rule[_State,None]":
        return self.transform(lambda _: None)

    def as_field(
        self, name: str
    ) -> "Rule[_State,dataclass_field.DataclassFieldSetter[_Result]]":
        return self.transform(
            lambda result: dataclass_field.DataclassField[_Result](name).setter(result),
        )

    def __and__[
        RhsResult
    ](self, rhs: "Rule[_State,RhsResult]") -> "and_.And[_State,_Result|RhsResult]":
        match rhs:
            case and_.And():
                return and_.and_(self, *rhs.children)
            case Rule():
                return and_.and_(self, rhs)

    def __or__[
        RhsResult
    ](self, rhs: "Rule[_State,RhsResult]") -> "or_.Or[_State,_Result|RhsResult]":
        match rhs:
            case or_.Or():
                return or_.or_(self, *rhs.children)
            case Rule():
                return or_.or_(self, rhs)


from pysh.core.processor import transformer, zero_or_more, dataclass_field, and_, or_
