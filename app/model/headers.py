import struct
from dataclasses import dataclass
from typing import Optional

from app.model.base import Header, NULLABLE_STRING


@dataclass
class ResponseHeaderV0(Header):
    correlation_id: int

    STRUCT_FORMAT_HEADER = "!i"

    def to_bytes(self) -> bytes:
        return struct.pack(self.STRUCT_FORMAT_HEADER, self.correlation_id)

    def size(self) -> int:
        return struct.calcsize(self.STRUCT_FORMAT_HEADER)


@dataclass
class RequestHeaderV2(Header):
    request_api_key: int
    request_api_version: int
    correlation_id: int
    client_id: Optional[str]

    STRUCT_FORMAT_HEADER = "!hhih"

    def __init__(self, data: bytes):
        header_size = struct.calcsize(self.STRUCT_FORMAT_HEADER)
        self._data = data[:header_size]
        unpacked_base = struct.unpack(self.STRUCT_FORMAT_HEADER, self._data)

        self.request_api_key = unpacked_base[0]
        self.request_api_version = unpacked_base[1]
        self.correlation_id = unpacked_base[2]
        client_id_length = unpacked_base[3]

        if client_id_length == NULLABLE_STRING:
            self.client_id = None
            self._data = data[:header_size]
        else:
            client_id_bytes = data[header_size : header_size + client_id_length]
            self.client_id = client_id_bytes.decode("utf-8")
            self._data = data[: header_size + client_id_length]

    def size(self) -> int:
        return len(self._data)

    def to_bytes(self) -> bytes:
        if self.client_id:
            client_id_bytes = self.client_id.encode("utf-8")
            client_id_length = len(client_id_bytes)
            fmt = f"{self.STRUCT_FORMAT_HEADER}{client_id_length}s"
            packed_bytes = struct.pack(
                fmt,
                self.request_api_key,
                self.request_api_version,
                self.correlation_id,
                client_id_length,
                client_id_bytes,
            )
        else:
            packed_bytes = struct.pack(
                self.STRUCT_FORMAT_HEADER,
                self.request_api_key,
                self.request_api_version,
                self.correlation_id,
                NULLABLE_STRING,
            )

        return packed_bytes
