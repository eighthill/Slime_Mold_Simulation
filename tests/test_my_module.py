"""Tests for the slime_mold_simulation.my_module module."""

# import numpy as np
import pytest

from slime_mold_simulation.my_module import hello

# from slime_mold_simulation.simulation import get_sensors


def test_hello():
    assert hello("Alice") == "Hello Alice!"


def test_hello_with_error():
    with pytest.raises(ValueError) as excinfo:
        hello("nobody")
    assert "Can not say hello to nobody" in str(excinfo.value)


@pytest.fixture
def some_name():
    return "Jane Smith"


def test_hello_with_fixture(some_name):
    assert hello(some_name) == "Hello Jane Smith!"
