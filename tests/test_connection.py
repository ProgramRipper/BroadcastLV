import pytest

from broadcastlv.connection import Connection, connect
from broadcastlv.event import (
    Auth,
    AuthResponse,
    Command,
    ConnectionClosed,
    Heartbeat,
    HeartbeatResponse,
    NeedData,
)
from broadcastlv.exception import LocalProtocolError, RemoteProtocolError


def test_init():
    assert type(connect()) is Connection
    with pytest.raises(ValueError, match="Unknown role: 2"):
        connect(2)  # type: ignore


def test_send():
    conn = Connection()

    assert (
        conn.send(Heartbeat(b"test"))
        == b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00test"
    )
    assert (
        conn.send(HeartbeatResponse(114514, b"test"))
        == b"\x00\x00\x00\x18\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\xbfRtest"
    )
    assert (
        conn.send(Command("TEST"))
        == b'\x00\x00\x00\x1e\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00{"cmd":"TEST"}'
    )
    assert (
        conn.send(Auth(1, 2, 3, "4", 5, "6"))
        == b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
    )
    assert (
        conn.send(AuthResponse(1))
        == b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00{"code":1}'
    )
    assert (
        conn.send(b"test", 1, 2)
        == b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00test"
    )
    with pytest.raises(LocalProtocolError, match="Unknown event: object"):
        conn.send(object())  # type: ignore

    assert conn.send(ConnectionClosed()) is None


def test_receive_data():
    conn = Connection()

    conn.receive_data(b"test")
    conn.receive_data(b"")
    conn.receive_data(b"")
    with pytest.raises(RemoteProtocolError, match="Connection is closed"):
        conn.receive_data(b"test")


def test_next_event():
    conn = Connection()

    conn.receive_data(b"\x00\x00\x00\x14\x00\x10\x00\x01")
    assert conn.next_event() == NeedData(8)

    conn.receive_data(b"\x00\x00\x00\x02\x00\x00\x00\x00")
    assert conn.next_event() == NeedData(4)

    conn.receive_data(
        b"test"
        b"\x00\x00\x00\x18\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x01\xbfRtest"
        b'\x00\x00\x00\x1e\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00{"cmd":"TEST"}'
        b'\x00\x00\x00S\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":1,"uid":2,"protover":3,"platform":"4","type":5,"key":"6"}'
        b'\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00{"code":1}'
        b"\x00\x00\x001\x00\x10\x00\x02\x00\x00\x00\x05\x00\x00\x00\x00x\x9cc``\x90c\x10`\x00\x01V\x10Q\xad\x94\x9c\x9b\xa2d\xa5\x14\xe2\x1a\x1c\xa2T\x0b\x00%0\x04b"
        b'\x00\x00\x002\x00\x10\x00\x03\x00\x00\x00\x05\x00\x00\x00\x00\x8b\x0e\x80\x00\x00\x00\x1e\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00{"cmd":"TEST"}\x03'
    )
    assert conn.next_event() == Heartbeat(b"test")
    assert conn.next_event() == HeartbeatResponse(114514, b"test")
    assert conn.next_event() == Command("TEST")
    assert conn.next_event() == Auth(1, 2, 3, "4", 5, "6")
    assert conn.next_event() == AuthResponse(1)
    assert conn.next_event() == Command("TEST")
    assert conn.next_event() == Command("TEST")

    conn.receive_data(
        b"\x00\x00\x00\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    with pytest.raises(RemoteProtocolError, match="Unknown op: 0"):
        conn.next_event()

    conn = Connection()
    conn.receive_data(
        b"\x00\x00\x00\x10\x00\x10\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00"
    )
    with pytest.raises(RemoteProtocolError, match="Unknown protover: 1"):
        conn.next_event()

    conn = Connection()
    conn.receive_data(
        b"\x00\x00\x00\x1a\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00NOT A JSON"
    )
    with pytest.raises(RemoteProtocolError):
        conn.next_event()
