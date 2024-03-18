import abc
from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable, Sequence
from typing import TYPE_CHECKING, Self

import structlog.stdlib
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from kyotsu.fastapi.models import ErrorModel
from kyotsu.logging.error_codes import ERROR_CODES
from kyotsu.logging.exceptions import BaseKyotsuError, ClientKyotsuError
from kyotsu.logging.telemetry.constants import SpanKind
from kyotsu.logging.telemetry.utils import generate_ray_id, log_span_started, start_telemetry
from kyotsu.logging.utils import log_exception, transform_exceptions

if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response


class BaseLoggingMiddleware(abc.ABC):
    def __init__(self: Self, log_method: Callable[..., None] | Callable[..., Awaitable[None]]):
        self.log_method = log_method

    @abc.abstractmethod
    async def __call__(
        self: Self,
        request: "Request",
        call_next: Callable[["Request"], Awaitable["Response"]],
    ) -> "Response": ...


async def handle_errors(request: "Request", call_next: Callable[["Request"], Awaitable["Response"]]) -> "Response":
    try:
        response = await call_next(request)
    except BaseKyotsuError as exc:
        status_code, body, headers = exc.response_data
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                ErrorModel(**body).model_dump(exclude_unset=True),
            ),
            headers=headers,
        )
    return response


class StartTelemetryMiddlewareBase(BaseLoggingMiddleware):
    async def __call__(
        self: Self,
        request: "Request",
        call_next: Callable[["Request"], Awaitable["Response"]],
    ) -> "Response":
        h_trace_id = request.headers.get("X-Trace-ID", generate_ray_id())
        h_span_id = request.headers.get("X-Span-ID", generate_ray_id())
        async with (
            start_telemetry(_trace_id=h_trace_id, _span_id=h_span_id),
        ):
            if request.url.path != "/ping":
                async with log_span_started(self.log_method, span_kind=SpanKind.SERVER):
                    result = await call_next(request)
            else:
                result = await call_next(request)
        return result  # noqa: RET504 # Can't move return into ctx manager: https://github.com/python/mypy/issues/7577#issuecomment-535991883


async def exceptions_transformer_middleware(
    request: "Request",
    call_next: Callable[["Request"], Awaitable["Response"]],
) -> "Response":
    try:
        async with transform_exceptions(
            skip_transform={
                BaseKyotsuError,  # Already transformed
                ClientKyotsuError,  # Already transformed
                ResponseValidationError,  # Will be transformed manually lower
                RequestValidationError,  # Will be transformed manually lower
            },
        ):
            response = await call_next(request)
    except RequestValidationError as exc:
        msg = ("Unprocessable entity in request",)
        raise ClientKyotsuError(
            ERROR_CODES.UN.REQUEST_VALIDATION_ERROR,
            status_code=422,
            validationDetails=exc.errors(),
        ) from exc
    except ResponseValidationError as exc:
        msg = ("Unprocessable entity in response",)
        raise BaseKyotsuError(
            ERROR_CODES.UN.RESPONSE_VALIDATION_ERROR,
            status_code=500,
            validation_details=exc.errors(),  # We want to log details, but avoid adding them to response
        ) from exc
    return response


class ExceptionLoggerMiddleware(BaseLoggingMiddleware):
    async def __call__(
        self: Self,
        request: "Request",
        call_next: Callable[["Request"], Awaitable["Response"]],
    ) -> "Response":
        async with log_exception(self.log_method):
            result = await call_next(request)
        return result  # noqa: RET504 # Can't move return into ctx manager: https://github.com/python/mypy/issues/7577#issuecomment-535991883


class PathLogMiddleware(BaseLoggingMiddleware):
    async def __call__(
        self: Self,
        request: "Request",
        call_next: Callable[["Request"], Awaitable["Response"]],
    ) -> "Response":
        result = await call_next(request)
        status_code = result.status_code
        method = request.method
        path = request.url.path
        if path != "/ping":
            if iscoroutinefunction(self.log_method):
                await self.log_method("Processed request", method=method, path=path, status_code=status_code)
            else:
                self.log_method("Processed request", method=method, path=path, status_code=status_code)
        return result


def get_middleware_stack(
    log_info_method: Callable[..., None] | Callable[..., Awaitable[None]],
    log_error_method: Callable[..., None] | Callable[..., Awaitable[None]],
) -> list[Callable[["Request", Callable[["Request"], Awaitable["Response"]]], Awaitable["Response"]]]:
    return [
        handle_errors,
        StartTelemetryMiddlewareBase(log_info_method),
        ExceptionLoggerMiddleware(log_error_method),
        exceptions_transformer_middleware,
        PathLogMiddleware(log_info_method)
    ]


def apply_middleware_stack(
    app: "FastAPI",
    middlewares_stack: Sequence[
        Callable[["Request", Callable[["Request"], Awaitable["Response"]]], Awaitable["Response"]]
    ],
) -> None:
    for middleware in reversed(middlewares_stack):
        app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)
