import unittest

from app.model import RequestHeaderV2


class TestRequestV2(unittest.TestCase):
    def test_request_header_v2_with_client_id_to_bytes(self):
        header = RequestHeaderV2(
            request_api_key=18,
            request_api_version=4,
            correlation_id=1870644833,
            client_id='client1'
        )

        data = header.to_bytes()

        self.assertEqual(b"\x00\x00\x00\x11\x00\x12\x00\x04o\x7f\xc6a\x00\x07client1", data)

    def test_request_header_v2_without_client_id_to_bytes(self):
        header = RequestHeaderV2(
            request_api_key=18,
            request_api_version=4,
            correlation_id=1870644833,
        )

        data = header.to_bytes()

        self.assertEqual(b"\x00\x00\x00\n\x00\x12\x00\x04o\x7f\xc6a\xff\xff", data)

    def test_request_header_v2_with_client_id_from_bytes(self):
        expected = RequestHeaderV2(
            request_api_key=18,
            request_api_version=4,
            correlation_id=1870644833,
            client_id='client1'
        )

        response = RequestHeaderV2.from_bytes(b"\x00\x00\x00\x11\x00\x12\x00\x04o\x7f\xc6a\x00\x07client1")

        self.assertEqual(expected, response)

    def test_request_header_v2_without_client_id_from_bytes(self):
        expected = RequestHeaderV2(
            request_api_key=18,
            request_api_version=4,
            correlation_id=1870644833,
        )

        response = RequestHeaderV2.from_bytes(b"\x00\x00\x00\n\x00\x12\x00\x04o\x7f\xc6a\xff\xff")

        self.assertEqual(expected, response)
