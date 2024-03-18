__all__ = [
    "log_exception",
    "transform_exceptions",
]

from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable, Iterable
from types import TracebackType
from typing import Self

from kyotsu.logging.error_codes import ERROR_CODES
from kyotsu.logging.exceptions import BaseKyotsuError, ClientKyotsuError
from kyotsu.utils.contextmanagers import SyncAsyncContextDecorator


class transform_exceptions(SyncAsyncContextDecorator):  # noqa: N801 # snake_case to fit decorator and contex manager convention
    def __init__(
        self,
        *,
        skip_transform: Iterable[type[BaseException]] | None = None,
        transform_only: Iterable[type[BaseException]] | None = None,
    ) -> None:
        self.skip_transform: Iterable[type[BaseException]] = (
            skip_transform if skip_transform is not None else {BaseKyotsuError, ClientKyotsuError}
        )
        self.transform_only: Iterable[type[BaseException]] = transform_only or set()

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type:
            if exc_type in self.transform_only or (not self.transform_only and exc_type not in self.skip_transform):
                msg = f"Unhandled {exc_type.__name__} occurred"
                raise BaseKyotsuError(
                    error_code=ERROR_CODES.UN.UNHANDLED_EXCEPTION,
                ) from exc_val
            return False
        return True


class log_exception(SyncAsyncContextDecorator):  # noqa: N801 # snake_case to fit decorator and contex manager convention
    def __init__(
        self,
        log: Callable[..., None] | Callable[..., Awaitable[None]],
        *,
        skip_log: Iterable[type[BaseException]] | None = None,
        log_only: Iterable[type[BaseException]] | None = None,
    ) -> None:
        self.log = log
        self.skip_log: Iterable[type[BaseException]] = skip_log or set()
        self.log_only: Iterable[type[BaseException]] = log_only or set()

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if iscoroutinefunction(self.log):
            msg = f"Async log method '{self.log}' can't be used in sync context manager."
            raise BaseKyotsuError(error_code=ERROR_CODES.KTS.ASYNC_LOGGER_IN_SYNC_CONTEXT)
        if exc_type:
            if exc_type in self.log_only or (not self.log_only and exc_type not in self.skip_log):
                self.log(str(exc_val), exc_info=(exc_type, exc_val, exc_tb), extra=getattr(exc_val, "extra", None))
            return False
        return True

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type:
            if exc_type in self.log_only or (not self.log_only and exc_type not in self.skip_log):
                if iscoroutinefunction(self.log):
                    await self.log(
                        str(exc_val),
                        exc_info=(exc_type, exc_val, exc_tb),
                        extra=getattr(exc_val, "extra", None),
                    )
                else:
                    self.log(str(exc_val), exc_info=(exc_type, exc_val, exc_tb), extra=getattr(exc_val, "extra", None))
            return False
        return True
