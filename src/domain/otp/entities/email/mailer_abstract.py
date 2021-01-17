from abc import ABC, abstractclassmethod
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)


class MailerAbstract(ABC):
    @abstractclassmethod
    def get_instance(cls) -> MailerConnectionAbstract:
        pass
