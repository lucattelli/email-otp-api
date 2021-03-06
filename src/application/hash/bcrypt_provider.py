import bcrypt
from domain.otp.entities.otp.hash_abstract import HashAbstract


class BCryptProvider(HashAbstract):
    @staticmethod
    def to_hash(password: str) -> bytes:
        return bcrypt.hashpw(password=str.encode(password), salt=bcrypt.gensalt())

    @staticmethod
    def compare(string: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password=str.encode(string), hashed_password=hashed)
