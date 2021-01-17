import os
from unittest import TestCase, mock
import settings


class TestSettings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @mock.patch('dotenv.load_dotenv')
    @mock.patch('os.getenv')
    def test_load_settings_WHEN_called_THEN_calls_load_dotenv(
        self, getenv_mock, load_dotenv_mock
    ):
        settings.load_settings()
        self.assertTrue(load_dotenv_mock.called)

    @mock.patch('dotenv.load_dotenv')
    @mock.patch('os.getenv')
    def test_load_settings_WHEN_called_THEN_calls_os_getenv_for_all_settings(
        self, getenv_mock, load_dotenv_mock
    ):
        expected_call_args_list = [
            ('GMAIL_USER', ''),
            ('GMAIL_PASSWORD', ''),
            ('GMAIL_URL', ''),
            ('GMAIL_PORT', ''),
        ]

        settings.load_settings()

        actual_call_args_list = [call[0] for call in getenv_mock.call_args_list]

        self.assertListEqual(expected_call_args_list, actual_call_args_list)

    @mock.patch.dict(
        os.environ,
        {
            'GMAIL_USER': 'user@domain.com',
            'GMAIL_PASSWORD': 'password',
            'GMAIL_URL': 'smtp.domain.com',
            'GMAIL_PORT': '999',
        },
    )
    @mock.patch('dotenv.load_dotenv')
    def test_load_settings_WHEN_called_THEN_set_settings_values(self, load_dotenv_mock):
        expected_settings_dict = {
            'GMAIL_USER': 'user@domain.com',
            'GMAIL_PASSWORD': 'password',
            'GMAIL_URL': 'smtp.domain.com',
            'GMAIL_PORT': '999',
        }

        settings.load_settings()
        actual_settings_dict = settings.settings

        self.assertDictEqual(expected_settings_dict, actual_settings_dict)
