from abc import ABC


class HashAbstract(ABC):
    @staticmethod
    def to_hash(password: str) -> bytes:
        pass

    @staticmethod
    def compare(string: str, hash: bytes) -> bool:
        pass
