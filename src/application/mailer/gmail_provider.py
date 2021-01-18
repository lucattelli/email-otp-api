import settings
from application.mailer import gmail_connection

from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)


class GMailProvider(MailerAbstract):
    __connection = None

    @classmethod
    def get_instance(cls) -> MailerConnectionAbstract:
        if cls.__connection is None:
            cls.__connection = gmail_connection.GMailConnection(
                gmail_user=settings.settings.get('GMAIL_USER'),
                gmail_password=settings.settings.get('GMAIL_PASSWORD'),
                server_url=settings.settings.get('GMAIL_URL'),
                server_port=settings.settings.get('GMAIL_PORT'),
            )
        return cls.__connection
