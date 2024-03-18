__all__ = [
    "LoggingGroup",
]

from enum import StrEnum, auto
from typing import Any


class LoggingGroup(StrEnum):
    """
    Predefined logging groups.

    This Enum is designed to generate value automatically, by replacing `_` in name wih `-` and making it lowercase.
    Always prioritize `auto()` over manual value assigment.

    Attributes:

        DEFAULT: Default logging group. Reference to APPLICATION.
        APPLICATION: Application logging group. Generic log group. Everything uncategorized should go here.
        PRODUCT: Product logging group. Used to mark product logs that are used by product analytics.
        NETWORK: Network logging group. Used to mark logs related to external services.
        DATABASE: Database logging group. Used to mark logs related to database operations.
        PERFORMANCE: Performance logging group. Used to mark logs related to performance metrics.
    """

    @staticmethod
    def _generate_next_value_(name: str, *args: Any) -> str:
        """Build group name by replacing `_` in name with `-` and making it lowercase."""
        return name.replace("_", "-").lower()

    DEFAULT = "application"
    APPLICATION = auto()
    PRODUCT = auto()
    NETWORK = auto()
    DATABASE = auto()
    PERFORMANCE = auto()
