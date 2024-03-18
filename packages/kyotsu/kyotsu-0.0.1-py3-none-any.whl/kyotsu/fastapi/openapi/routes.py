__all__ = [
    "BodyMetadataUnpack",
    "ContentExample",
    "RequestExample",
    "ResponseExample",
    "RouteData",
    "RouteMetadataUnpack",
]
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Self, TypedDict

from fastapi.openapi.models import Example
from pydantic import AnyUrl, BaseModel

from kyotsu.utils import JsonAlias


class BodyMetadataUnpack(TypedDict, total=False):
    title: str | None
    description: str | None
    openapi_examples: dict[str, Example] | None


class RouteMetadataUnpack(TypedDict, total=False):
    name: str | None
    summary: str | None
    description: str | None
    response_description: str
    tags: list[str | Enum] | None
    deprecated: bool | None
    responses: dict[str | int, dict[str, Any]] | None


@dataclass
class RequestExample:
    name: str
    summary: str
    description: str | None = None
    value: JsonAlias = None
    external_value: AnyUrl | None = None


@dataclass
class ContentExample:
    name: str
    value: JsonAlias = None


@dataclass
class ResponseExample:
    status_code: str
    description: str
    model: type[BaseModel] | None = None
    examples: list[ContentExample] | None = None


@dataclass(kw_only=True)
class RouteData:
    route_name: str | None = None
    route_summary: str | None = None
    route_description: str | None = None
    route_response_description: str = "Successful Response"
    route_tags: list[str | Enum] | None = None
    route_deprecated: bool = False
    _route_responses: list[ResponseExample] | None = None
    route_responses: dict[str | int, dict[str, JsonAlias | type[BaseModel]]] | None = field(init=False)

    body_title: str | None = None
    body_description: str | None = None
    _body_examples: list[RequestExample] | None = None
    body_openapi_examples: dict[str, Example] | None = field(init=False)

    @staticmethod
    def _get_response_example(example: ResponseExample) -> dict[str, JsonAlias | type[BaseModel]]:
        result: dict[str, JsonAlias | type[BaseModel]] = {"description": example.description}
        if example.model:
            result["model"] = example.model
        if example.examples:
            result["content"] = {
                "application/json": {
                    "examples": {content.name: {"value": content.value} for content in example.examples},
                },
            }
        return result

    def __post_init__(self: Self) -> None:
        if self._route_responses is None:
            self.route_responses = None
        else:
            self.route_responses = {
                response.status_code: self._get_response_example(response) for response in self._route_responses
            }
        if self._body_examples is None:
            self.body_openapi_examples = None
        else:
            self.body_openapi_examples = {
                example.name: Example(
                    summary=example.summary,
                    description=example.description,
                    value=example.value,
                    externalValue=example.external_value,
                )
                for example in self._body_examples
            }

    @property
    def route_metadata(self: Self) -> RouteMetadataUnpack:
        return RouteMetadataUnpack(
            name=self.route_name,
            summary=self.route_summary,
            description=self.route_description,
            response_description=self.route_response_description,
            tags=self.route_tags,
            deprecated=self.route_deprecated,
            responses=self.route_responses,
        )

    @property
    def body_metadata(self: Self) -> BodyMetadataUnpack:
        return BodyMetadataUnpack(
            title=self.body_title,
            description=self.body_description,
            openapi_examples=self.body_openapi_examples,
        )
