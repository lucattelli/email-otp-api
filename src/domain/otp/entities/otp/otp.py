from dataclasses import dataclass
from random import randint
from typing import Optional
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.otp_generation_failed_exception import (
    OTPGenerationFailedException,
)
from domain.otp.exceptions.otp_verification_failed_exception import (
    OTPVerificationFailedException,
)


@dataclass
class OTP:
    method: OTPMethodEnum
    to: str
    encoder: HashAbstract
    status: OTPStatusEnum
    hashed_otp: Optional[bytes] = None

    def verify(self, otp_code: str) -> None:
        if self.__invalid_status_for_verification() or self.__incorrect_otp(
            otp_code=otp_code
        ):
            raise OTPVerificationFailedException
        self.status = OTPStatusEnum.VALIDATED.value

        self.status = OTPStatusEnum.VALIDATED.value

    def generate_otp(self) -> str:
        if self.hashed_otp is not None:
            raise OTPGenerationFailedException
        otp_code = self.__generate_otp_code()
        self.hashed_otp = self.encoder.to_hash(password=otp_code)
        return otp_code

    def __invalid_status_for_verification(self) -> bool:
        return self.status != OTPStatusEnum.PENDING.value

    def __incorrect_otp(self, otp_code: str) -> bool:
        match = self.encoder.compare(string=otp_code, hashed=self.hashed_otp)
        return not match

    def __generate_otp_code(self) -> str:
        return str(randint(0, 999999)).zfill(6)
