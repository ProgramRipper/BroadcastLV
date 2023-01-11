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
from .util import pascal_to_upper_snake

__all__ = [
    "EVENT_TO_OP",
    "OP_TO_EVENT",
    "Auth",
    "AuthResponse",
    "Command",
    "Event",
    "Heartbeat",
    "HeartbeatResponse",
    "NeedData",
]


class ConnectionClosed:
    pass


@dataclass
class NeedData:
    size: int


class Event(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __bytes__(self) -> bytes:
        raise NotImplementedError


@dataclass
class Heartbeat(Event):
    content: bytes

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return Heartbeat(buffer)

    def __bytes__(self) -> bytes:
        return self.content


@dataclass
class HeartbeatResponse(Event):
    popularity: int
    content: bytes

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return HeartbeatResponse(
            int.from_bytes(buffer[:4], "big", signed=False),
            buffer[4:],
        )

    def __bytes__(self) -> bytes:
        return self.popularity.to_bytes(4, "big", signed=False) + self.content


@Event.register
class EventStruct(msgspec.Struct):
    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        return msgspec.json.decode(buffer, type=cls)

    def __bytes__(self) -> bytes:
        return msgspec.json.encode(self)


assert issubclass(EventStruct, Event)


class Command(EventStruct, gc=False):
    cmd: str

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        COMMAND_MAP[pascal_to_upper_snake(cls.__name__)] = cls

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        self = super().from_bytes(buffer)

        try:
            if cls is Command and (cls := COMMAND_MAP[self.cmd]) is not Command:
                self = super(Command, cls).from_bytes(buffer)
        except KeyError:
            from warnings import warn

            warn(
                f"Unknown command: {self.cmd} ({buffer.decode()})",
                RuntimeWarning,
            )
            COMMAND_MAP[self.cmd] = Command

        return self


class Auth(EventStruct, omit_defaults=True, gc=False):
    roomid: int
    uid: int | None = None
    protover: int | None = None
    platform: str | None = None
    type: int | None = None
    key: str | None = None


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
