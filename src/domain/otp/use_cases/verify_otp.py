from typing import Dict
from domain.otp.entities.otp.otp_repository_abstract import OTPRepositoryAbstract
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.otp_verification_failed_exception import (
    OTPVerificationFailedException,
)
from domain.otp.exceptions.otp_does_not_exist_exception import OTPDoesNotExistException


class VerifyOTP:
    def __init__(
        self, repository: OTPRepositoryAbstract, to: str, otp_code: str
    ) -> None:
        self.repository = repository
        self.to = to
        self.otp_code = otp_code

    def execute(self) -> Dict:
        try:
            otp = self.repository.get(to=self.to)
            otp.verify(otp_code=self.otp_code)
            if otp.status == OTPStatusEnum.VALIDATED.value:
                self.repository.delete(to=otp.to)
            return {'status': otp.status}
        except (OTPDoesNotExistException, OTPVerificationFailedException) as e:
            return {'status': f'Failed to verify OTP: {e}'}
