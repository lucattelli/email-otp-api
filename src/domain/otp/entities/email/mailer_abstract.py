from abc import ABC
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)


class MailerAbstract(ABC):
    @classmethod
    def get_instance(cls) -> MailerConnectionAbstract:
        pass
