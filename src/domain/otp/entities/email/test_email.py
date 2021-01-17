from unittest import TestCase, mock
from domain.otp.entities.email.email import Email
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)
from domain.otp.exceptions.email_server_connection_failed_exception import (
    EmailServerConnectionFailedException,
)
from domain.otp.exceptions.email_send_failed_exception import EmailSendFailedException


class TestEmail(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.to = 'user@domain.com'
        cls.subject = 'subject'
        cls.body = 'body'
        return super().setUpClass()

    def setUp(self) -> None:
        self.mailer_connection_stub = mock.Mock(spec=MailerConnectionAbstract)
        self.mailer_stub = mock.Mock(spec=MailerAbstract)
        self.mailer_stub.get_instance.return_value = self.mailer_connection_stub

    def test_email_WHEN_created_THEN_set_correct_attributes(self):
        expected_email_dict = {
            'body': 'body',
            'connection': self.mailer_connection_stub,
            'subject': 'subject',
            'to': 'user@domain.com',
        }

        email = Email(
            mailer=self.mailer_stub, to=self.to, subject=self.subject, body=self.body
        )
        actual_email_dict = email.__dict__

        self.assertDictEqual(expected_email_dict, actual_email_dict)

    def test_email_WHEN_created_THEN_calls_mailer_get_instance(self):
        Email(mailer=self.mailer_stub, to=self.to, subject=self.subject, body=self.body)

        self.mailer_stub.get_instance.assert_called_once()

    def test_email_WHEN_created_AND_mailer_get_instance_raises_exception_THEN_raise_exception(
        self,
    ):
        mailer_stub = mock.Mock(spec=MailerAbstract)
        mailer_stub.get_instance = mock.Mock(side_effect=Exception('Error'))

        with self.assertRaises(EmailServerConnectionFailedException):
            Email(
                mailer=mailer_stub,
                to=self.to,
                subject=self.subject,
                body=self.body,
            )

    def test_send_WHEN_called_THEN_calls_mailer_connection_send_email(self):
        email = Email(
            mailer=self.mailer_stub, to=self.to, subject=self.subject, body=self.body
        )
        email.send()

        self.mailer_connection_stub.send_email.assert_called_once_with(
            to=self.to, subject=self.subject, body=self.body
        )

    def test_send_WHEN_called_AND_send_mail_raises_exception_THEN_raise_exception(self):
        self.mailer_connection_stub.send_email = mock.Mock(
            side_effect=Exception('Error')
        )

        email = Email(
            mailer=self.mailer_stub, to=self.to, subject=self.subject, body=self.body
        )

        with self.assertRaises(EmailSendFailedException):
            email.send()
