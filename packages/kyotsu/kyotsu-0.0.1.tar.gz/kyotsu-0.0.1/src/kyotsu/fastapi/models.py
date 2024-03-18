from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ErrorModel(BaseModel):
    code: str = Field(
        ...,
        title="Error code",
        description="Error code according to error codes DB.",
        examples=["UN0001", "UN0002"],
    )
    details: str | None = Field(
        None,
        title="Error details",
        description="Error details (message) available to end user.",
        examples=["Unknown error has occurred", "Request Validation Error"],
    )
    ray_id: str | None = Field(
        None,
        title="Error Trace ID",
        description="Trace ID of the span where error occurred.",
        examples=["dd647833-339c-4080-b7a1-bebfbd2365d0", "a4f5fab3-abc0-48de-a6ff-c142fb27643b"],
        json_schema_extra={"format": "uuid"},
    )
    extra: str | Mapping[str, Any] | list[Any] | None = Field(
        None,
        title="Dev Error Details",
        description="Details that can be useful for developers.",
        examples=[
            {"exception": "ZeroDivisionError"},
            {
                "validationDetails": [
                    {
                        "type": "datetime_from_date_parsing",
                        "loc": ["body", "expires_at"],
                        "msg": (
                            "Input should be a valid datetime or date,"
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
        ],
    )

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
