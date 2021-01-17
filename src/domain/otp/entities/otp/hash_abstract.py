from abc import ABC, abstractstaticmethod


class HashAbstract(ABC):
    @abstractstaticmethod
    def to_hash(password: str) -> bytes:
        pass

    @abstractstaticmethod
    def compare(string: str, hashed: bytes) -> bool:
        pass
