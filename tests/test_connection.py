import pytest

from broadcastlv.command.danmu_msg import (
    ActivityInfo,
    DanmuMsg,
    DanmuMsgInfo,
    DanmuMsgInfoCheckInfo,
    DanmuMsgInfoLevel,
    DanmuMsgInfoMedal,
    DanmuMsgInfoMeta,
    DanmuMsgInfoSender,
    DmType,
    EmotionOptions,
    ModeInfo,
)
from broadcastlv.connection import Connection, ConnectionState
from broadcastlv.event import (
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
from broadcastlv.exception import LocalProtocolError, RemoteProtocolError


def test_connection():
    conn = Connection()

    # send auth
    assert (
        conn.send(Auth(8131361))
        == b'\x00\x00\x00"\x00\x10\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00{"roomid":8131361}'
    )

    # initial state
    assert conn.next_event() == NeedData(size=16)

    # receive auth response
    conn.receive_data(
        b"\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00"
    )
    assert conn.next_event() == NeedData(size=10)
    conn.receive_data(b'{"code":0}')
    assert conn.next_event() == AuthResponse(code=0)
    assert conn.next_event() == NeedData(size=16)

    # receive unknown command
    conn.receive_data(b"\x00\x00\x00)\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00")
    assert conn.next_event() == NeedData(size=25)
    conn.receive_data(b'{"cmd":"UNKNOWN_COMMAND"}')
    with pytest.warns(RuntimeWarning, match="Unknown command: UNKNOWN_COMMAND"):
        assert conn.next_event() == Command(cmd="UNKNOWN_COMMAND")
    assert COMMAND_MAP["UNKNOWN_COMMAND"] is Command
    assert conn.next_event() == NeedData(size=16)

    # send heartbeat
    assert (
        conn.send(Heartbeat(b""))
        == b"\x00\x00\x00\x10\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00"
    )

    # receive heartbeat response
    conn.receive_data(
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00"
    )
    assert conn.next_event() == NeedData(size=4)
    conn.receive_data(b"\x00\x00\x00\x01")
    assert conn.next_event() == HeartbeatResponse(popularity=1, content=bytearray(b""))
    assert conn.next_event() == NeedData(size=16)

    # receive zlib compressed data
    conn.receive_data(
        b"\x00\x00\x01\xf6\x00\x10\x00\x02\x00\x00\x00\x05\x00\x00\x00\x00"
        b"x\xdatQMk\x141\x18\x1e\x04\xef\xfe\x86\xd7k\x0e\x99\x8fffr[\xb6[\xeb\xa5BY\xd8\x83HH'\xe940\x99,I\xb6(e\x0f\x1e\xa4\x87\x16\x15\xf1h\x0f\xdeD\xa17\x0f\x16\xa4\x7f\xc6\xe9\xea\xbf\x90\x8c\xb3\xb5E;\x0c\xc3\xbc\xcf\x13\xde\xe7#Q\x14\xe9\xe8A\x14\x9e\xfb\xe1s\x04\x95\x16@a6\x9a\x8e\xb7'\x9bl\xbc=\xday4\x01\x04\x82{\x0e\xf4\x08\xda\x85\x06\x1a\xc7\tA\xe0\xe5s\xcf\x9c\xe6M\x03\x14\x02\x04\x03\xd6p[\xcb\x01\xfbqq\xb1\xfap\xf2\xf3\xf2\x18\x96\xcb(\xbaw\xf2?\xb1\xc7;\xd3\xc9\xeeh<e\xb3'\xbb\x9b7\xb4*\xd3z\xab\xf6\x16^\x996\xcc\xb5\xe5B\x02\xc5K\x04B\xbb\xcaX\t4C\xb0\xcf[\xc7\xb4\x14\xbc\t\x87x[\x1d\x18\xcb\xac1Z\t\xa0I\x89qFJ\x04\xf5\x82[\xc1\x1ay(\x1b\xa0\x18\x81\xaaL\xcb\xc2\x89\xf0\xefX\xa3\xea\x03/\xff\x8c\xfd.V\x99\xc6X\xa0\x04\x93\xbc\xd8\xc8n\xa1l\xcfX!-\xd08!i\x92l\x90\xdb\xacl\xc5]\x94\xf3\xdc\xfa\x7f\xc9\xc1V\xba\x9e[\xaeC\x81\xab\xd3/\xdd\xbb\xcf\xab\xefo\x01\xc1\x907/J\x04n.+\x15\xe2B\xa8<\xb4\xed\xfb(\xa4\xc8\xe2$\x8fCAJ\xc8\xd6+\xaf\xa4\x03\xfa4~\xd6gts+y\xb0\x86@\xbb\x9a\xf9\x17s\xd9\x0fs\xab\x0eU#k9@\x18\xc1\xba\xbe8-H\x9a\x16\xf8Z?&yB0)r\x9ceyp\x12V2!]\x05\x14\xae\xbe\xbe\xfcu\xfc\xa6;}u\xf5\xfaS\xf7\xed\x12\xaey\xd5\xee\x1b\xa0\xf0pk\x8bd\xe5\xa47\xad\x1a\x16\xae\xa0W\xf3JK\xe7\xb9\x9e\xff\xddO\x02lU]K\xcb\x02}\x93\xc9\xd2<\xc58\xc7\x18\xc1\"\x98\xcc\xca\"\xc1e\x9a\"X\x0c\xc5u\x1f\xdf\x87\xf7\xfc\xac;?\x9b\xc1\x80\xafo\x14`\xb9\xfc\x1d\x00\x00\xff\xff\x15l\xf2\xb1"
    )
    cmd = conn.next_event()
    assert isinstance(cmd, Command) and cmd.cmd == "WATCHED_CHANGE"
    cmd = conn.next_event()
    assert isinstance(cmd, Command) and cmd.cmd == "INTERACT_WORD"
    assert conn.next_event() == NeedData(size=16)

    # receive brotli compressed data
    conn.receive_data(
        b"\x00\x00\x01Z\x00\x10\x00\x03\x00\x00\x00\x05\x00\x00\x00\x00"
        b'\x1bf\x02\x00\xac\n\xec\xa6\xc7\xcbYU\xc5\xfd\xf0C\xd8\xac"\xcbG\xa3x#K7\x99\xca\x1c\xc2\xf4\t\xc6 \xf4\xba\xb6\xcc\xad\x08\xc2YZ$\xa6<\xbdc\xdc\x80\x03\xeap\xcb\xb5\xd1i4$\xa5\xd3)M\x05\xa1\xac\x05y1{5\xfb\\\xa9\x85\xce\xd4\xcd\xcb>\x0c\xec\x81p\xb6&\x16o\\4\xa6h\x16\xe9\x98JA\xb85\xa4\xa0\xd1{.\xdd\xcee\x8f\xf0Qy\xc7\xf1:\xd0\x11!t\x9e_\xd5R\x03\xe9{\xf6O\xe7\xff\x87\xb8\x1ep\xc9\x1a^\xaf%\x88\x8e\xf2\xabA]\xa0^\x863C\x0c\xe3\x91\xe3\xd2\xd4f6d\xe45\x12\xa9\x0e5\x14|S\xa0N\x97h!$L\xd6\x07\xc3E\xe7\x8c\xe6\xa4-\xe9\x0cur3\x18\xe1\x0f\x90\x143\x97,\x165k-\x14\xcb\xcc!;%\xea\x08_\x08@\x0c\x0f(1\xebY\x15\x83K\xbc\xa7\x18\xa4U\x1c\xb5\xa1\xb9\x90\xf5\xc5\xc32\t\xed\xbc\xf8W\xc7T\xa3\x8a\xc1*\x1bQ\r\x94\x04\xa9\'l\x91\x1d]\x7f\x89\x9c\n\x87\xdb\x13\xd0\xac\xc6;s\x13\xf8\xafg\xab\x1f~6\x1b\x92g\\1B5\xdbc\x7f\x98\x89\x9b\x8a<I\x0c\xfa\x08\xd5\x90_\x1aMF\xb59wyf\xb2\x82\x9e\xa1\xdeK\xc4"\xd3\xf0\xa0ju\xa67\xa7\x11Z\x86\x9b\xb0\xf2\xbe\x0b'
    )
    assert conn.next_event() == Command(cmd="INTERACT_WORD")
    assert conn.next_event() == NeedData(size=16)

    # receive known command
    conn.receive_data(
        b"\x00\x00\x04\xad\x00\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00"
        b'{"cmd":"DANMU_MSG","info":[[0,1,25,16777215,1672600515362,1672599856,0,"12de831c",0,0,0,"",1,{"bulge_display":0,"emoticon_unique":"official_114","height":60,"in_player_area":1,"is_dynamic":1,"url":"http://i0.hdslb.com/bfs/live/40db7427f02a2d9417f8eeed0f71860dfb28df5a.png","width":195},"{}",{"mode":0,"show_player_type":0,"extra":"{\\"send_from_me\\":false,\\"mode\\":0,\\"color\\":16777215,\\"dm_type\\":1,\\"font_size\\":25,\\"player_mode\\":1,\\"show_player_type\\":0,\\"content\\":\\"what\\",\\"user_hash\\":\\"316572444\\",\\"emoticon_unique\\":\\"official_114\\",\\"bulge_display\\":0,\\"recommend_score\\":7,\\"main_state_dm_color\\":\\"\\",\\"objective_state_dm_color\\":\\"\\",\\"direction\\":0,\\"pk_direction\\":0,\\"quartet_direction\\":0,\\"anniversary_crowd\\":0,\\"yeah_space_type\\":\\"\\",\\"yeah_space_url\\":\\"\\",\\"jump_to_url\\":\\"\\",\\"space_type\\":\\"\\",\\"space_url\\":\\"\\",\\"animation\\":{},\\"emots\\":null}"},{"activity_identity":"","activity_source":0,"not_show":0}],"what",[1087319369,"ProgramRipper",1,0,0,10000,1,""],[18,"\xe9\xb2\xb8\xe5\x91\x86","\xe5\xb8\x8c\xe6\x9c\x88\xe8\x90\x8c\xe5\xa5\x88",22889484,13081892,"",0,13081892,13081892,13081892,0,1,591892279],[9,0,9868950,"\\u003e50000",0],["",""],0,0,null,{"ts":1672600515,"ct":"5BDD7605"},0,0,null,null,0,91]}'
    )
    assert conn.next_event() == DanmuMsg(
        "DANMU_MSG",
        DanmuMsgInfo(
            DanmuMsgInfoMeta(
                0,
                1,
                25,
                16777215,
                1672600515362,
                1672599856,
                0,
                "12de831c",
                0,
                0,
                0,
                "",
                DmType.Emoji,
                EmotionOptions(
                    bulge_display=0,
                    emoticon_unique="official_114",
                    height=60,
                    in_player_area=1,
                    is_dynamic=1,
                    url="http://i0.hdslb.com/bfs/live/40db7427f02a2d9417f8eeed0f71860dfb28df5a.png",
                    width=195,
                ),
                "{}",
                ModeInfo(
                    0,
                    0,
                    '{"send_from_me":false,"mode":0,"color":16777215,"dm_type":1,"font_size":25,"player_mode":1,"show_player_type":0,"content":"what","user_hash":"316572444","emoticon_unique":"official_114","bulge_display":0,"recommend_score":7,"main_state_dm_color":"","objective_state_dm_color":"","direction":0,"pk_direction":0,"quartet_direction":0,"anniversary_crowd":0,"yeah_space_type":"","yeah_space_url":"","jump_to_url":"","space_type":"","space_url":"","animation":{},"emots":null}',
                ),
                ActivityInfo(activity_identity="", activity_source=0, not_show=0),
            ),
            "what",
            DanmuMsgInfoSender(
                1087319369,
                "ProgramRipper",
                1,
                0,
                0,
                10000,
                1,
                "",
            ),
            DanmuMsgInfoMedal(
                level=18,
                name="鲸呆",
                uname="希月萌奈",
                room_id=22889484,
                color=13081892,
                text="",
                code=0,
                color_border=13081892,
                color_start=13081892,
                color_end=13081892,
                guard_type=0,
                is_lighted=1,
                uid=591892279,
            ),
            DanmuMsgInfoLevel(
                9,
                0,
                9868950,
                ">50000",
                0,
            ),
            ("", ""),
            0,
            0,
            None,
            DanmuMsgInfoCheckInfo(ts=1672600515, ct="5BDD7605"),
            0,
            0,
            None,
            None,
            0,
            91,
        ),
    )

    # receive unknown protover
    conn.receive_data(
        b"\x00\x00\x00\x10\x00\x10\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00"
    )
    with pytest.raises(RemoteProtocolError, match="Unknown protover: 1"):
        conn.next_event()

    # receive unknown op
    conn = Connection()
    conn.send(Auth(8131361))
    conn.receive_data(
        b"\x00\x00\x00\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    with pytest.raises(RemoteProtocolError, match="Unknown op: 0"):
        conn.next_event()


def test_connection_connected():
    conn = Connection()

    # send heartbeat before auth
    assert conn.state == ConnectionState.CONNECTED
    with pytest.raises(LocalProtocolError, match="Connection is not authenticated"):
        conn.send(Heartbeat(b""))

    # receive heartbeat response before auth
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is not authenticated",
    ):
        conn.receive_data(
            b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00"
            b"\x00\x00\x00\x01"
        )
    assert conn.state == ConnectionState.CLOSED


def test_connection_authenticating():
    conn = Connection()
    conn.send(Auth(8131361))

    # send heartbeat after auth
    assert conn.state == ConnectionState.AUTHENTICATING
    assert (
        conn.send(Heartbeat(b""))
        == b"\x00\x00\x00\x10\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00"
    )

    # send auth again
    with pytest.raises(LocalProtocolError, match="Connection is already authenticated"):
        conn.send(Auth(8131361))

    # receive heartbeat response before auth
    conn.receive_data(
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00"
        b"\x00\x00\x00\x01"
    )
    with pytest.raises(
        RemoteProtocolError,
        match="Connection is not authenticated, but received a HeartbeatResponse",
    ):
        conn.next_event()
    assert conn.state == ConnectionState.CLOSED


def test_connection_authenticated():
    conn = Connection()
    conn.send(Auth(8131361))
    conn.receive_data(
        b"\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00"
        b'{"code":0}'
    )
    conn.next_event()
    assert conn.state == ConnectionState.AUTHENTICATED

    # send auth again
    with pytest.raises(LocalProtocolError, match="Connection is already authenticated"):
        conn.send(Auth(8131361))

    # send unknown event
    with pytest.raises(LocalProtocolError, match="Unknown event: UnknownEvent"):
        conn.send(
            type(
                "UnknownEvent",
                (Event,),
                {"from_bytes": None, "__bytes__": None},
            )()
        )

    # receive heartbeat response
    conn.receive_data(
        b"\x00\x00\x00\x14\x00\x10\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00"
        b"\x00\x00\x00\x01"
    )
    assert conn.next_event() == HeartbeatResponse(1, bytearray(b""))

    conn.receive_data(None)
    assert conn.state == ConnectionState.CLOSED


def test_connection_closed():

    # active close
    conn = Connection()
    assert conn.send(ConnectionClosed()) is None
    assert conn.state == ConnectionState.CLOSED
    conn.send(ConnectionClosed())

    # auth failed
    conn = Connection()
    conn.send(Auth(8131361))
    conn.receive_data(
        b"\x00\x00\x00\x1a\x00\x10\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00"
        b'{"code":1}'
    )
    with pytest.raises(RemoteProtocolError, match=r"Authentication failed \(code: 1\)"):
        conn.next_event()
    assert conn.state == ConnectionState.CLOSED

    conn = Connection()
    conn.receive_data(None)

    assert conn.state == ConnectionState.CLOSED

    # send after close
    with pytest.raises(LocalProtocolError, match="Connection is closed"):
        conn.send(Heartbeat(b""))

    # receive after close
    with pytest.raises(RemoteProtocolError, match="Connection is closed"):
        conn.receive_data(b"any data")

    # receive empty data again
        conn.receive_data(b"")
    conn.receive_data(None)
