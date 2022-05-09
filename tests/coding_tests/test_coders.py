from coding.coders import ROT13, ROT47
import pytest


class TestROT13:
    @pytest.fixture
    def coder(self):
        return ROT13()

    def test_encode_should_return_expected_string(self, coder):
        to_encode = "Test of Ciphering with ROT13."
        expected = "Grfg bs Pvcurevat jvgu EBG13."

        assert coder.encode(to_encode) == expected

    def test_decode_should_return_expected_string(self, coder):
        to_decode = "Grfg bs Pvcurevat jvgu EBG13."
        expected = "Test of Ciphering with ROT13."

        assert coder.decode(to_decode) == expected


class TestROT47:
    @pytest.fixture
    def coder(self):
        return ROT47()

    def test_encode_should_return_expected_string(self, coder):
        to_encode = "Test of Ciphering with ROT47."
        expected = "%6DE @7 r:A96C:?8 H:E9 #~%cf]"

        assert coder.encode(to_encode) == expected

    def test_decode_should_return_expected_string(self, coder):
        to_decode = "%6DE @7 r:A96C:?8 H:E9 #~%cf]"
        expected = "Test of Ciphering with ROT47."

        assert coder.decode(to_decode) == expected
