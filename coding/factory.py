from .coders import *


class FactoryMixin:
    def __init__(self):
        self.error_message = "There is no constructor like {}."
    
    def constructor_factory(self, constructors: dict, constructor_name: str) -> type:
        constructor = constructors.get(constructor_name)
        if constructor:
            return constructor
        raise KeyError(self.error_message.format(constructor_name))


class CoderFactory(FactoryMixin):
    def __init__(self):
        self.coders = {
            "rot13": ROT13,
            "rot47": ROT47,
        }
        self.error_message = "There is no coder like {}."

    def get_coder(self, coder_name: str) -> type[Coder]:
        return super().constructor_factory(self.coders, coder_name)
