from typing import Dict
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.entities.email.email import Email
from domain.otp.entities.otp.otp import OTP
from domain.otp.entities.otp.otp_repository_abstract import OTPRepositoryAbstract
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.email_server_connection_failed_exception import (
    EmailServerConnectionFailedException,
)
from domain.otp.exceptions.otp_generation_failed_exception import (
    OTPGenerationFailedException,
)
from domain.otp.exceptions.email_send_failed_exception import EmailSendFailedException


class SendOTP:
    def __init__(
        self,
        repository: OTPRepositoryAbstract,
        encoder: HashAbstract,
        mailer: MailerAbstract,
        to: str,
    ) -> None:
        self.repository = repository
        self.mailer = mailer
        self.otp = self.__build_otp(encoder=encoder, to=to)

    def execute(self) -> Dict:
        try:
            otp_code = self.otp.generate_otp()
            email = self.__build_email(otp_code=otp_code)
            email.send()
            self.repository.save(otp=self.otp)
            return {'status': self.otp.status, 'ttl_seconds': self.otp.ttl}
        except (
            OTPGenerationFailedException,
            EmailServerConnectionFailedException,
            EmailSendFailedException,
        ) as e:
            return {'status': f'failed: {e}'}

    def __build_otp(self, encoder: HashAbstract, to: str) -> OTP:
        return OTP(
            method=OTPMethodEnum.EMAIL.value,
            to=to,
            encoder=encoder,
            status=OTPStatusEnum.PENDING.value,
        )

    def __build_email(self, otp_code: str) -> Email:
        subject = 'Your OTP is here!'
        body = f"Here's your OTP code for logging in: {otp_code}"
        return Email(mailer=self.mailer, to=self.otp.to, subject=subject, body=body)
