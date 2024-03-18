__all__ = [
    "parent_span_id",
    "span_id",
    "trace_id",
]

from contextvars import ContextVar

trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)
span_id: ContextVar[str | None] = ContextVar("span_id", default=None)
parent_span_id: ContextVar[str | None] = ContextVar("parent_span_id", default=None)
