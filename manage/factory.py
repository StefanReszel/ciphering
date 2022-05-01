from coding.factory import FactoryMixin
from .buffer import *
from .file import *


class FileManagerFactory(FactoryMixin):
    file_managers = {
        "json": JSONManager,
    }
    error_message = "There is no file manager like {}."

    def get_file_manager(self, file_manager_name: str) -> type[FileManager]:
        return super().constructor_factory(self.file_managers, file_manager_name)


class BufferFactory(FactoryMixin):
    buffers = {
        "dict": DictBuffer,
    }
    error_message = "There is no buffer like {}."

    def get_buffer(self, buffer_name: str) -> type[Buffer]:
        return super().constructor_factory(self.buffers, buffer_name)
