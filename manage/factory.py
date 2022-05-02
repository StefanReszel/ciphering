from .buffer import *
from .file import *


class FileManagerFactory:
    file_managers = {
        "json": JSONManager,
    }


class BufferFactory:
    buffer_managers = {
        "dict": DictBuffer,
    }
