import struct
from dataclasses import dataclass

from app.model.base import Message, Serializer, RawBody
from app.model.headers import RequestHeaderV2


@dataclass
class RequestV2(Message, Serializer):
    header: RequestHeaderV2
    body: RawBody

    STRUCT_FORMAT_MESSAGE_SIZE = "!I"

    def __init__(self, data: bytes):
        base_size = struct.calcsize(self.STRUCT_FORMAT_MESSAGE_SIZE)
        self.size = struct.unpack(self.STRUCT_FORMAT_MESSAGE_SIZE, data[:base_size])[0]
        self.header = RequestHeaderV2(data[base_size:])
        self.body = RawBody(data[base_size + self.header.size() :])

    def to_bytes(self) -> bytes:
        header_bytes = self.header.to_bytes()
        body_bytes = self.body.to_bytes()
        message_size = len(header_bytes) + len(body_bytes)
        fmt = f"{self.STRUCT_FORMAT_MESSAGE_SIZE}{len(header_bytes)}s{len(body_bytes)}s"
        return struct.pack(fmt, message_size, header_bytes, body_bytes)
