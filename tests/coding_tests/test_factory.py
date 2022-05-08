from coding.factory import CoderFactory
from coding.abstract import Coder

import pytest


@pytest.fixture
def factory():
    return CoderFactory()


@pytest.mark.parametrize("coder_name", ["rot13", "rot47"])
def test_get_coder_should_return_constructor_of_coder(factory, coder_name):
    coder = factory.get_coder(coder_name)
    
    assert issubclass(coder, Coder)


def test_get_coder_should_raise_key_error_when_no_coder(factory):
    coder_name = "nonexisted_coder"
    
    with pytest.raises(KeyError):
        factory.get_coder(coder_name)
