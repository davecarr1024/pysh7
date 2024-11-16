from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Iterator, Optional, Sized, override


@dataclass(
    frozen=True,
    kw_only=True,
    repr=False,
)
class Error[Errorable: "errorable.Errorable"](
    Exception,
    Sized,
    Iterable["Error"],
):
    object: Errorable
    msg: Optional[str] = None
    children: Sequence["Error"] = field(default_factory=list)

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator["Error"]:
        return iter(self.children)

    @override
    def __repr__(self) -> str:
        return self._repr()

    def _repr(self, indent: int = 0) -> str:
        return "\n".join(
            [
                f"{'  '*indent}{self._repr_line()}",
                *[child._repr(indent + 1) for child in self],
            ],
        )

    def _repr_line(self) -> str:
        def format_field(key: str, value: Any) -> str:
            return f"{key}={value}"

        def format_fields(items: dict[str, Any]) -> str:
            return f"{', '.join(format_field(key,value) for (key, value) in items.items() if key != 'children')}"

        return f"{self.name()}({format_fields(asdict(self))})"


from . import errorable
