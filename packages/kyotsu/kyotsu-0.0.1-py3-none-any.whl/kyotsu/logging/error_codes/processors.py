__all__ = [
    "error_code_adder",
]

from typing import TYPE_CHECKING

from structlog.processors import _figure_out_exc_info
from structlog.typing import EventDict, WrappedLogger

if TYPE_CHECKING:
    from kyotsu.logging.error_codes import ErrorCode


def error_code_adder(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    exc_info = _figure_out_exc_info(event_dict.get("exc_info"))

    if not exc_info or all(e is None for e in exc_info):
        return event_dict

    try:
        code: "ErrorCode" = exc_info[1].error_code  # type: ignore[attr-defined] # We are handling AttributeError
    except AttributeError:
        return event_dict

    error_details = {
        "code": code.code,
        "message": code.message,
    }

    try:
        event_dict["error_details"] |= error_details
    except KeyError:
        event_dict["error_details"] = error_details

    return event_dict
