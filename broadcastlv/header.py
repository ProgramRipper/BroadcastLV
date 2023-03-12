from __future__ import annotations

import struct
import sys
from typing import NamedTuple

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

__all__ = [
    "Header",
    "HeaderStruct",
]

HeaderStruct = struct.Struct(">I2H2I")


class Header(NamedTuple):
    size: int
    """封包总大小，包括头部和正文"""
    header_size: int
    """头部大小，一般为 16"""
    protover: int
    """协议版本，0：不压缩普通包，1：不压缩心跳和认证包，2：zlib 压缩普通包，3：brotli 压缩普通包"""
    op: int
    """操作码，2：心跳包，3：心跳包回复，5：普通包，7：认证包，8：认证包回复"""
    seq: int
    """序列号"""

    @classmethod
    def from_bytes(cls, buffer: bytes, offset: int = 0) -> Self:
        return cls(*HeaderStruct.unpack_from(buffer, offset))

    def into_buffer(self, buffer: bytearray, offset: int = 0) -> None:
        HeaderStruct.pack_into(buffer, offset, *self)

    def __bytes__(self) -> bytes:
        return HeaderStruct.pack(*self)
