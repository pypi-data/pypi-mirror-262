__all__ = [
    "SyncAsyncContextDecorator",
]
import abc
from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable
from functools import wraps
from types import TracebackType
from typing import Any, Self


class SyncAsyncContextDecorator(abc.ABC):
    def _recreate_cm(self: Self) -> Self:
        """
        Return a recreated instance of self.

        Copied from [contextlib.ContextDecorator][].
        """
        return self

    def __call__(
        self,
        func: Callable[..., Any] | Callable[..., Awaitable[Any]],
    ) -> Callable[..., Any] | Callable[..., Awaitable[Any]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self._recreate_cm():
                return func(*args, **kwargs)

        @wraps(func)
        async def awrapper(*args: Any, **kwargs: Any) -> Any:
            async with self._recreate_cm():
                return await func(*args, **kwargs)

        if not iscoroutinefunction(func):
            return wrapper
        return awrapper

    @abc.abstractmethod
    def __enter__(self: Self) -> Self: ...

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool: ...

    async def __aenter__(self: Self) -> Self:
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        return self.__exit__(exc_type, exc_val, exc_tb)
