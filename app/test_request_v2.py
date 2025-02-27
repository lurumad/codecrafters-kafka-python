import unittest

from app.model import RequestV2, RequestHeaderV2


class TestRequestV2(unittest.TestCase):
    def test_request_v2_to_bytes(self):
        request = RequestV2(
            header=RequestHeaderV2(
                request_api_key=18,
                request_api_version=4,
                correlation_id=1870644833,
            )
        )

        data = request.to_bytes()

        self.assertEqual(b"\x00\x00\x00\n\x00\x12\x00\x04o\x7f\xc6a\xff\xff", data)

    def test_request_v2_from_bytes(self):
        expected = RequestV2(
            header=RequestHeaderV2(
                request_api_key=18,
                request_api_version=4,
                correlation_id=1870644833,
            )
        )

        data = RequestV2.from_bytes(b"\x00\x00\x00\n\x00\x12\x00\x04o\x7f\xc6a\xff\xff")

        self.assertEqual(expected, data)
