from dataclasses import dataclass, field
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
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
        self.connection = mailer.get_instance()
        self.to = to
        self.subject = subject
        self.body = body

    def send(self) -> None:
        self.connection.send_email(to=self.to, subject=self.subject, body=self.body)
