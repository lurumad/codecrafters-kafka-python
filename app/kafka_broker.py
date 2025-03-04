import socket
import threading

from app.model.base import KafkaApiKeys, Message
from app.model.headers import ResponseHeaderV0
from app.model.requests import RequestV2
from app.model.responses import ApiVersionsResponseV4, ApiKeys

SUPPORTED_API_KEYS = {18: [0, 1, 2, 4]}


class KafkaBroker:
    def __init__(self, host="localhost", port=9092):
        self.threads = []
        self.host = host
        self.port = port
        self.server = socket.create_server((self.host, self.port), reuse_port=True)
        self.server.listen()
        self.running = False

    def start(self) -> None:
        self.running = True
        print(f"Kafka Broker listening on {self.host}:{self.port}...")
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                )
                client_thread.start()
                self.threads.append(client_thread)
            except (OSError, ConnectionAbortedError):
                break

    def handle_client(self, client_socket: socket.socket) -> None:
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    request = RequestV2(data)

                    if request.header.request_api_key == KafkaApiKeys.ApiVersions.value:
                        error_code = (
                            0
                            if request.header.request_api_version
                            in SUPPORTED_API_KEYS[KafkaApiKeys.ApiVersions.value]
                            else 35
                        )

                        response = Message(
                            header=ResponseHeaderV0(request.header.correlation_id),
                            body=ApiVersionsResponseV4(
                                error_code=error_code,
                                api_keys=[
                                    ApiKeys(
                                        api_key=KafkaApiKeys.ApiVersions.value,
                                        min_version=min(SUPPORTED_API_KEYS[18]),
                                        max_version=max(SUPPORTED_API_KEYS[18]),
                                    )
                                ],
                                throttle_time_ms=0,
                            ),
                        )
                        client_socket.sendall(response.to_bytes())

                    else:
                        raise NotImplementedError

                except (ConnectionResetError, BrokenPipeError):
                    print("Client disconnected unexpectedly")
                    break

    def stop(self) -> None:
        self.running = False
        self.server.close()
