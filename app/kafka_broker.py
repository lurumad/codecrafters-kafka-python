import socket

from app.model import ResponseHeaderV0, RequestHeaderV2, ApiVersionsResponseV4


class KafkaBroker:
    def __init__(self, host='localhost', port=9092):
        self.host = host
        self.port = port
        self.server = socket.create_server(("localhost", 9092), reuse_port=True)
        self.server.listen()
        self.running = False

    def start(self) -> None:
        self.running = True
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                with client_socket:
                    data = client_socket.recv(1024)
                    if data:
                        request = RequestHeaderV2.from_bytes(data)

                        if request.request_api_version < 0 or request.request_api_version > 4:
                            response = ApiVersionsResponseV4(
                                correlation_id=request.correlation_id,
                                error_code=35
                            )
                            client_socket.sendall(response.to_bytes())
                            return

                        response = ResponseHeaderV0(
                            correlation_id=request.correlation_id
                        )
                        client_socket.sendall(response.to_bytes())
            except (OSError, ConnectionAbortedError):
                break

    def stop(self) -> None:
        self.running = False
        self.server.close()
