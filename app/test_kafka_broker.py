import struct
import threading
import unittest

from app.kafka_broker import KafkaBroker
from app.kafka_client import KafkaClient
from app.model import RequestHeaderV2, RequestV2


class TestKafkaBroker(unittest.TestCase):
    def test_parse_correlation_id(self):
        correlation_id = 1870644833
        broker = KafkaBroker()
        broker_thread = threading.Thread(target=broker.start)
        broker_thread.start()
        client = KafkaClient()
        request = RequestV2(
            header=RequestHeaderV2(
                request_api_key=18,
                request_api_version=4,
                correlation_id=correlation_id,
                client_id=None,
            )
        )
        response = client.send_message('topic', request)
        broker.stop()
        broker_thread.join()
        self.assertEqual(correlation_id, response.header.correlation_id)


if __name__ == '__main__':
    unittest.main()
