from manage.buffer import DictBuffer

import pytest


class TestDictBuffer:
    @pytest.fixture
    def buffer(self):
        return DictBuffer("coder", "text")

    def test_data_property_should_return_dict_type(self, buffer):
        data = buffer.data

        assert isinstance(data, dict)
