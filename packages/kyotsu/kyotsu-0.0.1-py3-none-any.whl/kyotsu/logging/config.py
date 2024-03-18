__all__ = [
    "configure_logger",
]

import logging
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

import structlog

from kyotsu.logging.error_codes.processors import error_code_adder
from kyotsu.logging.groups.processors import log_group_adder
from kyotsu.logging.opensearch.processors import OpenSearchLogProcessor
from kyotsu.logging.telemetry.processors import error_telemetry_adder

if TYPE_CHECKING:
    from kyotsu.config.databases import OpenSearchNoCertConnection


def _extract_from_record(
    _: structlog.typing.WrappedLogger,
    __: str,
    event_dict: structlog.typing.EventDict,
) -> structlog.typing.EventDict:
    """
    Processor that will try to extract `thread_name` and `process_name`
    from uvicorn logger, and add them to `event_dict`.
    """
    try:
        record = event_dict["_record"]
    except KeyError:
        return event_dict
    try:
        event_dict["thread_name"] = record.getattr("threadName", event_dict.get("thread_name", "n/a"))
        event_dict["process_name"] = record.getattr("processName", event_dict.get("thread_name", "n/a"))
    except AttributeError:
        return event_dict
    return event_dict


def _apply_to_default_logging(shared_processors: Sequence[structlog.typing.Processor], *, is_dev: bool) -> None:
    """
    Apply structlog logging to default loggers.

    Attributes:
        shared_processors: Previously configured processors chain.
        is_dev: Whether to use [structlog.dev.ConsoleRenderer][] or [structlog.processors.JSONRenderer][] for rendering.
    """
    handler = logging.StreamHandler()

    processors: list[structlog.typing.Processor] = [
        _extract_from_record,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]

    if is_dev:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    else:
        processors.append(structlog.processors.JSONRenderer())

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=processors,
    )

    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    from celery.utils.log import get_task_logger
    celery_logger = get_task_logger("celery.consumer")
    celery_logger.addHandler(handler)
    celery_logger.setLevel(logging.INFO)



def configure_logger(
    *,
    is_dev: bool,
    opensearch_config: "OpenSearchNoCertConnection",
    log_group_index_mapping: Mapping[str, str] | None,
    default_index: str,
    async_only: bool = False,
    cached_logger: bool = False,
) -> None:
    """
    Configure structlog logger.

    This method should be called in that main application file,
    so on app start-up per se.

    Attributes:
        is_dev: True if you're running project locally (doesn't mean `dev` stage).
        opensearch_config: OpenSearch connection config.
        log_group_index_mapping: Mapping of log groups to their respective indices in OpenSearch.
                                 You can keep it None, if you want to fallback on default index only.
        default_index: Default index to use for logs, if log group not found in mapping.
        async_only: Whether to use [structlog.stdlib.AsyncBoundLogger][] logger or not.
        cached_logger: Whether to cache logger or not.
                       (If you are planing to reconfigure logger or use it with multiprocessing keep it `False`)

    Processors:
        Chain of processors used by logger after configuration.

        | Processor | Definition | Description |
        | :-------- | :--------- | :---------- |
        | `timestamper` | [structlog.processors.TimeStamper][] | Add ISO UTC timestamp |
        | `event_to_msg` | [structlog.processors.EventRenamer][] | Rename `event` ro `msg` and then `_event` to `event` |
        | `add_log_level` | [structlog.stdlib.add_log_level][] | Add log level (info, warning, error, etc.) |
        | `add_logger_name` | [structlog.stdlib.add_logger_name][] | Add logger name (passed on initialization) |
        | `set_exc_info` | [structlog.dev.set_exc_info][] | If log_level is `exception` set `exc_info` to `True` |
        | `merge_contextvars` | [structlog.contextvars.merge_contextvars][] | Merge contextvars to `event_dict` (support for bindable loggers). Mainly used for [kyotsu.logging.telemetry.utils][] dcontext managers and decorators |
        | `CallsiteParameter` | [structlog.processors.CallsiteParameterAdder][] | Add `pathname`, `filename`, `func_name`, `thread`, `thread_name`, `process`, `process_name` parameters to `event_dict` |
        | `error_code_adder` | [kyotsu.logging.error_codes.processors.error_code_adder][] | Try to extract error code from [kyotsu.logging.exceptions.BaseKyotsuError][] and add it to `event_dict.error_details` |
        | `log_group_adder` | [kyotsu.logging.groups.processors.log_group_adder][] | Set `group` parameter to `event_dict`. The priority of sources are:  `event_dict` `override_group` parameter; [kyotsu.logging.exceptions.BaseKyotsuError][] `group` parameter; `event_dict` `group` parameter; default group |
        | `error_telemetry_adder` | [kyotsu.logging.telemetry.processors.error_telemetry_adder][] | Try to extract telemetry from [kyotsu.logging.exceptions.BaseKyotsuError][] and add it to `event_dict.error_details` |
        | `ExtraAdder` | [structlog.stdlib.ExtraAdder][] | Unpack `event_dict.extra` to `event_dict` |
        | `dict_tracebacks` | [structlog.processors.dict_tracebacks][] | If `is_dev` is `False` - convert exceptions to suitable for [kyotsu.logging.opensearch.processors.OpenSearchLogProcessor][] and [structlog.processors.JSONPrenderer][] dicts |
        | `OpenSearchLogProcessor` | [kyotsu.logging.opensearch.processors.OpenSearchLogProcessor][] | If `is_dev` is `False` - Send logs to OpenSearch |
        | `ProcessorFormatter.wrap_for_formatter` | [structlog.stdlib.ProcessorFormatter.wrap_for_formatter][] | Wrap logger with `ProcessorFormatter`. Added to support functionality of wrapping classic logger |
        | `_extract_from_record` | [kyotsu.logging.config._extract_from_record][] | Extract `thread_name` and `process_name` from `_record` and add them to `event_dict`. Added to support uvicorn loggers |
        | `ProcessorFormatter.remove_processors_meta` | [structlog.stdlib.ProcessorFormatter.remove_processors_meta][] | Remove `_processors_meta` from `event_dict`. Added to support functionality of wrapping classic logger |
        | `renderer` | [structlog.dev.ConsoleRenderer][] &#124; [structlog.processors.JSONRenderer][] | Use pretty [structlog.dev.ConsoleRenderer][] when `is_dev` is `True`. [structlog.processors.JSONRenderer][] otherwise |
    """
    _log_group_index_mapping: Mapping[str, str] = log_group_index_mapping or {}

    timestamper = structlog.processors.TimeStamper(fmt="ISO", utc=True)
    event_to_msg = structlog.processors.EventRenamer("msg", "_event")

    shared_processors: list[structlog.typing.Processor] = [
        timestamper,  # Add ISO UTC timestamp
        event_to_msg,  # Rename `event` ro `msg` and then `_event` to `event`
        structlog.stdlib.add_log_level,  # Add log level (info, warning, error, etc.)
        structlog.stdlib.add_logger_name,  # Add logger name (passed on initialization)
        structlog.dev.set_exc_info,  # If log_level is `exception` set `exc_info` to `True`
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder({
            structlog.processors.CallsiteParameter.PATHNAME,
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.THREAD,
            structlog.processors.CallsiteParameter.THREAD_NAME,
            structlog.processors.CallsiteParameter.PROCESS,
            structlog.processors.CallsiteParameter.PROCESS_NAME,
        }),
        error_code_adder,
        log_group_adder,
        error_telemetry_adder,
        structlog.stdlib.ExtraAdder(),
    ]

    if not is_dev:
        shared_processors.extend([
            structlog.processors.dict_tracebacks,
            OpenSearchLogProcessor(opensearch_config, _log_group_index_mapping, default_index=default_index),
        ])

    shared_processors.append(structlog.stdlib.ProcessorFormatter.wrap_for_formatter)

    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.stdlib.AsyncBoundLogger if async_only else structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=cached_logger,
    )

    _apply_to_default_logging(shared_processors, is_dev=is_dev)
