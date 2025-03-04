import threading
import unittest

from app.kafka_broker import KafkaBroker
from app.kafka_client import KafkaClient
from app.model.requests import RequestV2


class TestKafkaBroker(unittest.TestCase):
    def test_parse_incorrect_api_version(self):
        broker = KafkaBroker()
        broker_thread = threading.Thread(target=broker.start)
        broker_thread.start()
        client = KafkaClient()
        request = RequestV2(
            b"\x00\x00\x00\x11\x00\x12\x00\x04o\x7f\xc6a\x00\x07client1"
        )
        response = client.get_api_versions(request)
        broker.stop()
        broker_thread.join()
        self.assertEqual(
            b"\x00\x00\x00\x13o\x7f\xc6a\x00\x00\x02\x00\x12\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00",
            response,
        )

    def test_api_versions(self):
        broker = KafkaBroker()
        broker_thread = threading.Thread(target=broker.start)
        broker_thread.start()
        client = KafkaClient()
        request = RequestV2(
            b"\x00\x00\x00#\x00\x12\x00\x04WP\xd5L\x00\x09kafka-cli\x00\nkafka-cli\x040.1\x00"
        )
        response = client.get_api_versions(request)
        broker.stop()
        broker_thread.join()
        self.assertEqual(
            response,
            b"\x00\x00\x00\x13WP\xd5L\x00\x00\x02\x00\x12\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00",
        )


if __name__ == "__main__":
    unittest.main()
