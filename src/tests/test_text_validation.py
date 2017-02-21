#!/usr/bin/env python
import pytest
import sys
import os.path

# fudge validate.py on to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from validation import Text, ValidationError


@pytest.mark.parametrize("value", [
    "Test Text",
    "Test Text 2"
])
def test_valid(value):
    assert value == Text().validate(value)


@pytest.mark.parametrize("value", [
    1, False, None, 0.1, object()
])
def test_invalid(value):
    with pytest.raises(ValidationError):
        assert value == Text().validate(value)


@pytest.mark.parametrize("value", [
    "Default Text",
    "Default Text 2"
])
def test_default_value(value):
    assert value == Text(default=value).default()


def test_no_default():
    with pytest.raises(ValidationError):
        Text().default()
