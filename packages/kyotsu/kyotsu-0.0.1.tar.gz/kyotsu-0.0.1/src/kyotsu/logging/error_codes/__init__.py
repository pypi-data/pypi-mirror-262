"""This module contains all possible error codes used across microservices.

The intention is to avoid error codes duplication, standardize categories, provide messages and descriptions
through enums and dataclasses.

These error codes are not intended to be reused several times, and it's better
to create a separate error for every exception handling/raise. With that it's much easier to debug the application.

Classes:
    ErrorCodesKeeper: Dataclass for all error codes.

Attributes:
    ERROR_CODES: Constant entrypoint to all existing error codes.

"""

__all__ = [
    "ERROR_CODES",
    "ErrorCode",
    "ErrorCodesKeeper",
    "Prefix",
    "error_code_keeper",
]

from typing import Final

from kyotsu.logging.error_codes.dataclasses import ErrorCode, error_code_keeper
from kyotsu.logging.error_codes.definitions import ErrorCodesKeeper, Prefix

ERROR_CODES: Final[ErrorCodesKeeper] = ErrorCodesKeeper()
"""An entrypoint to the ✨error codes world✨. Keeps all error codes."""
