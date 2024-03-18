__all__ = [
    "OpenSearchLogProcessor",
]

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self

from opensearchpy import JSONSerializer, OpenSearch
from structlog.typing import EventDict, WrappedLogger

if TYPE_CHECKING:
    from kyotsu.config.databases import OpenSearchNoCertConnection

from ..groups import LoggingGroup


class SafeJSONSerializer(JSONSerializer):
    def default(self: Self, data: Any) -> Any:
        try:
            return super().default(data)
        except TypeError:
            return f"<<nonserializable: {data!r}>>"


class OpenSearchLogProcessor:
    def __init__(
        self: Self,
        os_settings: "OpenSearchNoCertConnection",
        log_group_index_mapping: Mapping[str, str],
        *,
        default_index: str,
    ):
        self.conn = OpenSearch(**os_settings.CONN_DICT, serializer=SafeJSONSerializer())
        self.log_group_index_mapping = log_group_index_mapping
        self.default_index = default_index

    def __call__(self: Self, _: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
        log_group = event_dict.get("group", LoggingGroup.APPLICATION)
        index_name = self.log_group_index_mapping.get(log_group, self.default_index)
        index = f"{index_name}-{datetime.datetime.now(datetime.UTC)}"
        self.conn.index(index=index, body=event_dict)
        return event_dict
