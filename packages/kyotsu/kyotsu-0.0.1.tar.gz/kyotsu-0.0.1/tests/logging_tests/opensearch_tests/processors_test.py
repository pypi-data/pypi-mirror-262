"""
This module contains the unit tests for classes and functions within
the `kyotsu.logging.opensearch.processors` module.
"""

import json

import pytest

from kyotsu.logging.opensearch.processors import SafeJSONSerializer


class NonSerializableObject:
    """
    A simple mockup class that represents an object that cannot be serialized with the standard JSON serializer.
    """

    def __repr__(self) -> str:
        return "NonSerializableObject()"


# Instance of SafeJSONSerializer
serializer = SafeJSONSerializer()

# Test data for parameterization
test_data = [
    pytest.param({"key": NonSerializableObject(), "other_key": 123}, ["key"], id="object_at_root"),
    pytest.param(
        {"key": {"nested_key": NonSerializableObject(), "nested_key2": 456}},
        ["key", "nested_key"],
        id="object_in_nested_dict",
    ),
    pytest.param({"key": [1, "string", NonSerializableObject(), 4.5]}, ["key", 2], id="object_in_list"),
]


@pytest.mark.parametrize(("data", "path"), test_data)
def test_safe_json_serializer(data, path):
    """
    Test that the SafeJSONSerializer correctly replaces non-serializable objects with a string representation.

    Args:
        data (dict): The data to be serialized. It contains a non-serializable object in a location specified by path.
        path (list): The path to the non-serializable object in the data.

    Raises:
        AssertionError: If the SafeJSONSerializer doesn't replace the non-serializable object correctly.
    """

    serialized = serializer.dumps(data)
    loaded = json.loads(serialized)

    # Extract element at `path`.
    element = loaded
    for p in path:
        element = element[p]

    assert element == f"<<nonserializable: {NonSerializableObject()!r}>>"
