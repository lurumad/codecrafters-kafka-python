import unittest

from app.model.responses import ApiVersionsResponseV4, ApiKeys


class TestApiVersionsV4(unittest.TestCase):
    def test_api_versions_to_bytes(self):
        api_versions = ApiVersionsResponseV4(
            error_code=35,
            api_keys=[ApiKeys(api_key=18, min_version=0, max_version=4)],
            throttle_time_ms=0,
        )

        data = api_versions.to_bytes()

        self.assertEqual(
            b"\x00#\x02\x00\x12\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00", data
        )
        self.assertEqual("002302001200000004000000000000", data.hex())
