from abc import ABC


class HashAbstract(ABC):
    @staticmethod
    def to_hash(password: str) -> bytes:
        pass
