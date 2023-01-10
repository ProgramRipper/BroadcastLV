import pytest

from broadcastlv.connection import (
    ClientConnection,
    ConnectionRole,
    ConnectionState,
    connect,
)
from broadcastlv.event import Auth, Command, ConnectionClosed, Heartbeat
from broadcastlv.exception import LocalProtocolError, RemoteProtocolError


def test_init():
    assert type(connect(ConnectionRole.CLIENT)) is ClientConnection


def test_send():
    conn = ClientConnection()

    conn.send(ConnectionClosed())
    assert conn.state == ConnectionState.CLOSED

    with pytest.raises(LocalProtocolError, match="Connection is closed"):
        conn.send(Heartbeat(b""))

    conn = ClientConnection()

    with pytest.raises(LocalProtocolError, match="Connection is not authenticated"):
        conn.send(Heartbeat(b""))

    conn.send(Auth(0))
    assert conn.state == ConnectionState.AUTHENTICATING

    conn.receive_data(
        b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00{"code":0}'
    )
    conn.next_event()
    conn.send(Heartbeat(b""))
    conn.send(b"", 0, 0)
    with pytest.raises(LocalProtocolError, match="Connection is already authenticated"):
        conn.send(Auth(0))
    with pytest.raises(LocalProtocolError, match="Unknown event: Command"):
        conn.send(Command("TEST"))  # type: ignore


def test_next_event():
    conn = ClientConnection()
    conn.send(Auth(0))

    conn.receive_data(
        b"\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00"
    )
    conn.next_event()
    conn.receive_data(
        b'{"code":0}'
        b"\x00\x00\x00\x18\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\xbfRtest"
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00test"
    )
    conn.next_event()
    assert conn.state == ConnectionState.AUTHENTICATED
    conn.next_event()
    with pytest.raises(RemoteProtocolError, match="Unknown event: Heartbeat"):
        conn.next_event()
    assert conn.state == ConnectionState.CLOSED

    conn = ClientConnection()
    conn.receive_data(
        b"\x00\x00\x00\x18\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\xbfRtest"
    )
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is not authenticated, but received a HeartbeatResponse",
    ):
        conn.next_event()

    conn = ClientConnection()
    conn.receive_data(
        b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00{"code":0}'
    )
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is not authenticating, but received a AuthResponse",
    ):
        conn.next_event()

    conn = ClientConnection()
    conn.send(Auth(0))
    conn.receive_data(
        b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00{"code":1}'
    )
    with pytest.raises(
        RemoteProtocolError,
        match=r"Authentication failed \(code: 1\)",
    ):
        conn.next_event()
