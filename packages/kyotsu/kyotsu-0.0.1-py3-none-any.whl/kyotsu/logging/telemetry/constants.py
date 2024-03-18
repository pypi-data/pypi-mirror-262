__all__ = [
    "SpanKind",
    "SpanStatus",
]

from enum import StrEnum, unique


@unique
class SpanKind(StrEnum):
    """
    https://opentelemetry.io/docs/concepts/signals/traces/#span-kind
    """

    CLIENT = "CLIENT"
    SERVER = "SERVER"
    INTERNAL = "INTERNAL"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


@unique
class SpanStatus(StrEnum):
    """
    https://opentelemetry.io/docs/concepts/signals/traces/#span-status
    """

    UNSET = "Unset"
    OK = "Ok"
    ERROR = "Error"
