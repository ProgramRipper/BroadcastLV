import struct
from typing import Literal, NamedTuple, Self

__all__ = (
    "Header",
    "HeaderStruct",
)

HeaderStruct = struct.Struct(">I2H2I")


class Header(NamedTuple):
    size: int
    """封包总大小，包括头部和正文"""
    header_size: int
    """头部大小，一般为 16"""
    protover: Literal[0, 1, 2, 3]
    """协议版本，0 为不压缩普通包，1 为不压缩心跳和认证包，2 zlib 压缩普通包，3 为 brotli 压缩普通包"""
    op: Literal[2, 3, 5, 7, 8]
    """操作码，2 为心跳包，3 为心跳包回复，5 为普通包，7 为认证包，8 为认证包回复"""
    seq: int
    """序列号"""

    @classmethod
    def from_bytes(cls, buffer: bytes, offset: int = 0) -> Self:
        return cls(*HeaderStruct.unpack_from(buffer, offset))

    def __bytes__(self) -> bytes:
        return HeaderStruct.pack(*self)
