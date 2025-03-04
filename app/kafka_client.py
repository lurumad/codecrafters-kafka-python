import socket

from app.model.requests import RequestV2


class KafkaClient:
    def __init__(self, host="localhost", port=9092):
        self.host = host
        self.port = port

    def get_api_versions(self, request: RequestV2) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.to_bytes())
            return s.recv(1024)
