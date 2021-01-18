from unittest import TestCase, mock
from application.repositories.otp_repository_redis import OTPRepositoryRedis
from domain.otp.entities.otp.hash_abstract import HashAbstract
from domain.otp.entities.otp.otp import OTP
from domain.otp.enums.otp_method_enum import OTPMethodEnum
from domain.otp.enums.otp_status_enum import OTPStatusEnum
from domain.otp.exceptions.otp_does_not_exist_exception import OTPDoesNotExistException


class TestOTPRepositoryRedis(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.to = 'user@domain.com'

    def setUp(self) -> None:
        self.database_sesssion_mock = mock.Mock()
        self.encoder = mock.Mock(spec=HashAbstract)
        self.otp = OTP(
            method=OTPMethodEnum.EMAIL.value,
            to=self.to,
            encoder=self.encoder,
            status=OTPStatusEnum.PENDING.value,
        )
        self.serialized_otp = 'serialized-otp-entity'

    def test_otp_repository_redis_WHEN_created_THEN_set_repository_attributes(self):
        expected_dict = {'database_session': self.database_sesssion_mock}

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)

        actual_dict = repository.__dict__

        self.assertDictEqual(expected_dict, actual_dict)

    @mock.patch('pickle.dumps')
    def test_save_WHEN_called_THEN_calls_pickle_dumps(self, pickle_dumps_mock):
        pickle_dumps_mock.return_value = self.serialized_otp

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.save(otp=self.otp)

        pickle_dumps_mock.assert_called_once_with(obj=self.otp)

    @mock.patch('pickle.dumps')
    def test_save_WHEN_called_THEN_calls_database_session_set(self, pickle_dumps_mock):
        serialized_otp_entity = self.serialized_otp
        pickle_dumps_mock.return_value = serialized_otp_entity
        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.save(otp=self.otp)

        self.database_sesssion_mock.set.assert_called_once_with(
            name=self.otp.to, value=serialized_otp_entity
        )

    @mock.patch('pickle.dumps')
    def test_save_WHEN_called_THEN_calls_database_session_expire(
        self, pickle_dumps_mock
    ):
        pickle_dumps_mock.return_value = self.serialized_otp
        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.save(otp=self.otp)

        self.database_sesssion_mock.expire.assert_called_once_with(
            name=self.otp.to, time=self.otp.ttl
        )

    @mock.patch('pickle.loads')
    def test_get_WHEN_called_THEN_calls_database_session_get(self, pickle_loads_mock):
        pickle_loads_mock.return_value = self.otp
        self.database_sesssion_mock.get.return_value = self.serialized_otp

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.get(to=self.otp.to)

        self.database_sesssion_mock.get.assert_called_once_with(name=self.otp.to)

    def test_get_WHEN_called_AND_otp_is_not_found_THEN_raise_exception(self):
        self.database_sesssion_mock.get.return_value = None

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)

        with self.assertRaises(OTPDoesNotExistException):
            repository.get(to=self.otp.to)

    @mock.patch('pickle.loads')
    def test_get_WHEN_called_THEN_calls_pickle_loads(self, pickle_loads_mock):
        pickle_loads_mock.return_value = self.otp
        self.database_sesssion_mock.get.return_value = self.serialized_otp

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.get(to=self.otp.to)

        pickle_loads_mock.assert_called_once_with(__data=self.serialized_otp)

    @mock.patch('pickle.loads')
    def test_get_WHEN_called_THEN_calls_database_session_ttl(self, pickle_loads_mock):
        pickle_loads_mock.return_value = self.otp
        self.database_sesssion_mock.get.return_value = self.serialized_otp

        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.get(to=self.otp.to)

        self.database_sesssion_mock.ttl.assert_called_once_with(name=self.otp.to)

    @mock.patch('pickle.loads')
    def test_get_WHEN_called_THEN_returns_otp(self, pickle_loads_mock):
        pickle_loads_mock.return_value = self.otp
        self.database_sesssion_mock.get.return_value = self.serialized_otp
        self.database_sesssion_mock.ttl.return_value = self.otp.ttl

        expected_otp = self.otp
        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        actual_otp = repository.get(to=self.otp.to)

        self.assertEqual(expected_otp, actual_otp)

    def test_delete_WHEN_called_THEN_calls_database_session_delete(self):
        repository = OTPRepositoryRedis(database_session=self.database_sesssion_mock)
        repository.delete(to=self.otp.to)
        self.database_sesssion_mock.delete.assert_called_once_with(names=self.otp.to)
