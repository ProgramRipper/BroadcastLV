from __future__ import annotations

import zlib
from enum import Enum, auto
from typing import overload

import brotli

from .event import (
    COMMAND_MAP,
    Auth,
    AuthResponse,
    Command,
    ConnectionClosed,
    Event,
    Heartbeat,
    HeartbeatResponse,
    NeedData,
)
from .exception import LocalProtocolError, RemoteProtocolError
from .header import Header, HeaderStruct

__all__ = [
    "Connection",
]


class ConnectionState(Enum):
    CONNECTED = auto()
    AUTHENTICATING = auto()
    AUTHENTICATED = auto()
    CLOSED = auto()


class Connection:
    state: ConnectionState
    buffer1: bytearray
    buffer2: bytearray
    current: Header | None = None

    def __init__(self) -> None:
        self.state = ConnectionState.CONNECTED
        self.buffer1 = bytearray()
        self.buffer2 = bytearray()

    @overload
    def send(self, event: Event) -> bytes:
        ...

    @overload
    def send(self, event: ConnectionClosed) -> None:
        ...

    def send(self, event: Event | ConnectionClosed) -> bytes | None:
        if isinstance(event, ConnectionClosed):
            self.state = ConnectionState.CLOSED
            return None

        if self.state == ConnectionState.CLOSED:
            raise LocalProtocolError("Connection is closed")

        if isinstance(event, Heartbeat):
            if self.state not in {
                ConnectionState.AUTHENTICATING,
                ConnectionState.AUTHENTICATED,
            }:  # prevent sending heartbeat before auth, but allow before receiving auth response
                raise LocalProtocolError("Connection is not authenticated")
            op = 2
        elif isinstance(event, Auth):
            if self.state in {
                ConnectionState.AUTHENTICATING,
                ConnectionState.AUTHENTICATED,
            }:  # prevent sending auth twice
                raise LocalProtocolError("Connection is already authenticated")
            self.state = ConnectionState.AUTHENTICATING
            op = 7
        else:
            raise LocalProtocolError(f"Unknown event: {type(event).__name__}")

        data = bytes(event)
        header = bytes(
            Header(
                HeaderStruct.size + len(data),
                HeaderStruct.size,
                1,
                op,
                0,
            )
        )
        return header + data

    def receive_data(self, data: bytes) -> None:
        if not data:
            self.state = ConnectionState.CLOSED
            return

        match self.state:
            case ConnectionState.CONNECTED:
                self.state = ConnectionState.CLOSED
                raise RemoteProtocolError("Connection is not authenticated")
            case ConnectionState.CLOSED:
                raise RemoteProtocolError("Connection is closed")

        self.buffer1.extend(data)

    def next_event(self) -> Event | NeedData:
        if self.buffer2:
            header = Header.from_bytes(self.buffer2)
            event = self._next_command(self.buffer2[header.header_size : header.size])
            del self.buffer2[: header.size]
            return event

        if self.current is None:
            if len(self.buffer1) < HeaderStruct.size:
                return NeedData(HeaderStruct.size - len(self.buffer1))
            self.current = Header.from_bytes(self.buffer1)

        if len(self.buffer1) < self.current.size:
            return NeedData(self.current.size - len(self.buffer1))

        header, self.current = self.current, None
        buffer = self.buffer1[header.header_size : header.size]

        match header.op:
            case 3:
                event = HeartbeatResponse.from_bytes(buffer)

            case 5:
                match header.protover:
                    case 0:
                        event = self._next_command(buffer)

                    case 2:
                        self.buffer2.extend(zlib.decompress(buffer))
                        event: Event = self.next_event()  # type: ignore
                    case 3:
                        self.buffer2.extend(brotli.decompress(buffer))
                        event: Event = self.next_event()  # type: ignore

                    case _:
                        raise RemoteProtocolError(
                            f"Unknown protover: {header.protover}"
                        )

            case 8:
                event = AuthResponse.from_bytes(buffer)
                if event.code != 0:
                    self.state = ConnectionState.CLOSED
                    raise RemoteProtocolError(
                        f"Authentication failed (code: {event.code})"
                    )
                self.state = ConnectionState.AUTHENTICATED

            case _:
                raise RemoteProtocolError(f"Unknown op: {header.op}")

        if self.state != ConnectionState.AUTHENTICATED:
            self.state = ConnectionState.CLOSED
            raise RemoteProtocolError(
                f"Connection is not authenticated, but received a {type(event).__name__}"
            )

        del self.buffer1[: header.size]
        return event

    @staticmethod
    def _next_command(buffer: bytes) -> Command:
        event = Command.from_bytes(buffer)
        try:
            if (type_ := COMMAND_MAP[event.cmd]) is not Command:
                event = type_.from_bytes(buffer)
        except KeyError:
            from warnings import warn

            warn(
                f"Unknown command: {event.cmd} ({buffer.decode()})",
                RuntimeWarning,
            )
            COMMAND_MAP[event.cmd] = Command

        return event
