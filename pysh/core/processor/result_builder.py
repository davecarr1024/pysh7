from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, Sequence, override
from pysh.core.errors.errorable import Errorable


class ResultBuilder[Result, ChildResult](ABC, Errorable):
    @abstractmethod
    def reset(self) -> Self: ...

    @abstractmethod
    def add(self, child_result: ChildResult) -> Self: ...

    @abstractmethod
    def get(self) -> Result: ...
