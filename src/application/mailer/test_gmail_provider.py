from unittest import TestCase, mock
from application.mailer.gmail_provider import GMailProvider


class TestGMailProvider(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    @mock.patch('application.mailer.gmail_connection.GMailConnection')
    @mock.patch('settings.settings')
    def test_get_instance_WHEN_called_THEN_sets_connection(self, settings_mock, _):
        settings_mock.get.return_value = 'dummy-value'
        GMailProvider.get_instance()
        actual_connection = GMailProvider.__dict__.get(
            '_GMailProvider__connection', None
        )
        self.assertIsNotNone(actual_connection)

    @mock.patch('application.mailer.gmail_connection.GMailConnection')
    @mock.patch('settings.settings')
    def test_get_instance_WHEN_called_THEN_returns_connection(
        self, settings_mock, gmail_connection_mock
    ):
        settings_mock.get.return_value = 'dummy-value'

        expected_instance = gmail_connection_mock()
        actual_instance = GMailProvider.get_instance()

        self.assertEqual(expected_instance, actual_instance)
