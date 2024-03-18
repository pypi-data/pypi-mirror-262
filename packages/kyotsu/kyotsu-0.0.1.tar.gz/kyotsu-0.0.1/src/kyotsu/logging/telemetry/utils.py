__all__ = [
    "generate_ray_id",
    "log_span_started",
    "nest_span_id",
    "start_telemetry",
]

import uuid
from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Self

import structlog.contextvars

from kyotsu.logging.error_codes import ERROR_CODES
from kyotsu.logging.exceptions import BaseKyotsuError
from kyotsu.logging.telemetry.constants import SpanKind, SpanStatus
from kyotsu.logging.telemetry.contextvars import parent_span_id, span_id, trace_id
from kyotsu.utils.contextmanagers import SyncAsyncContextDecorator


def generate_ray_id() -> str:
    return str(uuid.uuid4())


class start_telemetry(SyncAsyncContextDecorator):  # noqa: N801 # snake_case to fit decorator and contex manager convention
    def __init__(
        self,
        _trace_id: str | None = None,
        _span_id: str | None = None,
        _parent_span_id: str | None = None,
    ) -> None:
        self._trace_id = _trace_id
        self._span_id = _span_id
        self._parent_span_id = _parent_span_id

    def __enter__(self: Self) -> Self:
        self.trace_id_token = trace_id.set(self._trace_id or generate_ray_id())
        self.span_id_token = span_id.set(self._span_id or generate_ray_id())
        self.parent_span_id_token = None
        if self._parent_span_id:
            self.parent_span_id_token = parent_span_id.set(self._parent_span_id)

        self._structlog_tokens = structlog.contextvars.bind_contextvars(
            trace_id=trace_id.get(),
            span_id=span_id.get(),
            parent_span_id=parent_span_id.get(),
        )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        trace_id.reset(self.trace_id_token)
        span_id.reset(self.span_id_token)

        if self.parent_span_id_token:
            parent_span_id.reset(self.parent_span_id_token)

        structlog.contextvars.reset_contextvars(**self._structlog_tokens)

        return not exc_type


class nest_span_id(SyncAsyncContextDecorator):  # noqa: N801 # snake_case to fit decorator and contex manager convention
    def __enter__(self: Self) -> Self:
        self.parent_span_id_token = parent_span_id.set(span_id.get())
        self.span_id_token = span_id.set(generate_ray_id())
        self._structlog_tokens = structlog.contextvars.bind_contextvars(
            span_id=span_id.get(),
            parent_span_id=parent_span_id.get(),
        )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        parent_span_id.reset(self.parent_span_id_token)
        span_id.reset(self.span_id_token)

        structlog.contextvars.reset_contextvars(**self._structlog_tokens)

        return not exc_type


class log_span_started(SyncAsyncContextDecorator):  # noqa: N801 # snake_case to fit decorator and contex manager convention
    def __init__(
        self,
        log: Callable[..., None] | Callable[..., Awaitable[None]],
        span_kind: SpanKind,
    ):
        self.log = log
        self.span_kind = span_kind

    def __enter__(self: Self) -> Self:
        if iscoroutinefunction(self.log):
            msg = f"Async log method '{self.log}' can't be used in sync context manager."
            raise BaseKyotsuError(ERROR_CODES.KTS.ASYNC_LOGGER_IN_SYNC_CONTEXT)
        self.log("Span Started", span_kind=self.span_kind, span_status=SpanStatus.UNSET)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if iscoroutinefunction(self.log):
            msg = f"Async log method '{self.log}' can't be used in sync context manager."
            raise BaseKyotsuError(ERROR_CODES.KTS.ASYNC_LOGGER_IN_SYNC_CONTEXT)
        if exc_type:
            status, supress = SpanStatus.ERROR, False
        else:
            status, supress = SpanStatus.OK, True
        self.log("Span Ended", span_kind=self.span_kind, span_status=status)
        return supress

    async def __aenter__(self: Self) -> Self:
        if iscoroutinefunction(self.log):
            await self.log("Span Started", span_kind=self.span_kind, span_status=SpanStatus.UNSET)
        else:
            self.log("Span Started", span_kind=self.span_kind, span_status=SpanStatus.UNSET)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type:
            status, supress = SpanStatus.ERROR, False
        else:
            status, supress = SpanStatus.OK, True
        if iscoroutinefunction(self.log):
            await self.log("Span Ended", span_kind=self.span_kind, span_status=status)
        else:
            self.log("Span Ended", span_kind=self.span_kind, span_status=status)
        return supress
