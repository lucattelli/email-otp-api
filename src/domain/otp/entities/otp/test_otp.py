from unittest import TestCase, mock
from domain.otp.entities.otp.otp import OTP
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.otp_verification_failed_exception import (
    OTPVerificationFailedException,
)


class TestOTP(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.otp_method = OTPMethodEnum.EMAIL.value
        cls.to = 'user@domain.com'
        cls.otp_code = '123456'
        cls.invalid_otp_code = '999999'
        cls.hashed_otp = str.encode(cls.otp_code)
        cls.invalid_hashed_otp = str.encode('invalid-hashed-string')
        cls.hash_stub = mock.Mock(spec=HashAbstract)
        cls.hash_stub.to_hash = mock.Mock(
            side_effect=lambda password: cls.hashed_otp
            if password == cls.otp_code
            else cls.invalid_hashed_otp
        )
        cls.hash_stub.compare = mock.Mock(
            side_effect=lambda string, hashed: str.encode(string) == hashed
        )
        return super().setUpClass()

    def test_otp_WHEN_created_THEN_set_correct_attributes(self):
        expected_otp_dict = {
            'method': self.otp_method,
            'to': self.to,
            'hashed_otp': self.hashed_otp,
            'encoder': self.hash_stub,
            'status': OTPStatusEnum.PENDING.value,
            'ttl': 60,
        }

        otp = OTP(
            method=self.otp_method,
            to=self.to,
            hashed_otp=self.hashed_otp,
            encoder=self.hash_stub,
            status=OTPStatusEnum.PENDING.value,
        )
        actual_otp_dict = otp.__dict__

        self.assertDictEqual(expected_otp_dict, actual_otp_dict)

    def test_verify_WHEN_called_AND_status_is_pending_THEN_calls_encoder_compare(
        self,
    ):
        otp = OTP(
            method=self.otp_method,
            to=self.to,
            hashed_otp=self.hashed_otp,
            encoder=self.hash_stub,
            status=OTPStatusEnum.PENDING.value,
        )
        otp.verify(self.otp_code)
        self.hash_stub.compare.assert_called_once_with(
            string=self.otp_code, hashed=self.hashed_otp
        )

    def test_verify_WHEN_called_with_correct_otp_AND_status_is_pending_THEN_set_status_to_validated(
        self,
    ):
        expected_status = OTPStatusEnum.VALIDATED.value

        otp = OTP(
            method=self.otp_method,
            to=self.to,
            hashed_otp=self.hashed_otp,
            encoder=self.hash_stub,
            status=OTPStatusEnum.PENDING.value,
        )
        otp.verify(self.otp_code)
        actual_status = otp.status

        self.assertEqual(expected_status, actual_status)

    def test_verify_WHEN_called_with_incorrect_otp_AND_status_is_pending_THEN_raise_exception(
        self,
    ):
        otp = OTP(
            method=self.otp_method,
            to=self.to,
            hashed_otp=self.hashed_otp,
            encoder=self.hash_stub,
            status=OTPStatusEnum.PENDING.value,
        )
        with self.assertRaises(OTPVerificationFailedException):
            otp.verify(self.invalid_otp_code)

    def test_verify_WHEN_called_AND_status_is_validated_THEN_raise_exception(self):
        otp = OTP(
            method=self.otp_method,
            to=self.to,
            hashed_otp=self.hashed_otp,
            encoder=self.hash_stub,
            status=OTPStatusEnum.VALIDATED.value,
        )
        with self.assertRaises(OTPVerificationFailedException):
            otp.verify(self.invalid_otp_code)
