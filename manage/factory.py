from coding.factory import FactoryMixin
from .buffer import *
from .file import *


class FileManagerFactory(FactoryMixin):
    def __init__(self):
        self.file_managers = {
            "json": JSONManager,
        }
        self.error_message = "There is no file manager like {}."

    def get_file_manager(self, file_manager_name: str) -> type[FileManager]:
        return super().constructor_factory(self.file_managers, file_manager_name)


class BufferFactory(FactoryMixin):
    def __init__(self):
        self.buffers = {
            "dict": DictBuffer,
        }
        self.error_message = "There is no buffer like {}."

    def get_buffer(self, buffer_name: str) -> type[Buffer]:
        return super().constructor_factory(self.buffers, buffer_name)
