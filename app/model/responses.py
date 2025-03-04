import struct
from dataclasses import dataclass
from typing import List

from app.model.base import Serializer, Body, TAG_BUFFER


@dataclass
class ApiKeys(Serializer):
    api_key: int
    min_version: int
    max_version: int

    STRUCT_FORMAT = "!hhhB"

    def to_bytes(self) -> bytes:
        return struct.pack(
            self.STRUCT_FORMAT,
            self.api_key,
            self.min_version,
            self.max_version,
            TAG_BUFFER,
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> "ApiKeys":
        api_key, min_version, max_version, _ = struct.unpack(
            cls.STRUCT_FORMAT, data[: struct.calcsize(cls.STRUCT_FORMAT)]
        )
        return ApiKeys(api_key, min_version, max_version)


@dataclass
class ApiVersionsResponseV4(Body):
    error_code: int
    api_keys: List[ApiKeys]
    throttle_time_ms: int

    STRUCT_FORMAT_ERROR_CODE = "!h"
    STRUCT_FORMAT_ENUM_API_KEYS = "!B"
    STRUCT_FORMAT_THROTTLE = "!iB"

    def to_bytes(self) -> bytes:
        packed_error_code = struct.pack(self.STRUCT_FORMAT_ERROR_CODE, self.error_code)
        packed_num_api_keys = struct.pack(
            self.STRUCT_FORMAT_ENUM_API_KEYS,
            len(self.api_keys) + (len(self.api_keys) > 0),
        )
        packed_keys = b"".join(key.to_bytes() for key in self.api_keys)
        packed_tail = struct.pack(
            self.STRUCT_FORMAT_THROTTLE, self.throttle_time_ms, TAG_BUFFER
        )
        return packed_error_code + packed_num_api_keys + packed_keys + packed_tail

    @classmethod
    def from_bytes(cls, data: bytes) -> "ApiVersionsResponseV4":
        offset = 0
        error_code = struct.unpack(
            cls.STRUCT_FORMAT_ERROR_CODE,
            data[offset : offset + struct.calcsize(cls.STRUCT_FORMAT_ERROR_CODE)],
        )[0]
        offset += struct.calcsize(cls.STRUCT_FORMAT_ERROR_CODE)
        num_api_keys = struct.unpack(
            "!B",
            data[offset : offset + struct.calcsize(cls.STRUCT_FORMAT_ENUM_API_KEYS)],
        )[0]
        offset += struct.calcsize(cls.STRUCT_FORMAT_ENUM_API_KEYS)
        api_keys = []
        api_key_size = struct.calcsize(ApiKeys.STRUCT_FORMAT)
        for _ in range(num_api_keys):
            api_key_obj = ApiKeys.from_bytes(data[offset : offset + api_key_size])
            api_keys.append(api_key_obj)
            offset += api_key_size
        throttle_time_ms = struct.unpack(
            cls.STRUCT_FORMAT_THROTTLE,
            data[offset : offset + struct.calcsize(cls.STRUCT_FORMAT_THROTTLE)],
        )[0]
        return ApiVersionsResponseV4(
            error_code=error_code, api_keys=api_keys, throttle_time_ms=throttle_time_ms
        )
