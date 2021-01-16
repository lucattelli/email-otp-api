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
    hashed_otp: str
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
        return self.hashed_otp != self.__to_hash(otp_code=otp_code)

    def __to_hash(self, otp_code: str) -> str:
        return self.encoder.to_hash(string=otp_code)
