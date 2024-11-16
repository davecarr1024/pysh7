from abc import ABC, abstractmethod
from typing import Callable
from pysh.core.errors.errorable import Errorable
from pysh.core.processor.state_and_result import StateAndResult


class Rule[State, Result](ABC, Errorable):
    @abstractmethod
    def __call__(self, state: State) -> StateAndResult[State, Result]: ...

    def transform[
        TransformResult
    ](
        self, func: Callable[[Result], TransformResult]
    ) -> "Transformer[State,TransformResult,Result]":
        return transformer(child=self, func=func)

    def zero_or_more(self) -> "ZeroOrMore[State,Result]":
        return ZeroOrMore[State, Result](child=self)


from pysh.core.processor.transformer import Transformer, transformer
from pysh.core.processor.zero_or_more import ZeroOrMore
