import pytest

from broadcastlv.connection import (
    Connection,
    ConnectionRole,
    ConnectionState,
    ServerConnection,
)
from broadcastlv.event import (
    Auth,
    AuthResponse,
    Command,
    ConnectionClosed,
    HeartbeatResponse,
)
from broadcastlv.exception import LocalProtocolError, RemoteProtocolError


def test_init():
    assert type(Connection(ConnectionRole.SERVER)) is ServerConnection


def test_send():
    conn = ServerConnection()

    conn.send(ConnectionClosed())
    assert conn.state == ConnectionState.CLOSED

    with pytest.raises(LocalProtocolError, match="Connection is closed"):
        conn.send(HeartbeatResponse(0, b""))

    conn = ServerConnection()

    with pytest.raises(LocalProtocolError, match="Connection is not authenticated"):
        conn.send(HeartbeatResponse(0, b""))

    conn.receive_data(
        b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
    )
    conn.next_event()
    conn.send(AuthResponse(0))
    assert conn.state == ConnectionState.AUTHENTICATED

    conn.send(HeartbeatResponse(0, b""))
    conn.send(Command("TEST"))
    conn.send(b"", 0, 0)
    with pytest.raises(LocalProtocolError, match="Connection is not authenticating"):
        conn.send(AuthResponse(0))
    with pytest.raises(LocalProtocolError, match="Unknown event: Auth"):
        conn.send(Auth(0))  # type: ignore

    conn = ServerConnection()
    conn.receive_data(
        b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
    )
    conn.next_event()
    conn.send(AuthResponse(1))
    assert conn.state == ConnectionState.CLOSED


def test_next_event():
    conn = ServerConnection()
    conn.receive_data(b"\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00")
    conn.next_event()
    conn.receive_data(
        b'{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00test"
        b"\x00\x00\x00\x18\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\xbfRtest"
    )
    conn.next_event()
    assert conn.state == ConnectionState.AUTHENTICATING
    conn.send(AuthResponse(0))
    conn.next_event()
    with pytest.raises(RemoteProtocolError, match="Unknown event: HeartbeatResponse"):
        conn.next_event()
    assert conn.state == ConnectionState.CLOSED

    conn = ServerConnection()
    conn.receive_data(
        b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
        b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
    )
    conn.next_event()
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is already authenticated, but received a Auth",
    ):
        conn.next_event()

    conn = ServerConnection()
    conn.receive_data(
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00test"
    )
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is not authenticated, but received a Heartbeat",
    ):
        conn.next_event()
