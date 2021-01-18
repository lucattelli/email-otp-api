from unittest import TestCase, mock

from application.mailer.gmail_connection import GMailConnection


class TestGMailConnection(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gmail_user = 'user@domain.com'
        cls.gmail_password = 'password'
        cls.gmail_server_url = 'smtp.domain.com'
        cls.gmail_server_port = '1234'
        cls.to = 'email@domain.com'
        cls.subject = 'Subject'
        cls.body = 'Email body'
        cls.email = f'From: {cls.gmail_user}\nTo: {cls.to}\nSubject: {cls.subject}\n\n{cls.body}'

    def setUp(self) -> None:
        pass

    @mock.patch('smtplib.SMTP_SSL')
    def test_gmail_connection_WHEN_created_THEN_properly_set_attributes(
        self, smtp_ssl_mock
    ):
        expected_attributes = {
            '_GMailConnection__gmail_user': self.gmail_user,
            '_GMailConnection__gmail_password': self.gmail_password,
            '_GMailConnection__gmail_server_url': self.gmail_server_url,
            '_GMailConnection__gmail_server_port': self.gmail_server_port,
            '_GMailConnection__server': smtp_ssl_mock(
                host=self.gmail_server_url, port=self.gmail_server_port
            ),
        }

        gmail_connection = GMailConnection(
            gmail_user=self.gmail_user,
            gmail_password=self.gmail_password,
            server_url=self.gmail_server_url,
            server_port=self.gmail_server_port,
        )
        actual_attributes = gmail_connection.__dict__
        self.assertDictEqual(expected_attributes, actual_attributes)

    @mock.patch('smtplib.SMTP_SSL')
    def test_gmail_connection_WHEN_created_THEN_calls_smtplib_smtp_ssl(
        self, smtp_ssl_mock
    ):
        GMailConnection(
            gmail_user=self.gmail_user,
            gmail_password=self.gmail_password,
            server_url=self.gmail_server_url,
            server_port=self.gmail_server_port,
        )
        smtp_ssl_mock.assert_called_once_with(
            host=self.gmail_server_url, port=self.gmail_server_port
        )

    @mock.patch('smtplib.SMTP_SSL')
    def test_gmail_connection_WHEN_created_THEN_calls_smtp_server_ehlo(
        self, smtp_ssl_mock
    ):
        server_mock = mock.Mock()
        smtp_ssl_mock.return_value = server_mock
        GMailConnection(
            gmail_user=self.gmail_user,
            gmail_password=self.gmail_password,
            server_url=self.gmail_server_url,
            server_port=self.gmail_server_port,
        )
        server_mock.ehlo.assert_called_once()

    @mock.patch('smtplib.SMTP_SSL')
    def test_gmail_connection_WHEN_created_THEN_calls_smpt_server_login(
        self, smtp_ssl_mock
    ):
        server_mock = mock.Mock()
        smtp_ssl_mock.return_value = server_mock
        GMailConnection(
            gmail_user=self.gmail_user,
            gmail_password=self.gmail_password,
            server_url=self.gmail_server_url,
            server_port=self.gmail_server_port,
        )
        server_mock.login.assert_called_once_with(
            user=self.gmail_user, password=self.gmail_password
        )

    @mock.patch('smtplib.SMTP_SSL')
    def test_send_email_WHEN_called_THEN_calls_smtp_server_sendmail(
        self, smtp_ssl_mock
    ):
        server_mock = mock.Mock()
        smtp_ssl_mock.return_value = server_mock
        connection = GMailConnection(
            gmail_user=self.gmail_user,
            gmail_password=self.gmail_password,
            server_url=self.gmail_server_url,
            server_port=self.gmail_server_port,
        )
        connection.send_email(to=self.to, subject=self.subject, body=self.body)
        server_mock.sendmail.assert_called_once_with(
            from_addr=self.gmail_user, to_addrs=self.to, msg=self.email
        )
