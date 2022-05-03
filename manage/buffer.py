from .abstract import Buffer


class DictBuffer(Buffer):
    @property
    def data(self) -> dict:
        return self.__dict__
