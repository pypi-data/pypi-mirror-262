from django.test import TestCase  # type: ignore

from analytics.safety.function import decryption, encryption


class SafetyTests(TestCase):
    """safetyモジュールのテスト"""

    def setUp(self):
        self.original = "test"

    def tearDown(self):
        del self.original

    def test_function_decryption(self):
        """復号化テスト"""
        encrypt = encryption(self.original)
        decrypt = decryption(encrypt)
        self.assertEqual(decrypt, self.original)
