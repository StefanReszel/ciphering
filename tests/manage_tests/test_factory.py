from manage.factory import FileManagerFactory, BufferFactory
from manage.abstract import FileManager, Buffer

import pytest


class TestFileManagerFactory:
    @pytest.fixture
    def factory(self):
        return FileManagerFactory()

    @pytest.mark.parametrize("file_manager_name", ["json"])
    def test_get_file_manager_should_return_constructor_of_file_manager(self, factory, file_manager_name):
        file_manager = factory.get_file_manager(file_manager_name)
        
        assert issubclass(file_manager, FileManager)

    def test_get_file_manager_should_raise_key_error_when_no_file_manager(self, factory):
        file_manager_name = "nonexisted_file_manager"
        
        with pytest.raises(KeyError):
            factory.get_file_manager(file_manager_name)


class TestBufferFactory:
    @pytest.fixture
    def factory(self):
        return BufferFactory()

    @pytest.mark.parametrize("buffer_name", ["dict"])
    def test_get_buffer_should_return_constructor_of_buffer(self, factory, buffer_name):
        buffer = factory.get_buffer(buffer_name)
        
        assert issubclass(buffer, Buffer)

    def test_get_buffer_should_raise_key_error_when_no_buffer(self, factory):
        buffer_name = "nonexisted_buffer"
        
        with pytest.raises(KeyError):
            factory.get_buffer(buffer_name)
