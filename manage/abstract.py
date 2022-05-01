from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Buffer(ABC):
    def __init__(self, coder_name: str, text: str):
        self.coder = coder_name
        self.text = text

    @property
    @abstractmethod
    def data(self) -> Any:
        raise NotImplementedError


class FileManager(ABC):
    dir_with_saved_files = Path("ciphered-files/")

    def save(self, file_name: str, content: str):
        self.dir_with_saved_files.mkdir(exist_ok=True)
        path_to_file = self.dir_with_saved_files / file_name

        with open(path_to_file, "w") as file:
            file.write(content)

    def read(self, file_name: str) -> str:
        path_to_file = self.dir_with_saved_files / file_name

        with open(path_to_file, "r") as file:
            content = file.read()
        return content
