"""
This module contains base models for defining application settings involving HTTP and gRPC services.

These models should be used in a nested manner with [`BaseSettings`][kyotsu.config.base.BaseSettings] class.

Example:
    ```python3
    >>> from kyotsu.config import BaseSettings, HttpService, GrpcService, HttpGrpcService

    >>> class Settings(BaseSettings):
    ...     EXTERNAL_HTTP_SERVICE_NAME: HttpService
    ...     EXTERNAL_GRPC_SERVICE_NAME: GrpcService
    ...     EXTERNAL_HTTP_GRPC_SERVICE_NAME: HttpGrpcService

    ```

In the above example, `EXTERNAL_HTTP_SERVICE_NAME`, `EXTERNAL_GRPC_SERVICE_NAME`, and `EXTERNAL_HTTP_GRPC_SERVICE_NAME`
will contain the configuration for each respective service type.

Classes:
    HttpService: Defines and validates the HTTP_URL attribute representing the URL for HTTP communication
                 with a service.
    GrpcService: Defines and validates the GRPC_HOST and GRPC_PORT attributes required for GRPC communication
                 with a service.
    HttpGrpcService: A combination of HttpService and GrpcService, for services that offer both
                     HTTP and GRPC interfaces.
"""

__all__ = [
    "GrpcService",
    "HttpGrpcService",
    "HttpService",
]

from typing import Annotated

from pydantic import BaseModel, HttpUrl


class HttpService(BaseModel):
    """
    This class represents the standard attributes for a service that interacts via HTTP.

    Attributes:
        HTTP_URL: The URL for the HTTP service.
    """

    HTTP_URL: Annotated[str, HttpUrl]


class GrpcService(BaseModel):
    """
    This class represents the standard attributes for a service that interacts via gRPC.

    Attributes:
        GRPC_HOST: The host for the gRPC service.
        GRPC_PORT: The port for the gRPC service.
    """

    GRPC_HOST: str
    GRPC_PORT: str


class HttpGrpcService(HttpService, GrpcService):
    """
    A combined service class that possesses both HTTP and gRPC attributes.

    Attributes:
        HTTP_URL: The URL for the HTTP service.
        GRPC_HOST: The host for the gRPC service.
        GRPC_PORT: The port for the gRPC service.
    """
