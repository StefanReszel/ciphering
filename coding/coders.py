from .abstract import Coder
import codecs


class ROT13(Coder):
    def encode(self, txt: str) -> str:
        return self._rot13(txt)

    def decode(self, txt: str) -> str:
        return self._rot13(txt)

    def _rot13(self, txt: str) -> str:
        return codecs.encode(txt, 'rot_13')


class ROT47(Coder):
    def encode(self, txt: str) -> str:
        return self._rot47(txt)

    def decode(self, txt: str) -> str:
        return self._rot47(txt)

    def _rot47(self, txt: str) -> str:
        encoded_leters = []
        for letter in txt:
            unicode_number = ord(letter)
            if unicode_number >= 33 and unicode_number <= 126:
                encoded_leters.append(chr(33 + ((unicode_number + 14) % 94)))
            else:
                encoded_leters.append(letter)
        encoded_txt = ''.join(encoded_leters)
        return encoded_txt
