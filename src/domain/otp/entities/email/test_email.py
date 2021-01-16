from unittest import TestCase, mock
from domain.otp.entities.email.email import Email
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.email.mailer_connection_abstract import (
    MailerConnectionAbstract,
)


class TestEmail(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mailer_connection_stub = mock.Mock(spec=MailerConnectionAbstract)
        cls.mailer_stub = mock.Mock(spec=MailerAbstract)
        cls.mailer_stub.get_instance.return_value = cls.mailer_connection_stub
        cls.to = 'user@domain.com'
        cls.subject = 'subject'
        cls.body = 'body'
        return super().setUpClass()

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

    def test_send_WHEN_called_THEN_calls_mailer_connection_send_email(self):
        email = Email(
            mailer=self.mailer_stub, to=self.to, subject=self.subject, body=self.body
        )
        email.send()

        self.mailer_connection_stub.send_email.assert_called_once_with(
            to=self.to, subject=self.subject, body=self.body
        )
