from unittest import TestCase, mock
from domain.otp.entities.otp.otp import OTP
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.use_cases.verify_otp import VerifyOTP
from domain.otp.exceptions.otp_does_not_exist_exception import OTPDoesNotExistException
from domain.otp.exceptions.otp_verification_failed_exception import (
    OTPVerificationFailedException,
)


class TestVerifyOTP(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hash_mock = mock.Mock()
        cls.repository_mock = mock.Mock()
        cls.to = 'user@domain.com'
        cls.otp_code = '123456'
        cls.hashed_otp = str.encode(cls.otp_code)
        cls.otp = OTP(
            method=OTPMethodEnum.EMAIL.value,
            to=cls.to,
            encoder=cls.hash_mock,
            status=OTPStatusEnum.PENDING.value,
            hashed_otp=cls.hashed_otp,
        )

    def test_verify_otp_WHEN_created_THEN_sets_use_case_atributes(self):
        expected_use_case_attributes = {
            'repository': self.repository_mock,
            'to': self.to,
            'otp_code': self.otp_code,
        }
        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        actual_use_case_attributes = use_case.__dict__

        self.assertDictEqual(expected_use_case_attributes, actual_use_case_attributes)

    def test_execute_WHEN_called_THEN_calls_repository_get(self):
        self.repository_mock.get = mock.Mock()
        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )
        use_case.execute()

        self.repository_mock.get.assert_called_once_with(to=self.to)

    def test_execute_WHEN_called_AND_repository_get_raises_exception_THEN_returns_dict_with_exception(
        self,
    ):
        self.repository_mock.get = mock.Mock(
            side_effect=OTPDoesNotExistException('Error')
        )

        expected_result = {'status': 'Failed to verify OTP: Error'}

        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)

    def test_execute_WHEN_called_AND_repository_get_returns_otp_THEN_calls_otp_verify(
        self,
    ):
        self.otp.verify = mock.Mock()
        self.repository_mock.get = mock.Mock(return_value=self.otp)

        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        use_case.execute()

        self.otp.verify.assert_called_once_with(otp_code=self.otp_code)

    def test_execute_WHEN_called_AND_verify_raises_exception_THEN_returns_dict_with_exception(
        self,
    ):
        self.otp.verify = mock.Mock(side_effect=OTPVerificationFailedException('Error'))
        self.repository_mock.get = mock.Mock(return_value=self.otp)

        expected_result = {'status': 'Failed to verify OTP: Error'}

        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)

    def test_execute_WHEN_called_AND_verify_passes_AND_status_is_validated_THEN_calls_repository_delete(
        self,
    ):
        self.repository_mock.delete = mock.Mock()
        self.otp.verify = mock.Mock()
        self.otp.status = OTPStatusEnum.VALIDATED.value
        self.repository_mock.get = mock.Mock(return_value=self.otp)

        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        use_case.execute()

        self.repository_mock.delete.assert_called_once_with(to=self.to)

    def test_execute_WHEN_called_AND_verify_passes_AND_status_is_validated_THEN_return_dict(
        self,
    ):
        self.repository_mock.delete = mock.Mock()
        self.otp.verify = mock.Mock()
        self.otp.status = OTPStatusEnum.VALIDATED.value
        self.repository_mock.get = mock.Mock(return_value=self.otp)

        expected_result = {'status': OTPStatusEnum.VALIDATED.value}

        use_case = VerifyOTP(
            repository=self.repository_mock, to=self.to, otp_code=self.otp_code
        )

        actual_result = use_case.execute()

        self.assertDictEqual(expected_result, actual_result)
