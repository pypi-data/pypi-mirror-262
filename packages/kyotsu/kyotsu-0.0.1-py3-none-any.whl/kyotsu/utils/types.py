__all__ = [
    "JsonAlias",
]

from collections.abc import Mapping, Sequence
from typing import TypeAlias

JsonBasics: TypeAlias = str | int | float | bool | None  # noqa: UP040 # MyPy 1.8.0 does not support type keyword yet
JsonAlias: TypeAlias = JsonBasics | Sequence["JsonAlias"] | Mapping[str, "JsonAlias"]  # noqa: UP040 # MyPy 1.8.0 does not support type keyword yet
