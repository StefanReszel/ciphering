from abc import ABC, abstractmethod


class AbstractBuffer(ABC):
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def set(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass


class AbstractFileManager(ABC):
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def save(self):
        pass
    