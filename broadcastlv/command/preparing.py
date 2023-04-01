from typing import Literal

from ..event import Command
from ..util import add_from_bytes


@add_from_bytes
class Preparing(Command, kw_only=True, gc=False):
    cmd: Literal["PREPARING"] = "PREPARING"
    roomid: str
    """房间号"""
