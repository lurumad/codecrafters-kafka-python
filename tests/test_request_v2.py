import unittest

from app.model.headers import RequestHeaderV2
from app.model.requests import RequestV2


class TestRequestV2(unittest.TestCase):
    def test_request_v2(self):
        request = RequestV2(
            b"\x00\x00\x00\x11\x00\x12\x00\x04o\x7f\xc6a\x00\x07client1"
        )

        self.assertEqual(request.header.request_api_key, 18)
        self.assertEqual(request.header.request_api_version, 4)
        self.assertEqual(request.header.correlation_id, 1870644833)
        self.assertEqual(request.header.client_id, "client1")
