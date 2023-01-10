from broadcastlv.event import (
    Auth,
    AuthResponse,
    Command,
    Heartbeat,
    HeartbeatResponse,
    NeedData,
)


def test_need_data():
    assert NeedData(1).size == 1


def test_heartbeat():
    assert Heartbeat(b"abc").content == b"abc"
    assert Heartbeat.from_bytes(b"abc") == Heartbeat(b"abc")
    assert bytes(Heartbeat(b"abc")) == b"abc"


def test_heartbeat_response():
    heartbeat_response = HeartbeatResponse(1, b"abc")
    assert heartbeat_response.popularity == 1
    assert heartbeat_response.content == b"abc"
    assert HeartbeatResponse.from_bytes(b"\x00\x00\x00\x01abc") == heartbeat_response
    assert bytes(heartbeat_response) == b"\x00\x00\x00\x01abc"


def test_command():
    assert bytes(Command(cmd="COMMAND")) == b'{"cmd":"COMMAND"}'
    assert (
        bytes(Command.from_bytes(b'{"cmd":"COMMAND","ignored":"field"}'))
        == b'{"cmd":"COMMAND"}'
    )
    Command.from_bytes(b'{"cmd":"COMMAND"}')

    class Unknown(Command):
        ...

    assert Command.from_bytes(b'{"cmd":"UNKNOWN"}') == Unknown(cmd="UNKNOWN")


def test_auth():
    auth = Auth(123, 456, 3, "web", 2, "token")
    assert auth.roomid == 123
    assert auth.uid == 456
    assert auth.protover == 3
    assert auth.platform == "web"
    assert auth.type == 2
    assert auth.key == "token"
    assert (
        Auth.from_bytes(
            b'{"roomid":123,"uid":456,"protover":3,"platform":"web","type":2,"key":"token"}'
        )
        == auth
    )
    assert (
        bytes(auth)
        == b'{"roomid":123,"uid":456,"protover":3,"platform":"web","type":2,"key":"token"}'
    )


def test_auth_omit_defaults():
    auth = Auth(123)
    assert auth.roomid == 123
    assert auth.uid is None
    assert auth.protover is None
    assert auth.platform is None
    assert auth.type is None
    assert auth.key is None
    assert Auth.from_bytes(b'{"roomid":123}') == auth
    assert bytes(auth) == b'{"roomid":123}'


def test_auth_response():
    auth_response = AuthResponse(0)
    assert auth_response.code == 0
    assert AuthResponse.from_bytes(b'{"code":0}') == auth_response
    assert bytes(auth_response) == b'{"code":0}'
