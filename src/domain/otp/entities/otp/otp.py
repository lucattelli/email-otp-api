from dataclasses import dataclass
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.otp_verification_failed_exception import (
    OTPVerificationFailedException,
)


@dataclass
class OTP:
    method: OTPMethodEnum
    to: str
    hashed_otp: bytes
    encoder: HashAbstract
    status: OTPStatusEnum

    def verify(self, otp_code: str) -> None:
        if self.__invalid_status_for_verification() or self.__incorrect_otp(
            otp_code=otp_code
        ):
            raise OTPVerificationFailedException
        self.status = OTPStatusEnum.VALIDATED.value

        self.status = OTPStatusEnum.VALIDATED.value

    def __invalid_status_for_verification(self) -> bool:
        return self.status != OTPStatusEnum.PENDING.value

    def __incorrect_otp(self, otp_code: str) -> bool:
        match = self.encoder.compare(string=otp_code, hashed=self.hashed_otp)
        return not match

    def __to_hash(self, otp_code: str) -> str:
        return self.encoder.to_hash(password=otp_code)
