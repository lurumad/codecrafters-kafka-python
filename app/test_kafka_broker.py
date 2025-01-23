import threading
import unittest

from app.kafka_broker import KafkaBroker
from app.kafka_client import KafkaClient

class TestKafkaBroker(unittest.TestCase):
    def test_kafka_broker(self):
        expected = b'\x00\x00\x00\x00\x00\x00\x00\x07'
        broker = KafkaBroker()
        broker_thread = threading.Thread(target=broker.start)
        broker_thread.start()
        client = KafkaClient()
        response = client.send_message('topic', 'message')
        broker.stop()
        broker_thread.join()
        self.assertEqual(expected, response)

if __name__ == '__main__':
    unittest.main()