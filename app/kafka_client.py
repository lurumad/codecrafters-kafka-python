import socket


class KafkaClient:
    def __init__(self, host='localhost', port=9092):
        self.host = host
        self.port = port

    def send_message(self, topic, message) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(bytes('Placeholder request', 'utf-8'))
            data = s.recv(1024)
            return data