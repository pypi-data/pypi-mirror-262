__all__ = [
    "AsyncTelemetryClient",
    "TelemetryClient",
]

import typing
from collections.abc import Mapping

from httpx import USE_CLIENT_DEFAULT, AsyncClient, Client, Headers, Response
from httpx._client import UseClientDefault
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
)

from kyotsu.logging.telemetry.contextvars import span_id, trace_id


def _standardize_headers(
    headers: typing.Iterable[tuple[str, str]] | typing.Iterable[tuple[bytes, bytes]],
) -> typing.Iterator[tuple[str, str]]:
    for key, value in headers:
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        yield key, value


def _update_headers(headers: HeaderTypes | None) -> Headers | dict[str, str]:
    telemetry_headers: dict[str, str] = {
        "X-Trace-ID": trace_id.get() or "",
        "X-Span-ID": span_id.get() or "",
    }
    match headers:
        case False | None:
            # headers are None or empty
            return telemetry_headers
        case Headers():
            for key, value in telemetry_headers.items():
                headers[key] = value
            return headers
        case Mapping():
            return dict(_standardize_headers(headers.items())) | telemetry_headers
        case typing.Sequence():
            return dict(_standardize_headers(headers)) | telemetry_headers


class TelemetryClient(Client):
    def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> Response:
        return super().request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=_update_headers(headers),
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
        )


class AsyncTelemetryClient(AsyncClient):
    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> Response:
        return await super().request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=_update_headers(headers),
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
        )
