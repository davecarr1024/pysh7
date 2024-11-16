from abc import ABC, abstractmethod
from typing import Self
from pysh.core.errors.errorable import Errorable


class ResultBuilder[Result, ChildResult](ABC, Errorable):
    @abstractmethod
    def add(self, result: ChildResult) -> Self: ...

    @abstractmethod
    def get(self) -> Result: ...
