__all__ = [
    "error_telemetry_adder",
]

from structlog.processors import _figure_out_exc_info
from structlog.typing import EventDict, WrappedLogger


def error_telemetry_adder(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    exc_info = _figure_out_exc_info(event_dict.get("exc_info"))

    if not exc_info or all(e is None for e in exc_info):
        return event_dict

    try:
        telemetry = exc_info[1].telemetry  # type: ignore[attr-defined] # We are handling AttributeError
    except AttributeError:
        return event_dict

    try:
        event_dict["error_details"] |= telemetry
    except KeyError:
        event_dict["error_details"] = telemetry

    return event_dict
