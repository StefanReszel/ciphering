from coding.abstract import Coder
from coding.factory import CoderFactory

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class CoderFactoryMixin:
    coder_factory = CoderFactory()


class Buffer(CoderFactoryMixin, ABC):
    def __init__(self, coder_name: str, txt: str):
        self.coder = coder_name
        self.encoded_txt = txt

    @property
    @abstractmethod
    def data(self) -> Any:
        raise NotImplementedError

    @property
    def encoded_txt(self) -> str:
        return self.text

    @encoded_txt.setter
    def encoded_txt(self, txt: str):
        encoder = self.coder_factory.get_coder(self.coder)
        self.text = encoder.encode(txt)


class FileManager(CoderFactoryMixin, ABC):
    dir_with_saved_files = Path("ciphered-files/")

    @abstractmethod
    def get_coder_name_and_text_from_file(self, file_content: str) -> tuple[str, str]:
        """Should return two element tuple or list with coder name and encoded text in this order."""
        raise NotImplementedError

    def read(self, file_name: str) -> str:
        file_content = self.get_file_content(file_name)
        coder_name, text = self.get_coder_name_and_text_from_file(file_content)
        decoder = self.get_decoder(coder_name)
        decoded_text = decoder.decode(text)
        return decoded_text

    def save(self, file_name: str, content: str):
        self.dir_with_saved_files.mkdir(exist_ok=True)
        path_to_file = self.dir_with_saved_files / file_name

        with open(path_to_file, "w") as file:
            file.write(content)

    def get_file_content(self, file_name: str) -> str:
        path_to_file = self.dir_with_saved_files / file_name

        with open(path_to_file, "r") as file:
            content = file.read()
        return content

    def get_decoder(self, coder_name: str) -> Coder:
        return self.coder_factory.get_coder(coder_name)
