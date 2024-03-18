"""
The `kyotsu.config.base` module provides a base settings configuration class for the application.
This class ensures a uniform way to manage configurations including environment variables across the
entire application, contributing to the maintenance and consistency of the codebase.

Classes:
    BaseSettings: An abstract class that encapsulates the base configuration settings for models using
                  the Pydantic settings configuration approach.
"""

__all__ = [
    "BaseSettings",
]

from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticSettings):
    """
    A base settings configuration class that simplifies environment-based settings for Pydantic models.

    It includes environmental settings specified as '__'-separated nested properties and the encoding
    for .env files is 'utf-8'.

    Attributes:
        IS_DEV: A boolean flag indicating whether the application is running in development mode.
        model_config (SettingsConfigDict): Configuration dictionary for the settings model.
                                           It sets the delimiter and encoding standard for environment variables.
    """

    IS_DEV: bool = False

    model_config = SettingsConfigDict(
        extra="allow",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
    )
