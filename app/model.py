import struct
from dataclasses import dataclass
from typing import Optional

NULLABLE_STRING = -1


@dataclass
class Header:
    correlation_id: int

    def to_bytes(self):
        return struct.pack("!i", self.correlation_id)

    @classmethod
    def from_bytes(cls, data: bytes):
        base_format = "!i"
        base_size = struct.calcsize(base_format)
        unpacked_base = struct.unpack(base_format, data[:base_size])
        correlation_id = unpacked_base[0]

        return cls(
            correlation_id=correlation_id
        )


@dataclass
class Response:
    header: Header

    def to_bytes(self):
        header_bytes = self.header.to_bytes()
        message_size = len(header_bytes)
        fmt = f"!I{message_size}s"
        return struct.pack(fmt, message_size, header_bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        message_size = struct.unpack("!I", data[:4])[0]
        header = Header.from_bytes(data[4:])

        return cls(
            header=header
        )


@dataclass
class RequestHeaderV2:
    request_api_key: int
    request_api_version: int
    correlation_id: int
    client_id: Optional[str] = None
    _tagged_fields: Optional[dict] = None

    def to_bytes(self):
        if self.client_id:
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
            client_id_bytes = self.client_id.encode("utf-8")
            client_id_length = len(self.client_id.encode("utf-8"))
            fmt = f"!hhih{client_id_length}s"
            return struct.pack(
                fmt,
                self.request_api_key,
                self.request_api_version,
                self.correlation_id,
                client_id_length,
                client_id_bytes
            )

        return struct.pack(
            "!hhih",
            self.request_api_key,
            self.request_api_version,
            self.correlation_id,
            NULLABLE_STRING
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        base_format = "!hhih"
        base_size = struct.calcsize(base_format)
        unpacked_base = struct.unpack(base_format, data[:base_size])

        request_api_key, request_api_version, correlation_id, client_id_length = unpacked_base

        if client_id_length == NULLABLE_STRING:
            client_id = None
        else:
            client_id = data[base_size:base_size+client_id_length].decode("utf8")

        return cls(
            request_api_key=request_api_key,
            request_api_version=request_api_version,
            correlation_id=correlation_id,
            client_id=client_id
        )


@dataclass
class RequestV2:
    header: RequestHeaderV2

    def to_bytes(self):
        header_bytes = self.header.to_bytes()
        message_size = len(header_bytes)
        fmt = f"!I{message_size}s"
        return struct.pack(fmt, message_size, header_bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        message_size = struct.unpack("!I", data[:4])[0]
        header = RequestHeaderV2.from_bytes(data[4:])

        return cls(
            header=header
        )
