__all__ = [
    "AppMetaData",
    "MetaDataContact",
    "MetaDataLicense",
    "MetaDataServer",
    "MetaDataTag",
    "MetaDataTagExternalDocs",
    "OpenAPIMetaData",
]

from dataclasses import asdict, dataclass, field
from typing import Self

from pydantic import BaseModel

from kyotsu.utils import JsonAlias

from .routes import ContentExample, ResponseExample


@dataclass
class MetaDataContact:
    name: str | None = None
    url: str | None = None
    email: str | None = None


@dataclass
class MetaDataLicense:
    name: str
    url: str | None = None


@dataclass
class MetaDataTagExternalDocs:
    url: str
    description: str | None = None


@dataclass(frozen=True)
class MetaDataTag:
    name: str
    description: str | None = None
    externalDocs: MetaDataTagExternalDocs | None = None  # noqa: N815 # following metadata dict case


@dataclass
class MetaDataServer:
    url: str
    description: str | None = None


@dataclass
class OpenAPIMetaData:
    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = None
    contact: MetaDataContact | None = None
    license_info: MetaDataLicense | None = None

    tags: list[MetaDataTag] | None = None
    servers: list[MetaDataServer] | None = None

    @property
    def unpack(self: Self) -> dict[str, JsonAlias]:
        return asdict(self)


def _get_default_responses() -> list[ResponseExample]:
    from kyotsu.fastapi.models import ErrorModel

    return [
        ResponseExample(
            status_code="4XX",
            description="Client Error",
            model=ErrorModel,
            examples=[
                ContentExample(
                    name="Validation Error",
                    value={
                        "code": "UN0002",
                        "details": "An unknown error occurred",
                        "rayId": "dd647833-339c-4080-b7a1-bebfbd2365d0",
                        "extra": {
                            "validationDetails": [
                                {
                                    "type": "datetime_from_date_parsing",
                                    "loc": ["body", "expires_at"],
                                    "msg": (
                                        "Input should be a valid datetime or date, "
                                        "unexpected extra characters at the end of the input"
                                    ),
                                    "input": "2024-03-05TT23:35:00.323Z",
                                    "ctx": {"error": "unexpected extra characters at the end of the input"},
                                    "url": "https://errors.pydantic.dev/2.6/v/datetime_from_date_parsing",
                                },
                                {
                                    "type": "missing",
                                    "loc": ["body", "start_at"],
                                    "msg": "Field required",
                                    "input": {"key1": "value1", "key2": "value2"},
                                    "url": "https://errors.pydantic.dev/2.6/v/missing",
                                },
                            ],
                        },
                    },
                ),
                ContentExample(
                    name="Not Found Error",
                    value={
                        "code": "AB1234",
                        "details": "Instance with id 123 not found",
                        "rayId": "255a55a3-7492-45a6-b40f-27e1e2e460b4",
                    },
                ),
            ],
        ),
        ResponseExample(
            status_code="5XX",
            description="Server Error",
            model=ErrorModel,
            examples=[
                ContentExample(
                    name="Internal Server Error",
                    value={
                        "code": "UN0001",
                        "details": "An unknown error occurred",
                        "rayId": "a4f5fab3-abc0-48de-a6ff-c142fb27643b",
                        "extra": {"exception": "ZeroDivisionError"},
                    },
                ),
            ],
        ),
    ]


@dataclass
class AppMetaData:
    openapi_url: str | None = "/openapi.json"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    _responses: list[ResponseExample] | None = field(default_factory=_get_default_responses)
    responses: dict[str, dict[str, JsonAlias | type[BaseModel]]] | None = field(init=False)

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
        if self._responses is None:
            self.responses = None
        else:
            self.responses = {
                response.status_code: self._get_response_example(response) for response in self._responses
            }

    @property
    def unpack(self: Self) -> dict[str, dict[int | str, JsonAlias | BaseModel]]:
        result = asdict(self)
        del result["_responses"]
        return result
