__all__ = [
    "log_group_adder",
]

from structlog.processors import _figure_out_exc_info
from structlog.typing import EventDict, WrappedLogger

from kyotsu.logging.groups.constants import LoggingGroup


def _get_override_group_or_none(event_dict: EventDict) -> str | None:
    try:
        return str(event_dict.pop("override_group"))
    except KeyError:
        return None


def _get_exc_group_or_none(event_dict: EventDict) -> str | None:
    exc_info = _figure_out_exc_info(event_dict.get("exc_info"))

    if not exc_info or all(e is None for e in exc_info):
        return None

    return getattr(exc_info[1], "group", None)


def _get_group_or_default(event_dict: EventDict) -> str:
    return event_dict.get("group", LoggingGroup.DEFAULT)


def log_group_adder(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    event_dict["group"] = (
        _get_override_group_or_none(event_dict)  # trying to get override_group
        or _get_exc_group_or_none(event_dict)  # looking for group in exception
        or _get_group_or_default(event_dict)  # validating group in event dict or returning default group
    )
    return event_dict
