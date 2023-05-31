from __future__ import annotations

import sys
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Literal

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

import msgspec

from .command import COMMAND_MAP
from .exception import UnknownCommandWarning
from .util import add_from_bytes, pascal_to_upper_snake

__all__ = [
    "EVENT_TO_OP",
    "OP_TO_EVENT",
    "Auth",
    "AuthResponse",
    "Command",
    "ConnectionClosed",
    "Event",
    "Heartbeat",
    "HeartbeatResponse",
    "NeedData",
]


class ConnectionClosed:
    _instance = None

    def __new__(cls) -> Self | ConnectionClosed:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


@dataclass
class NeedData:
    size: int


class Event(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> Self:
        raise NotImplementedError

    def into_buffer(self, buffer: bytearray, offset: int = 0) -> None:
        buffer[offset:] = bytes(self)

    @abstractmethod
    def __bytes__(self) -> bytes:
        raise NotImplementedError


@dataclass
class Heartbeat(Event):
    content: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return Heartbeat(data)

    def __bytes__(self) -> bytes:
        return self.content


@dataclass
class HeartbeatResponse(Event):
    popularity: int
    content: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return HeartbeatResponse(
            int.from_bytes(data[:4], "big", signed=False), data[4:]
        )

    def __bytes__(self) -> bytes:
        return self.popularity.to_bytes(4, "big", signed=False) + self.content


_encoder = msgspec.json.Encoder()


@Event.register
class EventStruct(msgspec.Struct):
    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return msgspec.json.decode(data, type=cls)

    def into_buffer(self, buffer: bytearray, offset: int = 0) -> None:
        _encoder.encode_into(self, buffer, offset)

    def __bytes__(self) -> bytes:
        return _encoder.encode(self)


assert issubclass(EventStruct, Event)


class Command(EventStruct, gc=False):
    cmd: str

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        COMMAND_MAP[pascal_to_upper_snake(cls.__name__)] = cls

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        if cls is Command:
            self = _command_decode(data)
            try:
                if (cls := COMMAND_MAP[self.cmd]) is not Command:
                    self = cls.from_bytes(data)
            except KeyError:
                from pprint import pformat
                from warnings import warn

                warn(
                    f"Unknown command: {self.cmd} ({pformat(msgspec.json.decode(data))})\n"
                    "Please raise an issue on GitHub.",
                    UnknownCommandWarning,
                )
                COMMAND_MAP[self.cmd] = Command
            except msgspec.ValidationError:
                from pprint import pformat
                from traceback import print_exc
                from warnings import warn

                print_exc()
                warn(
                    f"Failed to decode command: {self.cmd} ({pformat(msgspec.json.decode(data))})\n"
                    "Please raise an issue on GitHub.",
                    RuntimeWarning,
                )
        else:
            self = super().from_bytes(data)

        return self


_command_decode = msgspec.json.Decoder(Command).decode


@add_from_bytes
class Auth(EventStruct, omit_defaults=True, gc=False):
    roomid: int
    uid: int | None = None
    protover: int | None = None
    platform: str | None = None
    type: int | None = None
    key: str | None = None


@add_from_bytes
class AuthResponse(EventStruct, gc=False):
    code: int


EVENT_TO_OP: dict[type[Event], Literal[2, 3, 5, 7, 8]] = {
    Heartbeat: 2,
    HeartbeatResponse: 3,
    Command: 5,
    Auth: 7,
    AuthResponse: 8,
}

OP_TO_EVENT: dict[Literal[2, 3, 5, 7, 8], type[Event]] = {
    2: Heartbeat,
    3: HeartbeatResponse,
    5: Command,
    7: Auth,
    8: AuthResponse,
}
