from dataclasses import dataclass, field
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)
from domain.otp.exceptions.email_send_failed_exception import EmailSendFailedException
from domain.otp.exceptions.email_server_connection_failed_exception import (
    EmailServerConnectionFailedException,
)


@dataclass
class Email:
    connection: MailerConnectionAbstract = field(init=False)
    to: str
    subject: str
    body: str

    def __init__(
        self, mailer: MailerAbstract, to: str, subject: str, body: str
    ) -> None:
        try:
            self.connection = mailer.get_instance()
        except Exception as e:
            raise EmailServerConnectionFailedException(e) from e
        self.to = to
        self.subject = subject
        self.body = body

    def send(self) -> None:
        try:
            self.connection.send_email(to=self.to, subject=self.subject, body=self.body)
        except Exception as e:
            raise EmailSendFailedException(e) from e
