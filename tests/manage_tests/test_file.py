from unittest.mock import mock_open
from manage.file import JSONManager
import pytest


class TestJSONManager:
    @pytest.fixture
    def manager(self):
        return JSONManager()

    @pytest.fixture
    def content(self):
        return {"test": "content"}

    @pytest.fixture
    def file_mock(self, mocker):
        m = mock_open(read_data='{"test": "content"}')
        open_mock = mocker.patch("manage.abstract.open", m)
        return open_mock()

    @pytest.fixture
    def mkdir_mock(self, mocker):
        return mocker.patch("manage.abstract.Path.mkdir")

    @pytest.fixture
    def super_save_mock(self, mocker):
        return mocker.patch("manage.file.FileManager.save")

    def test_save_should_invoke_mkdir(self, file_mock, mkdir_mock, manager, content):
        manager.save("file_name", content)
        
        assert mkdir_mock.called

    def test_save_should_invoke_write_of_file(self, file_mock, mkdir_mock, manager, content):
        manager.save("file_name", content)
        
        assert file_mock.write.called

    def test_save_should_invoke_super_save_with_added_to_file_name_correct_extension_json(self, super_save_mock, manager, content):
        manager.save("file_name", content)
        file_name = super_save_mock.call_args.args[0]

        assert file_name.endswith(".json")

    def test_save_should_invoke_super_save_with_correct_content_type_str(self, super_save_mock, manager, content):
        manager.save("file_name", content)

        saved_content = super_save_mock.call_args.args[1]

        assert isinstance(saved_content, str)

    def test_read_should_invoke_read_of_file(self, file_mock, manager):
        manager.read("file_name.json")
        
        assert file_mock.read.called

    def test_read_should_return_dict(self, file_mock, manager):
        result = manager.read("file_name.json")
        
        assert isinstance(result, dict)
