from abc import ABC, abstractmethod


class MailerConnectionAbstract(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        pass
