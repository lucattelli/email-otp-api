from abc import ABC


class MailerConnectionAbstract(ABC):
    def send_email(self, to: str, subject: str, body: str) -> None:
        pass
