from ..event import Command
from ..util import add_from_bytes


@add_from_bytes
class Live(Command, kw_only=True, gc=False):
    cmd: str
    live_key: str
    voice_background: str
    sub_session_key: str
    live_platform: str
    "pc_link, pc"
    live_model: int
    live_time: int | None = None
    """开播时间"""
    roomid: int
    """房间号"""
