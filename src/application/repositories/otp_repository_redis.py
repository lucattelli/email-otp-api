import pickle
from typing import Optional
from redis import Redis
from domain.otp.entities.otp.otp import OTP
from domain.otp.entities.otp.otp_repository_abstract import OTPRepositoryAbstract
from domain.otp.exceptions.otp_does_not_exist_exception import OTPDoesNotExistException


class OTPRepositoryRedis(OTPRepositoryAbstract):
    def __init__(self, database_session: Redis):
        self.database_session = database_session

    def save(self, otp: OTP) -> None:
        serialized_otp = pickle.dumps(obj=otp)
        self.database_session.set(name=otp.to, value=serialized_otp)
        self.database_session.expire(name=otp.to, time=otp.ttl)

    def get(self, to: str) -> Optional[OTP]:
        binary_otp = self.database_session.get(name=to)
        if binary_otp is None:
            raise OTPDoesNotExistException
        otp: OTP = pickle.loads(__data=binary_otp)
        otp.ttl = self.database_session.ttl(name=otp.to)
        return otp

    def delete(self, to: str) -> None:
        self.database_session.delete(names=to)
