import smtplib
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)


class GMailConnection(MailerConnectionAbstract):
    def __init__(
        self, gmail_user: str, gmail_password: str, server_url: str, server_port: int
    ) -> None:
        self.__gmail_user = gmail_user
        self.__gmail_password = gmail_password
        self.__gmail_server_url = server_url
        self.__gmail_server_port = server_port
        self.__create_server()

    def __create_server(self) -> None:
        self.__server = smtplib.SMTP_SSL(
            host=self.__gmail_server_url, port=self.__gmail_server_port
        )
        self.__server.ehlo()
        self.__server.login(user=self.__gmail_user, password=self.__gmail_password)

    def __build_email(
        self, sent_from: str, send_to: str, subject: str, body: str
    ) -> str:
        return f'From: {sent_from}\nTo: {send_to}\nSubject: {subject}\n\n{body}'

    def send_email(self, to: str, subject: str, body: str) -> None:
        email = self.__build_email(
            sent_from=self.__gmail_user, send_to=to, subject=subject, body=body
        )
        self.__server.sendmail(from_addr=self.__gmail_user, to_addrs=to, msg=email)
