from .abstract import Buffer


class DictBuffer(Buffer):
    @property
    def data(self):
        return self.__dict__
