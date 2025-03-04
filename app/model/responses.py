import struct
from dataclasses import dataclass
from typing import List

from app.model.base import Serializer, Body


@dataclass
class ApiKeys(Serializer):
    api_key: int
    min_version: int
    max_version: int

    def to_bytes(self) -> bytes:
        return struct.pack("!hhhB", self.api_key, self.min_version, self.max_version, 0)


@dataclass
class ApiVersionsResponseV4(Body):
    error_code: int
    api_keys: List[ApiKeys]
    throttle_time_ms: int

    def to_bytes(self) -> bytes:
        packed_header = struct.pack("!h", self.error_code)
        num_api_keys_packed = struct.pack("!B", 2)
        packed_keys = b"".join(key.to_bytes() for key in self.api_keys)
        packed_tail = struct.pack("!iB", self.throttle_time_ms, 0)
        return packed_header + num_api_keys_packed + packed_keys + packed_tail
