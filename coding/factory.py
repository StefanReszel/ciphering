from coders import *


class CoderFactory:
    coders = {
        "rot13": ROT13,
        "rot47": ROT47,
    }
    error_message = "There is no coder like {}."

    def make_coder(self, coder_name: str) -> Coder:
        coder = self.coders.get(coder_name)
        if coder:
            return coder()
        raise KeyError(self.error_message.format(coder_name))
