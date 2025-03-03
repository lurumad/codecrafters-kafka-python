import unittest

from app.model import ApiVersionsResponseV4


class TestApiVersionsV4(unittest.TestCase):
    def test_api_versions_to_bytes(self):
        api_versions = ApiVersionsResponseV4(
            correlation_id=1333056139,
            error_code=35
        )

        data = api_versions.to_bytes()

        self.assertEqual(b"\x00\x00\x00\x06Ot\xd2\x8b\x00#", data)
        self.assertEqual("000000064f74d28b0023", data.hex())
