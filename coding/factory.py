from .coders import *


class FactoryMixin:
    error_message = "There is no constructor like {}."
    
    def object_factory(self, constructors: dict, constructor_name: str) -> object:
        constructor = constructors.get(constructor_name)
        if constructor:
            return constructor()
        raise KeyError(self.error_message.format(constructor_name))


class CoderFactory(FactoryMixin):
    coders = {
        "rot13": ROT13,
        "rot47": ROT47,
    }
    error_message = "There is no coder like {}."

    def get_coder(self, coder_name: str) -> Coder:
        return super().object_factory(self.coders, coder_name)
