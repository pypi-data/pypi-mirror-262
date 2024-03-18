"""This module contains keeper class for uncategorized errors."""

__all__ = [
    "UncategorizedKeeper",
]

from typing import Final

from kyotsu.logging.error_codes.dataclasses import ErrorCode, error_code_keeper

from ._constants import Prefix


@error_code_keeper
class UncategorizedKeeper:
    """Collection of uncategorized errors.

    Danger:
        Do not add anything to this category unless you are absolutely sure in your actions.
        # ToDo: Add link to recipes
        See: [Using Error Prefix]()

    Attributes:
        UNHANDLED_EXCEPTION: Error code that indicates previously unhandled exception.
    """

    UNHANDLED_EXCEPTION: Final[ErrorCode] = ErrorCode(
        Prefix.UN,
        1
        # _dev_description=(
        #     "Unhandled error has occurred. Please consider validating an error source and add error handler."
        # ),
        # _hp_description="Something bad happened. Please contact developers for further investigation.",
    )

    REQUEST_VALIDATION_ERROR: Final[ErrorCode] = ErrorCode(
        Prefix.UN,
        2,
        message="Unprocessable entity in request",
        # _dev_description=(
        #     "FastAPI request validation error has occurred. "
        #     "Consider validating request/query params/etc. over pydantic models."
        # ),
        # _hp_description=(
        #     "At some point of Frontend-to-Service or Service-to-Service communication "
        #     "some part of request/query params/etc. appeared inconsistent with API contract. "
        #     "This can be caused by incorrect user input or by poor API contract handling. "
        #     "Send this log to dev team for further investigation."
        # ),
    )

    RESPONSE_VALIDATION_ERROR: Final[ErrorCode] = ErrorCode(
        Prefix.UN,
        3,
        # _dev_description=(
        #     "FastAPI response validation error has occurred. Consider validating response. over pydantic models."
        # ),
        # _hp_description=(
        #     "At some point backend returned invalid response (inconsistent with API contract). "
        #     "Send this log to dev team for further investigation."
        # ),
    )
