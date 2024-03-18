__all__ = [
    "Prefix",
]

from enum import StrEnum, auto, unique
from typing import Any


@unique
class Prefix(StrEnum):
    """Enum that keeps prefixes for [kyotsu.logging.error_codes.ErrorCode][]s.

    This Enum is designed to generate value automatically, by replacing `_` in name wih `-`.
    Always prioritize `auto()` over manual value assigment.

    Attributes:
        UN: Uncategorized Errors
        KTS: Kyotsu Runtime Errors
        SCH: Scheduler Errors
    """

    @staticmethod
    def _generate_next_value_(name: str, *args: Any) -> str:
        """Build prefix by replacing `_` in name with `-`."""
        return name.replace("_", "-")

    UN = auto()
    KTS = auto()
    SCH = auto()
