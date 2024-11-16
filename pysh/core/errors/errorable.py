from collections.abc import Callable
from typing import Any, Optional, Type, TypeVar
from . import error

_Error = TypeVar("_Error", bound=error.Error)
_R = TypeVar("_R")


class Errorable:
    def _error(
        self,
        *args: Any,
        type: Type[_Error] = error.Error,
        **kwargs: Any,
    ) -> _Error:
        return type(
            object=self,
            *args,
            **kwargs,
        )

    def _try(
        self,
        f: Callable[[], _R],
        *args: Any,
        type: Type[_Error] = error.Error,
        **kwargs: Any,
    ) -> _R:
        try:
            return f()
        except error.Error as e:
            raise self._error(
                children=[e],
                type=type,
                *args,
                **kwargs,
            )
