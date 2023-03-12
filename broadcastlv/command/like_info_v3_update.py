from typing import Literal

import msgspec

from ..event import Command
from ..util import add_from_bytes


class Data(msgspec.Struct, kw_only=True, gc=False):
    click_count: int
    """点赞数"""


@add_from_bytes
class LikeInfoV3Update(Command, kw_only=True, gc=False):
    """点赞信息更新"""

    cmd: Literal["LIKE_INFO_V3_UPDATE"] = "LIKE_INFO_V3_UPDATE"
    data: Data
    """点赞数据"""
