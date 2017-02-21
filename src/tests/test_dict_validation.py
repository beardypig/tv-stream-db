#!/usr/bin/env python
import pytest
import sys
import os.path

# fudge validate.py on to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from validation import Text, Schema, Dict, ValidationError


@pytest.mark.parametrize("schema, value, expected", [
    ({"test": Text()},
     {"test": "hello"},
     {"test": "hello"}),
    ({"test": Text(default="default")},
     {},
     {"test": "default"}),
    ({"test": Dict({"test": Text()})},
     {"test": {"test": "hello"}},
     {"test": {"test": "hello"}}),
    ({"test": Dict({"test": Text(default="hello")}, default={})},
     {"test": {"test": "hello"}},
     {"test": {"test": "hello"}})
])
def test_schema(schema, value, expected):
    s = Dict(schema)
    assert expected == s.validate(value)

