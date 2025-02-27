import socket
import struct

from app.model import RequestHeaderV2, Response, RequestV2


class KafkaClient:
    def __init__(self, host='localhost', port=9092):
        self.host = host
        self.port = port

    def send_message(self, topic, request: RequestV2) -> Response:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request.to_bytes())
            data = s.recv(1024)
            return Response.from_bytes(data)
