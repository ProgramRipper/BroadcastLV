from __future__ import annotations

from typing import Literal

import msgspec

from ..event import Command

__all__ = [
    "DanmuMsg",
]


class EmoticonOptions(msgspec.Struct, gc=False):  # TODO: Complete comments
    bulge_display: int = 0
    """是否突出显示"""
    emoticon_unique: str = ""
    """表情唯一标识"""
    height: int = 1
    """表情高度"""
    in_player_area: int = 0
    is_dynamic: Literal[0, 1] = 0
    """是否有表情动画"""
    url: str = ""
    """表情 URL"""
    width: int = 1
    """表情宽度"""


class VoiceInfo(msgspec.Struct, gc=False):  # TODO: Complete fields and comments
    file_id: str
    """语音文件 ID"""
    voice_url: str
    """语音 URL"""
    file_duration: str = '"'
    """语音时长"""


class Emot(msgspec.Struct, gc=False):
    emoticon_id: int
    """表情 ID"""
    emoji: str
    """表情文本版本（展示时使用，为空时回退到 descript，类似 __str__）"""
    descript: str
    """表情文本表达（发送时使用，类似 __repr__）"""
    url: str
    """表情 URL"""
    width: int
    """表情宽度"""
    height: int
    """表情高度"""
    emoticon_unique: str
    """表情唯一标识"""


class Extra(msgspec.Struct, kw_only=True, gc=False):  # TODO: Complete comments
    send_from_me: bool
    """是否为自己发送的弹幕，恒为 False"""
    mode: int
    """同 DanmuMsg.info.meta.mode_info.mode"""
    color: int
    """同 DanmuMsg.info.meta.color"""
    dm_type: Literal[0, 1, 2, 6]
    """同 DanmuMsg.info.meta.dm_type"""
    font_size: int
    """同 DanmuMsg.info.meta.size"""
    player_mode: int
    show_player_type: int
    """同 DanmuMsg.info.meta.mode_info.show_player_type"""
    content: str
    """同 DanmuMsg.info.content"""
    user_hash: str
    emoticon_unique: str
    """同 DanmuMsg.info.meta.emoticon_options.emoticon_unique"""
    bulge_display: int
    """同 DanmuMsg.info.meta.emoticon_options.bulge_display"""
    recommend_score: int
    main_state_dm_color: str
    objective_state_dm_color: str
    direction: int
    pk_direction: int
    quartet_direction: int
    anniversary_crowd: int
    yeah_space_type: str
    yeah_space_url: str = ""
    jump_to_url: str = ""
    space_type: str
    space_url: str = ""
    animation: dict[str, str]
    emots: dict[str, Emot] | None
    """emoji 信息，仅当 dm_type 为 0 时有效，键为 Emot.descript"""


class ModeInfo(
    msgspec.Struct, rename={"_ModeInfo__extra": "extra"}, gc=False
):  # TODO: Complete comments
    mode: int
    show_player_type: int
    __extra: Extra | str

    @property
    def extra(self) -> Extra:
        """弹幕额外信息，与发送弹幕时返回的 extra 字段相同"""
        if isinstance(self.__extra, str):
            self.__extra = msgspec.json.decode(self.__extra.encode(), type=Extra)
        return self.__extra


class ActivityInfo(msgspec.Struct, gc=False):  # TODO: Complete comments
    activity_identity: str
    activity_source: int
    not_show: int
    """0: 展示，1：不展示"""


class Meta(
    msgspec.Struct, kw_only=True, array_like=True, gc=False
):  # TODO: Complete fields and comments
    __0: int
    mode: Literal[1, 4, 5]
    """弹幕位置，1: 滚动，4: 顶部，5: 底部"""
    size: int
    """字体大小"""
    color: int
    """弹幕颜色"""
    time: int
    """发送时间，单位：微秒"""
    rnd: int | str = 0
    """同发送弹幕的参数 rnd，网页端发送的弹幕此字段为进入直播间的时间，单位：秒"""
    __6: int
    __7: str
    __8: int
    type: Literal[0, 1, 2]
    chat_bubble_type: int
    chat_bubble_color: str
    dm_type: Literal[0, 1, 2, 6]
    """弹幕类型，0: 文本（有 emoji），1: 表情，2: 语音，6: 文本 + 表情"""
    emoticon_options: EmoticonOptions | Literal["{}"]
    """表情选项，仅当 dm_type 为 1 时有效"""
    voice_info: VoiceInfo | Literal["{}"]
    """语音信息，仅当 dm_type 为 2 时有效"""
    mode_info: ModeInfo
    """弹幕模式信息"""
    activity_info: ActivityInfo
    """活动信息"""


class Sender(
    msgspec.Struct, kw_only=True, array_like=True, gc=False
):  # TODO: Complete fields and comments
    uid: int = 0
    """发送者 uid"""
    username: str = ""
    """发送者用户名"""
    is_admin: int
    is_vip: int
    is_svip: int
    rank: int
    """是否是正式用户，< 1e4 时不是"""
    verify: Literal[0, 1]
    """是否绑定手机"""
    username_color: str = ""


class Medal(
    msgspec.Struct, kw_only=True, array_like=True, gc=False
):  # TODO: Complete fields and comments
    medal_level: int = 0
    """勋章等级"""
    medal_name: str = "--"
    """勋章名称"""
    anchor_username: str = "--"
    """勋章拥有者用户名"""
    short_room_id: int = 0
    """勋章拥有者房间号"""
    medal_color: int | None = None
    """勋章颜色"""
    special: str = ""
    icon_id: int = 0
    medal_color_border: int
    """勋章边框色"""
    medal_color_start: int
    """勋章渐变色起始色"""
    medal_color_end: int
    """勋章渐变色结束色"""
    guard_level: Literal[0, 1, 2, 3] = 0
    """大航海等级，0: 非舰长，1: 总督，2: 提督，3: 舰长"""
    is_light: Literal[0, 1]
    """是否点亮勋章"""
    anchor_id: int
    """勋章拥有者 uid"""


class Level(
    msgspec.Struct, kw_only=True, array_like=True, gc=False
):  # TODO: Complete fields and comments
    user_level: int = 0
    """用户等级"""
    __1: int
    __2: int
    rank: str | int
    """用户等级排名，> 50000 时为字符串 '>50000'，其他时候为 int"""
    __4: int


class Validation(msgspec.Struct, gc=False):  # TODO: Complete comments
    ts: int = 0
    ct: str = ""


class Info(
    msgspec.Struct, kw_only=True, array_like=True, gc=False
):  # TODO: Complete fields and comments
    meta: Meta
    """弹幕元数据"""
    content: str = ""
    """弹幕内容"""
    sender: Sender
    """发送者信息"""
    medal: Medal
    """勋章信息"""
    level: Level
    """等级信息"""
    title: tuple[str | None, str] = (None, "")
    __6: int
    guard_level: int = 0
    __8: None
    validation: Validation
    __10: int
    __11: int
    __12: None
    __13: None
    lpl: int = 0
    __15: int


class DanmuMsg(Command, omit_defaults=True, kw_only=True, gc=False):
    cmd: Literal["DANMU_MSG"]
    info: Info
    """弹幕信息"""
