import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

NULLABLE_STRING = -1

"""
Comparison between '!' and '>' in struct.pack / struct.unpack

| Symbol | Endianness  | Memory Alignment                     |
|--------|------------|---------------------------------------|
| '>'    | Big-endian | Uses the system's native alignment    |
| '!'    | Big-endian | No alignment (standard network order) |
---------------------------------------------------------------

Why use '!'?
1. Cross-platform compatibility: Ensures the same byte structure across different architectures.
2. Network byte order: Common in network protocols like Kafka, HTTP/2, and AWS binary formats.
3. Fixed-size serialization: Prevents unwanted padding that may occur with '>' on some systems.

'!' is the safest option for binary structures requiring portability.
"""


class Message(ABC):
    @classmethod
    def size(cls) -> int:
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, data: bytes):
        pass


@dataclass
class ResponseHeaderV0(Message):
    correlation_id: int

    @classmethod
    def size(cls) -> int:
        return struct.calcsize("!i")

    def to_bytes(self):
        packed_bytes = struct.pack("!i", self.correlation_id)
        message_size = len(packed_bytes)
        fmt = f"!I{message_size}s"
        return struct.pack(fmt, message_size, packed_bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        message_size_format = "!i"
        base_size = struct.calcsize(message_size_format)
        message_size = struct.unpack("!I", data[:base_size])[0]
        base_format = "!i"
        header_size = struct.calcsize(base_format)
        unpacked_base = struct.unpack(base_format, data[base_size:message_size + header_size])
        correlation_id = unpacked_base[0]

        return cls(
            correlation_id=correlation_id
        )


@dataclass
class RequestHeaderV2(Message):
    request_api_key: int
    request_api_version: int
    correlation_id: int
    client_id: Optional[str] = None
    _tagged_fields: Optional[dict] = None

    @classmethod
    def size(cls) -> int:
        return struct.calcsize("!hhih")

    def to_bytes(self):
        if self.client_id:
            client_id_bytes = self.client_id.encode("utf-8")
            client_id_length = len(self.client_id.encode("utf-8"))
            fmt = f"!hhih{client_id_length}s"
            packed_bytes = struct.pack(
                fmt,
                self.request_api_key,
                self.request_api_version,
                self.correlation_id,
                client_id_length,
                client_id_bytes
            )
        else:
            packed_bytes = struct.pack(
                "!hhih",
                self.request_api_key,
                self.request_api_version,
                self.correlation_id,
                NULLABLE_STRING
            )

        message_size = len(packed_bytes)
        fmt = f"!I{message_size}s"
        return struct.pack(fmt, message_size, packed_bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        message_size_format = "!I"
        base_size = struct.calcsize(message_size_format)
        message_size = struct.unpack("!I", data[:base_size])[0]
        header_format = "!hhih"
        header_size = struct.calcsize(header_format)
        unpacked_base = struct.unpack(header_format, data[base_size:base_size + header_size])

        request_api_key, request_api_version, correlation_id, client_id_length = unpacked_base

        if client_id_length == NULLABLE_STRING:
            client_id = None
        else:
            client_id = data[header_size + base_size:base_size + header_size + client_id_length].decode("utf-8")

        return cls(
            request_api_key,
            request_api_version,
            correlation_id,
            client_id
        )


@dataclass
class ApiVersionsResponseV4(Message):
    correlation_id: int
    error_code: int

    @classmethod
    def size(cls) -> int:
        return struct.calcsize("!ih")

    def to_bytes(self):
        packed_bytes = struct.pack("!ih", self.correlation_id, self.error_code)
        message_size = len(packed_bytes)
        fmt = f"!I{message_size}s"
        return struct.pack(fmt, message_size, packed_bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        message_size_format = "!I"
        base_size = struct.calcsize(message_size_format)
        message_size = struct.unpack("!I", data[:base_size])[0]
        fmt = "!ih"
        size = struct.calcsize(fmt)
        unpacked_base = struct.unpack(fmt, data[base_size:size + message_size])
        correlation_id, error_code = unpacked_base

        return cls(
            correlation_id,
            error_code
        )
