"""
This module defines `ErrorCode` class and `error_code_keeper` decorator
to handle application errors efficiently.


Classes:
    ErrorCode: A dataclass representing a structured error code that includes several descriptions useful for
               different audiences such as end user, developers, and support staff.

Methods:
    error_code_keeper: A decorator that creates a class that contains all error codes.


Example:
    Example of creating your error codes and keepers.

    ```python
    from kyotsu.logging.error_codes import Prefix

    @error_code_keeper
    class AD_CErrorCodes:
        ZERO_DIVISION_ERROR: Final[ErrorCode] = ErrorCode(
            _code=1000,
            _prefix=Prefix.AD_C,
            _message="Divider can't be zero, please try another number",
            _dev_description="Handled ZeroDivisionError exception caused by user input.",
            _hp_description="User tried to divide by zero. The zero shouldn't be entered as a divider.",
        )

    @error_code_keeper
    class SCHErrorCodes:
        EXTERNAL_SERVICE_ERROR: Final[ErrorCode] = ErrorCode(
            1001,
            Prefix.SCH,
            _dev_description="EXTERNAL_SERVICE returned an error. Check service logs for more details.",
            _hp_description="Error occurred during services communication. Raise a request for the dev team.",
        )

    @error_code_keeper
    class MixedErrorCodes:
        AD_C: Final[AD_CErrorCodes] = AD_CErrorCodes()
        SCH: Final[SCHErrorCodes] = SCHErrorCodes()

    ERROR_CODES: Final[MixedErrorCodes] = MixedErrorCodes()
    ```
"""

__all__ = [
    "ErrorCode",
    "error_code_keeper",
]

import dataclasses
from collections.abc import Hashable
from enum import StrEnum
from typing import Self, TypeVar


@dataclasses.dataclass(
    slots=True,
    frozen=True,
    eq=True,
)
class ErrorCode:
    """This class is used to define an error code and use it later in the application.

    Attributes:
        _prefix: A prefix for categorization error.
        _code: A numeric code for the error, should be >= 1.
        message: An error message that can be displayed to the user.
                  If the error is not designed for the end user keep the default value.
        code: A property that should be used to obtain full error code. Combination of `_prefix` and `_code` attributes.


    Example:
        Fully initialized
        ```python3
            >>> error = ErrorCode("A", 1, "Some Error Message")
            >>> error
            ErrorCode(_prefix='A', _code=1, message='Some Error Message')
            >>> error.code
            'A0001'
            >>> str(error)
            'A0001: Some Error Message'

        ```

        Fallback to default values
        ```python3
        >>> error = ErrorCode("B", 11)
        >>> error
        ErrorCode(_prefix='B', _code=11, message='An unknown error has occurred')
        >>> error.code
        'B0011'
        >>> str(error)
        'B0011: An unknown error has occurred'

        ```

        The class is frozen and can't be modified after initialization.
        ```python3
        >>> error = ErrorCode("C", 2222)
        >>> error._code = 2
        Traceback (most recent call last):
        dataclasses.FrozenInstanceError: ...

        ```

        The `ErrorCode` is [Hashable][collections.abc.Hashable],
        therefore you can use any instance as a dictionary key,
        if you need it for some reason.
        ```python3
        >>> error = ErrorCode("D", 333)
        >>> d = {error: error.code}
        >>> d[error]
        'D0333'

        ```
    """

    _prefix: str | StrEnum
    _code: int
    message: str = "An unknown error has occurred"

    @property
    def code(self: Self) -> str:
        """Concatenate `self._prefix` and `self._code`."""
        return f"{self._prefix}{self._code:0>4}"

    def __str__(self: Self) -> str:
        return f"{self.code}: {self.message}"


_T = TypeVar("_T")

t = Hashable


def error_code_keeper(__cls: type[_T]) -> type[_T]:
    """A decorator that creates a dataclass with `init=False` and `frozen=True`.

    Should be used to create error keepers and store [kyotsu.logging.error_codes.ErrorCode][]s.

    Attributes:
        __cls (type[_T]): Decorated class that should be augmented with dataclass methods

    Returns:
        A dataclass with `init=False` and `frozen=True`.

    Example:
        Using `@error_code_keeper` decorator to create new keeper.

        ```python3
        >>> from kyotsu.logging.error_codes.dataclasses import error_code_keeper, ErrorCode
        >>> from typing import Final

        >>> @error_code_keeper
        ... class BErrorKeeper:
        ...     UNEXPECTED_FOR_B: Final[ErrorCode] = ErrorCode("B", 1, "Unknown error in B context")

        >>> @error_code_keeper
        ... class AErrorKeeper:
        ...     UNEXPECTED_FOR_A: Final[ErrorCode] = ErrorCode("A", 1, "Unknown error in A context")

        >>> @error_code_keeper
        ... class ErrorKeeper:
        ...     GENERIC_UNEXPECTED: Final[ErrorCode] = ErrorCode("UN", 1)
        ...     B: Final[BErrorKeeper] = BErrorKeeper()
        ...     A: Final[AErrorKeeper] = AErrorKeeper()

        >>> ERROR_CODES = ErrorKeeper()

        >>> ERROR_CODES.GENERIC_UNEXPECTED
        ErrorCode(_prefix='UN', _code=1, message='An unknown error has occurred')
        >>> ERROR_CODES.B.UNEXPECTED_FOR_B
        ErrorCode(_prefix='B', _code=1, message='Unknown error in B context')
        >>> ERROR_CODES.A.UNEXPECTED_FOR_A
        ErrorCode(_prefix='A', _code=1, message='Unknown error in A context')

        ```
    """
    return dataclasses.dataclass(init=False, frozen=True)(__cls)
