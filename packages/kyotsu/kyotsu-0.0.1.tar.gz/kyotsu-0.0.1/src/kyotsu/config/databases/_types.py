"""
This module contains types that are used for `kyotsu.config.databases` `mixins` and `models`.

Attributes:
    ConnType: TypeVar that used for generic [`DBConnection`][kyotsu.config.databases.models.DBConnection] models.

Classes:
    AmqpQueryParams: Represents the set of query params used for AMQP connection.
    OpenSearchConnectionDict: Represents the dictionary of connection parameters needed for an OpenSearch connection.
"""

__all__ = [
    "AmqpQueryParams",
    "ConnType",
]

from collections.abc import Sequence
from ssl import SSLContext
from typing import Literal, NotRequired, TypedDict, TypeVar

ConnType = TypeVar("ConnType")
"""Type for `CONN_STR` in classes inherited from generic `DBConnection`."""


class AmqpQueryParams(TypedDict, total=False):
    """
    This `TypedDict` subclass represents the set of query parameters that can be used on an AMQP connection.

    These parameters include detailed AMQP client configurations, such as backpressure detection, retry delay,
    socket timeout and many others.

    This dict should be used as the `QUERY_PARAMS` attribute of an `AmqpConnection` instance.

    See more details at: [pika.connection.URLParameters](https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.URLParameters)
    """

    backpressure_detection: Literal["t"]
    channel_max: int
    connection_attempts: int
    frame_max: int
    heartbeat: int
    locale: str
    ssl_options: dict[str, str]
    retry_delay: int
    socket_timeout: int


class OpenSearchConnectionDict(TypedDict, total=False):
    """
    This `TypedDict` subclass represents the dictionary of connection parameters needed for an OpenSearch connection.

    It is used in the `CONN_DICT` attribute of an `OpenSearchNoCertConnection` instance after being processed in
    `assemble_conn_dict` method.

    This dict establishes details about hosts, authentication, scheme, port, and SSL context, which all will be used to
    configure and establish the OpenSearch connection.
    """

    hosts: Sequence[str]
    http_auth: tuple[str, str] | None
    scheme: Literal["http", "https"]
    port: str

    ssl_context: NotRequired[SSLContext]
    timeout: NotRequired[int]
    max_retries: NotRequired[int]
    retry_on_timeout: NotRequired[bool]
