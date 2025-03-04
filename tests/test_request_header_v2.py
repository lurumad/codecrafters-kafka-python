import unittest

from app.model.headers import RequestHeaderV2


class TestRequestHeaderV2(unittest.TestCase):
    def test_request_header_v2_with_client_id_to_bytes(self):
        header = RequestHeaderV2(b"\x00\x12\x00\x04o\x7f\xc6a\x00\x07client1")

        self.assertEqual(header.request_api_key, 18)
        self.assertEqual(header.request_api_version, 4)
        self.assertEqual(header.correlation_id, 1870644833)
        self.assertEqual(header.client_id, "client1")

    def test_request_header_v2_without_client_id_to_bytes(self):
        header = RequestHeaderV2(b"\x00\x12\x00\x04o\x7f\xc6a\xff\xff")

        self.assertEqual(header.request_api_key, 18)
        self.assertEqual(header.request_api_version, 4)
        self.assertEqual(header.correlation_id, 1870644833)
        self.assertEqual(header.client_id, None)
