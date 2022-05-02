from abc import ABC, abstractmethod


class Coder(ABC):
    @abstractmethod
    def encode(self, txt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, txt: str) -> str:
        raise NotImplementedError
