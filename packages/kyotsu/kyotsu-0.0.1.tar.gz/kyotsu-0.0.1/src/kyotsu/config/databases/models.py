"""
This module contains base models for defining database connection settings.

Each model class in this module represents a different type of database connection.

All classes derived from `DBConnection` that use separate properties
(`USERNAME`, `PASSWORD`, `HOST`, `PORT`, `DATABASE`) to define a connection string (`CONN_STR`) use two main methods:

- `_assemble_conn_str_value()`: an abstract method, which needs to be defined in subclasses.
It is responsible for creating the actual connection string value.

- `assemble_conn_str()`: a model validator, which checks whether `CONN_STR` is `None`.
If yes, it builds the connection string using `_assemble_conn_str_value()`.

Classes:
    DBConnection: Abstract class that can be inherited to represent different types of DB connections.
    AmqpConnection: Represents an AMQP (Advanced Message Queuing Protocol) connection.
    OpenSearchNoCertConnection: Represents an OpenSearch connection without requiring SSL certification.
    PostgresConnection: Represents a connection to a Postgres database using either asyncpg or psycopg2 scheme.
    RedisConnection: Represents a Redis database connection string with support for SSL.
"""

__all__ = [
    "AmqpConnection",
    "DBConnection",
    "OpenSearchNoCertConnection",
    "PostgresConnection",
    "RedisConnection",
]

import abc
import warnings
import urllib.parse
from typing import Annotated, Generic, Literal, Self

from pydantic import AmqpDsn, AnyHttpUrl, BaseModel, ConfigDict, PostgresDsn, RedisDsn, computed_field

from kyotsu.config.databases._types import AmqpQueryParams, ConnType, OpenSearchConnectionDict


class DBConnection(BaseModel, Generic[ConnType], abc.ABC):
    """
    This abstract base model class represents a generic database connection.

    It is designed to be inherited by subclasses that represent specific database connections.

    Subclasses must implement the `_assemble_conn_str_value` method to generate the necessary connection string
    representation for a specific database type.

    Attributes:
        USERNAME (str | None): The username for the database connection.
        PASSWORD (str | None): The password for the database connection.
        HOST (str | None): The host for the database connection.
        PORT (str | None): The port for the database connection.
        DATABASE (str | None): The specific database to connect to.
        CONN_STR (Annotated[str, ConnType]): The connection string, assembled from the other properties.
    """

    USERNAME: str | None = None
    PASSWORD: str | None = None
    HOST: str | None = None
    PORT: int | None = None
    DATABASE: str | None = None

    @computed_field
    @property
    def CONN_STR(self: Self) -> Annotated[str, ConnType]:
        """
        The connection string, assembled from the other properties.

        This attribute is computed by calling the `_assemble_conn_str_value` method.

        Returns:
            The connection string, assembled from the other properties.
        """
        return str(self._assemble_conn_str_value())

    @abc.abstractmethod
    def _assemble_conn_str_value(self: Self) -> ConnType:
        """
        Abstract method that subclasses must implement to generate a connection string representation.

        Arguments:
            self (Self): A reference to the instance of a subclass that this method will be called on.

        Returns:
            ConnType: A connection string that can be directly used by the specific type of database client
                to create a connection with the database.
        """
        ...


class AmqpConnection(DBConnection[AmqpDsn]):
    """
    Represents an AMQP (Advanced Message Queuing Protocol) connection.

    Attributes:
        USERNAME (str): The username for this AMQP service.
        PASSWORD (str): The password for this AMQP service.
        HOST (str): The host of the AMQP service.
        PORT (int): [Optional] The port of the AMQP service. Default is 5672.
        DATABASE (str): [Optional] The database for this AMQP service. Default is "%2f", a placeholder for root level.
        USE_SSL (bool): [Optional] If true, the AMQP service is assumed to use SSL. Default is True.
        QUERY_PARAMS (AmqpQueryParams | None): [Optional] Set of optional parameters for the connection,
            including backpressure detection, channel max, etc.

        CONN_STR (str): The connection string for the AMQP service, assembled from the other properties.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int = 5672
    # "%2f" value is used as default virtual host
    # https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.URLParameters
    DATABASE: str = "%2f"

    USE_SSL: bool = True
    QUERY_PARAMS: AmqpQueryParams | None = None

    def _assemble_conn_str_value(self: Self) -> AmqpDsn:
        """
        Assembles a connection string representation for an AMQP connection.

        Arguments:
            self (Self): A reference to the instance of AmqpConnection that this method will be called on.

        Returns:
            AmqpDsn: A Pydantic AMQP DSN model that represents the connection string.
        """
        scheme = "amqps" if self.USE_SSL else "amqp"
        query_params = urllib.parse.urlencode(self.QUERY_PARAMS) if self.QUERY_PARAMS else None
        return AmqpDsn.build(
            scheme=scheme,
            password=self.PASSWORD,
            host=self.HOST.split("://")[-1],
            port=self.PORT,
            path=self.DATABASE,
            query=query_params,
        )


class OpenSearchNoCertConnection(DBConnection[AnyHttpUrl]):
    """
    Represents an OpenSearch connection without requiring SSL certification.

    Attributes:
        SCHEME (Literal["http", "https"]): The scheme for this connection, either "http" or "https".
        USERNAME (str): The username for the OpenSearch service.
        PASSWORD (str): The password for the OpenSearch service.
        HOST (str): The host of the OpenSearch service.
        PORT (int): The port of the OpenSearch service.
        TTL (int): [Optional] The duration after which the connection times out. Default is 60.
        MAX_RETRIES (int): [Optional] The maximum number of times the request to the connection can be retried.
            Default is 10.
        RETRY_ON_TIMEOUT (bool): [Optional] If true, retries occur on timed-out connections. Default is True.
        CONN_DICT (OpenSearchConnectionDict): After being processed in `assemble_conn_dict`, this dict contains
                                                details about host, authentication, connectivity, and SSL context.

        CONN_STR (str): The connection string for the OpenSearch service, assembled from,
                                        assembled from the other properties.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    SCHEME: Literal["http", "https"]
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int

    TTL: int = 60
    MAX_RETRIES: int = 10
    RETRY_ON_TIMEOUT: bool = True

    @computed_field
    @property
    def CONN_DICT(self: Self) -> OpenSearchConnectionDict:
        """
        Returns dict with OpenSearch connection parameters,
        including host, scheme, port, authentication, and SSL context.

        Warns:
            ImportWarning: When opensearch-py is not installed, therefore the ssl_context can't be added.

        Returns:
            OpenSearchConnectionDict: The connection dictionary.
        """
        conn_dict = OpenSearchConnectionDict(
            hosts=(self.HOST,),
            http_auth=(self.USERNAME, self.PASSWORD) if self.USERNAME else None,
            scheme=self.SCHEME,
            port=str(self.PORT),
            timeout=self.TTL,
            max_retries=self.MAX_RETRIES,
            retry_on_timeout=self.RETRY_ON_TIMEOUT,
        )

        import ssl

        try:
            from opensearchpy.connection import create_ssl_context
        except ImportError:
            msg = "Can't add SSL context to OpenSearch Connection Dict. Make sure that opensearch-py is installed."
            warnings.warn(msg, ImportWarning, stacklevel=1)
            return conn_dict

        ssl_context = create_ssl_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        conn_dict["ssl_context"] = ssl_context
        return conn_dict

    def _assemble_conn_str_value(self: Self) -> AnyHttpUrl:
        """
        Assembles a connection string representation for an OpenSearch connection.

        Arguments:
            self (Self): A reference to the instance of `OpenSearchNoCertConnection` that this method will be called on.

        Returns:
            AnyHttpUrl: A Pydantic Http URL model (`AnyHttpUrl`) that represents the connection string.
        """
        return AnyHttpUrl.build(
            scheme=self.SCHEME,
            username=self.USERNAME,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
        )


class PostgresConnection(DBConnection[PostgresDsn]):
    """
    Represents a connection to a Postgres database.

    Attributes:
        USERNAME (str): The username for the Postgres database.
        PASSWORD (str): The password for the Postgres database.
        HOST (str): The host of the Postgres database.
        PORT (int): [Optional] The port of the Postgres database. Default is 5432.
        DATABASE (str): The name of the Postgres database.

        CONN_STR (str): The connection string for the Postgres database, assembled from the
                                       other properties.
    """

    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: int = 5432
    DATABASE: str

    def _assemble_conn_str_value(self: Self) -> PostgresDsn:
        """
        Assembles a connection string representation for a Postgres database connection.

        Arguments:
            self (Self): A reference to the instance of PostgresConnection that this method will be called on.

        Returns:
            PostgresDsn: A Pydantic Postgres DSN model that represents the connection string.
        """
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.USERNAME,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            path=self.DATABASE or "",
        )


class RedisConnection(DBConnection[RedisDsn]):
    """
    Represents a Redis database connection string.

    Attributes:
        PASSWORD (str): The password for the Redis database.
        HOST (str): The host of the Redis database.
        PORT (int): [Optional] The port for the Redis database. Default is 6379.
        DATABASE (str): [Optional] The database index for the Redis database. Default is "0".
        USE_SSL (bool): [Optional] If true, the Redis service is assumed to use SSL. Default is True.

        CONN_STR (str): The connection string for the Redis service, assembled from the other properties.
    """

    PASSWORD: str | None = None
    HOST: str
    PORT: int = 6379
    DATABASE: str = "0"

    USE_SSL: bool = True

    def _assemble_conn_str_value(self: Self) -> RedisDsn:
        """
        Assembles a connection string representation for a Redis database connection.

        Arguments:
            self (Self): A reference to the instance of RedisConnection that this method will be called on.

        Returns:
            RedisDsn: A Pydantic Redis DSN model that represents the connection string.
        """
        scheme = "rediss" if self.USE_SSL else "redis"
        return RedisDsn.build(
            scheme=scheme,
            password=self.PASSWORD,
            host=self.HOST.split("://")[-1],
            port=self.PORT,
            path=self.DATABASE or "",
        )
