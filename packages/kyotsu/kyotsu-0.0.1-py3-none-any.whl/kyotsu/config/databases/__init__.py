"""
This module provides the models and mix-ins necessary for configuring and maintaining the connections
to various databases across the application.

The configuration for different types of database connections are defined and standardized
in this package, ensuring the consistency and maintainability of the codebase.

Modules:
    models: Defines the models for various types of database connections used across the application.
    _types: Contains inner misc types for mixins and models.

When needing to configure a new database connection or reuse an existing common configuration across multiple services,
these modules should be the first place to look.
"""

__all__ = [
    "AmqpConnection",
    "DBConnection",
    "OpenSearchNoCertConnection",
    "PostgresConnection",
    "RedisConnection",
]

from .models import AmqpConnection, DBConnection, OpenSearchNoCertConnection, PostgresConnection, RedisConnection
