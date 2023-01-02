from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Self

import msgspec

from .command import COMMAND_MAP
from .util import pascal_to_upper_snake

__all__ = [
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


class Command(EventStruct):
    cmd: str

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        COMMAND_MAP[pascal_to_upper_snake(cls.__name__)] = cls


class Auth(EventStruct, omit_defaults=True):
    roomid: int
    uid: int | None = None
    protover: int | None = None
    platform: str | None = None
    type: int | None = None
    key: str | None = None


class AuthResponse(EventStruct):
    code: int
