from __future__ import annotations

import sys
import zlib
from enum import Enum, Flag, auto
from itertools import repeat
from operator import length_hint
from typing import Iterable, Literal, overload

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

import brotli

from .event import (
    EVENT_TO_OP,
    OP_TO_EVENT,
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
    "ClientConnection",
    "Connection",
    "ConnectionRole",
    "ConnectionState",
    "ServerConnection",
    "connect",
]


class ConnectionRole(Enum):
    CLIENT = auto()
    SERVER = auto()


class ConnectionState(Flag):
    CONNECTED = 0
    AUTHENTICATING = auto()
    AUTHENTICATED = auto()
    CLOSED = auto()


class Connection:
    state: ConnectionState
    buffer1: bytearray
    buffer2: bytearray
    current: Header | None

    def __init__(self) -> None:
        self.state = ConnectionState.CONNECTED
        self.buffer1 = bytearray()
        self.buffer2 = bytearray()
        self.current = None

    @overload
    def send(self, event: Event) -> bytes:
        ...

    @overload
    def send(self, event: bytes, protover: int, op: int) -> bytes:
        ...

    @overload
    def send(self, event: ConnectionClosed) -> None:
        ...

    def send(
        self,
        event: Event | bytes | ConnectionClosed,
        protover: int | None = None,
        op: int | None = None,
    ) -> bytes | None:
        match event:
            case ConnectionClosed():
                return
            case Command():
                protover = 0
                op = 5
                data = bytearray(2048)
                event.into_buffer(data, HeaderStruct.size)
            case Event() if op := EVENT_TO_OP.get(type(event)):
                protover = 1
                data = bytearray(256)
                event.into_buffer(data, HeaderStruct.size)
            case bytes() if protover is not None and op is not None:
                data = bytearray(HeaderStruct.size + len(event))
                data[HeaderStruct.size :] = event
            case _:
                raise LocalProtocolError(f"Unknown event: {type(event).__name__}")

        Header(
            len(data),
            HeaderStruct.size,
            protover,
            op,
            0,
        ).into_buffer(data)
        return data

    def receive_data(self, data: bytes) -> None:
        self.buffer1.extend(data)

    def next_event(self) -> Event | NeedData:
        try:
            if self.buffer2:
                header = Header.from_bytes(self.buffer2)
                event = Command.from_bytes(
                    self.buffer2[header.header_size : header.size]
                )
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
                case 2 | 3 | 7 | 8:
                    event = OP_TO_EVENT[header.op].from_bytes(buffer)
                case 5:
                    match header.protover:
                        case 0:
                            event = Command.from_bytes(buffer)
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
                case _:
                    raise RemoteProtocolError(f"Unknown op: {header.op}")
        except Exception as e:
            if isinstance(e, RemoteProtocolError):
                raise
            raise RemoteProtocolError from e

        del self.buffer1[: header.size]
        return event


class ClientConnection(Connection):
    @overload
    def send(self, event: Heartbeat | Auth) -> bytes:
        ...

    @overload
    def send(self, event: bytes, protover: int, op: int) -> bytes:
        ...

    @overload
    def send(self, event: ConnectionClosed) -> None:
        ...

    def send(
        self,
        event: Heartbeat | Auth | bytes | ConnectionClosed,
        protover: int = 1,
        op: int | None = None,
    ) -> bytes | None:
        match event:
            case ConnectionClosed():
                self.state |= ConnectionState.CLOSED
                return
            case _ if self.state & ConnectionState.CLOSED:
                raise LocalProtocolError("Connection is closed")
            case Heartbeat():
                if not self.state & ConnectionState.AUTHENTICATED:
                    raise LocalProtocolError("Connection is not authenticated")
            case Auth():
                if self.state & ConnectionState.AUTHENTICATING:
                    raise LocalProtocolError("Connection is already authenticated")
                self.state |= ConnectionState.AUTHENTICATING
            case bytes() if protover is not None and op is not None:
                pass
            case _:
                raise LocalProtocolError(f"Unknown event: {type(event).__name__}")

        return super().send(event, protover, op)  # type: ignore

    def receive_data(self, data: bytes) -> None:
        if not data:
            self.state |= ConnectionState.CLOSED
            return

        if self.state & ConnectionState.CLOSED:
            raise RemoteProtocolError("Connection is closed")

        super().receive_data(data)

    def next_event(
        self,
    ) -> HeartbeatResponse | Command | AuthResponse | NeedData | ConnectionClosed:
        try:
            match event := super().next_event():
                case HeartbeatResponse() | Command():
                    if (  # pragma: worst case  # FIXME: coverage.py incorrectly assumes that this line is partially run
                        not self.state & ConnectionState.AUTHENTICATED
                    ):
                        raise RemoteProtocolError(
                            f"Connection is not authenticated, but received a {type(event).__name__}"
                        )
                case AuthResponse(code):
                    if self.state & ConnectionState.AUTHENTICATED:
                        raise RemoteProtocolError(
                            "Connection is already authenticated, but received a AuthResponse"
                        )
                    elif not self.state & ConnectionState.AUTHENTICATING:
                        raise RemoteProtocolError(
                            "Connection is not authenticating, but received a AuthResponse"
                        )
                    elif code:
                        raise RemoteProtocolError(
                            f"Authentication failed (code: {code})"
                        )
                    self.state |= ConnectionState.AUTHENTICATED
                case NeedData():
                    if self.state & ConnectionState.CLOSED:
                        event = ConnectionClosed()
                case _:
                    raise RemoteProtocolError(f"Unknown event: {type(event).__name__}")
        except RemoteProtocolError:
            self.state |= ConnectionState.CLOSED
            raise

        return event


class ServerConnection(Connection):
    @overload
    def send(self, event: HeartbeatResponse | AuthResponse | Command) -> bytes:
        ...

    @overload
    def send(self, event: bytes, protover: int, op: int) -> bytes:
        ...

    @overload
    def send(self, event: ConnectionClosed) -> None:
        ...

    def send(
        self,
        event: HeartbeatResponse | AuthResponse | Command | bytes | ConnectionClosed,
        protover: int | None = None,
        op: int | None = None,
    ) -> bytes | None:
        match event:
            case ConnectionClosed():
                self.state |= ConnectionState.CLOSED
                return
            case _ if self.state & ConnectionState.CLOSED:
                raise LocalProtocolError("Connection is closed")
            case HeartbeatResponse() | Command() if not self.state & ConnectionState.AUTHENTICATED:
                raise LocalProtocolError("Connection is not authenticated")
            case AuthResponse(code):
                if self.state & ConnectionState.AUTHENTICATED:
                    raise LocalProtocolError("Connection is already authenticated")
                elif not self.state & ConnectionState.AUTHENTICATING:
                    raise LocalProtocolError("Connection is not authenticating")
                self.state |= ConnectionState.AUTHENTICATED
                if code:
                    self.state |= ConnectionState.CLOSED
            case bytes() if protover is not None and op is not None:
                pass
            case _:
                raise LocalProtocolError(f"Unknown event: {type(event).__name__}")

        return super().send(event, protover, op)  # type: ignore

    def multi_send(
        self, events: Iterable[Command | bytes], protover: Literal[2, 3] = 3
    ) -> bytes:
        if not self.state & ConnectionState.AUTHENTICATED:
            raise LocalProtocolError("Connection is not authenticated")

        match protover:
            case 2:
                compress = zlib.compress
            case 3:
                compress = brotli.compress
            case _:
                raise LocalProtocolError(f"Unknown protover: {protover}")

        data = bytearray(length_hint(events, 1) * 2048)
        offset = 0
        for event in events:
            match event:
                case Command():
                    event.into_buffer(data, offset + HeaderStruct.size)
                case bytes():
                    data[offset + HeaderStruct.size :] = event
                case _:
                    raise LocalProtocolError(f"Unknown event: {type(event).__name__}")
            Header(len(data) - offset, HeaderStruct.size, 0, 5, 0).into_buffer(
                data, offset
            )

        data[HeaderStruct.size :] = compress(data)
        Header(len(data), HeaderStruct.size, protover, 5, 0).into_buffer(data)

        return data

    def receive_data(self, data: bytes) -> None:
        if not data:
            self.state |= ConnectionState.CLOSED
            return

        if self.state & ConnectionState.CLOSED:
            raise RemoteProtocolError("Connection is closed")

        super().receive_data(data)

    def next_event(self) -> Heartbeat | Auth | NeedData | ConnectionClosed:
        try:
            match event := super().next_event():
                case Heartbeat():
                    if (  # pragma: worst case  # FIXME: coverage.py incorrectly assumes that this line is partially run
                        not self.state & ConnectionState.AUTHENTICATED
                    ):
                        raise RemoteProtocolError(
                            "Connection is not authenticated, but received a Heartbeat"
                        )
                case Auth():
                    if self.state & ConnectionState.AUTHENTICATED:
                        raise RemoteProtocolError(
                            "Connection is already authenticated, but received a Auth"
                        )
                    elif self.state & ConnectionState.AUTHENTICATING:
                        raise RemoteProtocolError(
                            "Connection is already authenticating, but received a Auth"
                        )
                    self.state |= ConnectionState.AUTHENTICATING
                case NeedData():
                    if self.state & ConnectionState.CLOSED:
                        event = ConnectionClosed()
                case _:
                    raise RemoteProtocolError(f"Unknown event: {type(event).__name__}")
        except RemoteProtocolError:
            self.state |= ConnectionState.CLOSED
            raise

        return event


@overload
def connect(role: Literal[ConnectionRole.CLIENT]) -> ClientConnection:
    ...


@overload
def connect(role: Literal[ConnectionRole.SERVER]) -> ServerConnection:
    ...


@overload
def connect(role: None = None) -> Connection:
    ...


def connect(role: ConnectionRole | None = None) -> Connection:
    match role:
        case ConnectionRole.CLIENT:
            return ClientConnection()
        case ConnectionRole.SERVER:
            return ServerConnection()
        case None:
            return Connection()

    raise ValueError(f"Unknown role: {role}")
