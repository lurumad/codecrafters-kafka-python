import socket

from app.model import ResponseHeaderV0, RequestHeaderV2, Message, ApiVersionsResponseV4


class KafkaClient:
    def __init__(self, host="localhost", port=9092):
        self.host = host
        self.port = port

    def send_message(self, topic, request: RequestHeaderV2) -> any:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.to_bytes())
            data = s.recv(1024)
            return ApiVersionsResponseV4.from_bytes(data)

