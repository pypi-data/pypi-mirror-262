__all__ = [
    "BaseKyotsuError",
    "ClientKyotsuError",
]

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypedDict

from kyotsu.logging.groups import LoggingGroup
from kyotsu.logging.telemetry.contextvars import parent_span_id, span_id, trace_id
from kyotsu.utils import JsonAlias

if TYPE_CHECKING:
    from kyotsu.logging.error_codes.dataclasses import ErrorCode


class ErrorModelMapping(TypedDict, total=False):
    code: str
    details: str
    ray_id: str
    extra: Mapping[str, Any]


class BaseKyotsuError(Exception):
    error_code: "ErrorCode"
    status_code: int
    group: LoggingGroup | None
    telemetry: dict[str, str | None]
    http_headers: dict[str, str]
    extra: dict[str, JsonAlias]

    def __init__(
        self: Self,
        error_code: "ErrorCode",
        status_code: int = 500,
        group: LoggingGroup | None = None,
        *,
        _trace_id: str | None = None,
        _span_id: str | None = None,
        _parent_span_id: str | None = None,
        _http_headers: dict[str, str] | None = None,
        **extra: JsonAlias,
    ):
        self.error_code = error_code
        self.group = group
        self.status_code = status_code
        self.telemetry = {
            "trace_id": _trace_id or trace_id.get(),
            "span_id": _span_id or span_id.get(),
            "parent_span_id": _parent_span_id or parent_span_id.get(),
        }
        self.http_headers = {} if _http_headers is None else _http_headers
        self.extra = extra
        super().__init__(str(self.error_code))

    def __repr__(self: Self) -> str:
        base_str = f"{self.__class__.__name__}({self.error_code!r}"
        if self.status_code != 500:
            base_str += f", status_code={self.status_code}"
        if self.group:
            base_str += f", group={self.group}"
        if self.telemetry:
            k_v = ", ".join(f"_{k}={v}" for k, v in self.telemetry.items() if v)
            base_str += f", {k_v}"
        if self.http_headers:
            base_str += f", _http_headers={self.http_headers}"
        if self.extra:
            k_v = ", ".join(f"{k}={v!r}" for k, v in self.extra.items())
            base_str += f", {k_v}"
        return f"{base_str})"

    @property
    def response_data(self: Self) -> tuple[int, ErrorModelMapping, dict[str, str]]:
        body = ErrorModelMapping(
            code=self.error_code.code,
            details=self.error_code.message,
        )
        if self.telemetry["trace_id"]:
            body["ray_id"] = self.telemetry["trace_id"]
        return self.status_code, body, self.http_headers


class ClientKyotsuError(BaseKyotsuError):
    @property
    def response_data(self: Self) -> tuple[int, ErrorModelMapping, dict[str, str]]:
        status_code, body, http_headers = super().response_data
        if self.extra:
            body["extra"] = self.extra
        return status_code, body, http_headers
