from unittest import TestCase, mock

from application.hash.bcrypt_provider import BCryptProvider


class TestBCryptProvider(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plain_password = 'plain-password'
        cls.hashed_password = 'hashed-password'
        cls.salt = 'salt'

    def setUp(self) -> None:
        pass

    @mock.patch('bcrypt.hashpw')
    @mock.patch('bcrypt.gensalt')
    def test_to_hash_WHEN_called_THEN_calls_bcrypt_hashpw(
        self, gensalt_mock, hashpw_mock
    ):
        gensalt_mock.return_value = self.salt
        hashpw_mock.return_value = self.hashed_password
        BCryptProvider.to_hash(password=self.plain_password)
        hashpw_mock.assert_called_once_with(
            password=str.encode(self.plain_password), salt=self.salt
        )

    @mock.patch('bcrypt.hashpw')
    @mock.patch('bcrypt.gensalt')
    def test_to_hash_WHEN_called_THEN_returns_hashed_password(
        self, gensalt_mock, hashpw_mock
    ):
        gensalt_mock.return_value = self.salt
        hashpw_mock.return_value = self.hashed_password

        expected_hash = self.hashed_password
        actual_hash = BCryptProvider.to_hash(password=self.plain_password)

        self.assertEqual(expected_hash, actual_hash)

    @mock.patch('bcrypt.checkpw')
    def test_compare_WHEN_called_THEN_calls_bcrypt_checkpw(self, checkpw_mock):
        checkpw_mock.return_value = True
        BCryptProvider.compare(string=self.plain_password, hashed=self.hashed_password)
        checkpw_mock.assert_called_once_with(
            password=str.encode(self.plain_password),
            hashed_password=self.hashed_password,
        )

    @mock.patch('bcrypt.checkpw')
    def test_compare_WHEN_called_THEN_returns_bcrypt_checkpw_result(self, checkpw_mock):
        expected_result = True
        checkpw_mock.return_value = expected_result

        actual_result = BCryptProvider.compare(
            string=self.plain_password, hashed=self.hashed_password
        )

        self.assertEqual(expected_result, actual_result)
