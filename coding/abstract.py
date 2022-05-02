from abc import ABC, abstractmethod


class Coder(ABC):
    @abstractmethod
    def encode(self):
        raise NotImplemented

    @abstractmethod
    def decode(self):
        raise NotImplemented
