"""This module contains keeper class for uncategorized errors."""

__all__ = [
    "KyotsuKeeper",
]

from typing import Final

from kyotsu.logging.error_codes.dataclasses import ErrorCode, error_code_keeper

from ._constants import Prefix


@error_code_keeper
class KyotsuKeeper:
    """Collection of kyotsu errors.

    Danger:
        Do not add anything to this category unless you are absolutely sure in your actions.
        # ToDo: Add link to recipes
        See: [Using Error Prefix]()

    Attributes:
        ASYNC_LOGGER_IN_SYNC_CONTEXT: Async log method was passed as callable to sync context manager.
    """

    ASYNC_LOGGER_IN_SYNC_CONTEXT: Final[ErrorCode] = ErrorCode(
        Prefix.KTS,
        1
    )
