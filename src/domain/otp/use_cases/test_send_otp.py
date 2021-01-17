from unittest import TestCase, mock
from domain.otp.entities.email.mailer_abstract import MailerAbstract
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.entities.otp.otp import OTP
from domain.otp.entities.otp.otp_repository_abstract import OTPRepositoryAbstract
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.use_cases.send_otp import SendOTP
from domain.otp.exceptions.otp_generation_failed_exception import (
    OTPGenerationFailedException,
)


class TestSendOTP(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.to = 'user@domain.com'
        cls.ttl = 60
        cls.otp_code = '123456'

    def setUp(self) -> None:
        self.repository_mock = mock.Mock(spec=OTPRepositoryAbstract)
        self.hash_mock = mock.Mock(spec=HashAbstract)
        self.mailer_mock = mock.Mock(spec=MailerAbstract)
        self.otp = OTP(
            method=OTPMethodEnum.EMAIL.value,
            to=self.to,
            encoder=self.hash_mock,
            status=OTPStatusEnum.PENDING.value,
        )

    def test_send_otp_WHEN_created_THEN_sets_use_case_attributes(self):
        expected_use_case_attributes = {
            'repository': self.repository_mock,
            'mailer': self.mailer_mock,
            'otp': self.otp,
        }

        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )

        actual_use_case_attributes = use_case.__dict__

        self.assertDictEqual(expected_use_case_attributes, actual_use_case_attributes)

    def test_execute_WHEN_called_AND_otp_generate_otp_raises_exception_THEN_returns_dict(
        self,
    ):
        self.hash_mock.to_hash = mock.Mock(
            side_effect=OTPGenerationFailedException('Error')
        )

        expected_result = {'status': 'failed: Error'}

        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )
        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)

    def test_execute_WHEN_called_AND_email_instance_raises_exception_THEN_returns_dict(
        self,
    ):
        self.mailer_mock.get_instance = mock.Mock(side_effect=Exception('Error'))

        expected_result = {'status': 'failed: Error'}

        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )
        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)

    def test_execute_WHEN_called_AND_email_send_raises_exception_THEN_returns_dict(
        self,
    ):
        mailer_connection_mock = mock.Mock()
        mailer_connection_mock.send_email = mock.Mock(side_effect=Exception('Error'))
        self.mailer_mock.get_instance = mock.Mock(return_value=mailer_connection_mock)

        expected_result = {'status': 'failed: Error'}

        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )
        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)

    def test_execute_WHEN_called_THEN_calls_repository_save(self):
        hashed_otp = str.encode(self.otp_code)
        self.hash_mock.to_hash = mock.Mock(return_value=hashed_otp)
        self.repository_mock.save = mock.Mock()
        self.otp.hashed_otp = hashed_otp

        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )
        use_case.execute()

        self.repository_mock.save.assert_called_once_with(otp=self.otp)

    def test_execute_WHEN_called_THEN_returns_dict(self):
        expected_return = {
            'status': OTPStatusEnum.PENDING.value,
            'ttl_seconds': self.ttl,
        }
        use_case = SendOTP(
            repository=self.repository_mock,
            encoder=self.hash_mock,
            mailer=self.mailer_mock,
            to=self.to,
        )
        actual_return = use_case.execute()

        self.assertDictEqual(expected_return, actual_return)
