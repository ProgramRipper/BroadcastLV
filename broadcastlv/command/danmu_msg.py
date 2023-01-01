from enum import IntEnum
from typing import Literal

import msgspec

from ..event import Command


# region DanmuMsgInfo
# region DanmuMsgInfoMeta
class DmType(IntEnum):
    Text = 0
    Emoji = 1
    Voice = 2


class EmotionOptions(msgspec.Struct):  # TODO: Complete comments
    bulge_display: int
    emoticon_unique: str
    """表情唯一标识"""
    height: int
    """表情高度"""
    in_player_area: int
    is_dynamic: Literal[0, 1]
    """是否为动态表情"""
    url: str
    """表情 URL"""
    width: int
    """表情宽度"""


class VoiceConfig(msgspec.Struct):
    ...  # TODO: Complete fields and comments


# region ModeInfo
class ModeInfoExtra(msgspec.Struct):  # TODO: Complete comments
    send_from_me: bool
    """是否为自己发送的弹幕，恒为 False"""
    mode: int
    """同 DanmuMsg.info.meta.mode_info.mode"""
    color: int
    """弹幕颜色，同 DanmuMsg.info.meta.color"""
    dm_type: DmType
    """弹幕类型，同 DanmuMsg.info.meta.dm_type"""
    font_size: int
    """字体大小，同 DanmuMsg.info.meta.size"""
    player_mode: int
    show_player_type: int
    """同 DanmuMsg.info.meta.mode_info.show_player_type"""
    content: str
    """弹幕内容，同 DanmuMsg.info.text"""
    user_hash: str
    emoticon_unique: str
    """表情唯一标识，同 DanmuMsg.info.meta.emotion_options.emoticon_unique"""
    bulge_display: int
    """同 DanmuMsg.info.meta.emotion_options.bulge_display"""
    recommend_score: int
    main_state_dm_color: str
    objective_state_dm_color: str
    direction: int
    pk_direction: int
    quartet_direction: int
    anniversary_crowd: int
    yeah_space_type: str
    yeah_space_url: str
    jump_to_url: str
    space_type: str
    space_url: str
    animation: dict[str, str]
    emots: None


class ModeInfo(
    msgspec.Struct, rename={"_ModeInfo__extra": "extra"}
):  # TODO: Complete comments
    mode: int
    show_player_type: int
    __extra: ModeInfoExtra | str

    @property
    def extra(self) -> ModeInfoExtra:
        """弹幕额外信息，与发送弹幕时返回的 extra 字段相同"""
        if isinstance(self.__extra, str):
            self.__extra = msgspec.json.decode(self.__extra.encode(), type=ModeInfoExtra)
        return self.__extra


# endregion
class ActivityInfo(msgspec.Struct):  # TODO: Complete comments
    activity_identity: str
    activity_source: int
    not_show: int


class DanmuMsgInfoMeta(
    msgspec.Struct, array_like=True
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
    rnd: int
    """同发送弹幕的参数 rnd，网页端发送的弹幕此字段为进入直播间的时间，单位：秒"""
    __6: int
    __7: str
    __8: int
    type: int
    __9: int
    __10: str
    dm_type: DmType
    """弹幕类型"""
    emotion_options: EmotionOptions | Literal["{}"]
    """表情选项，仅当 dm_type 为 DmType.Emoji 时有效"""
    voice_config: VoiceConfig | Literal["{}"]
    """语音配置，仅当 dm_type 为 DmType.Voice 时有效"""
    mode_info: ModeInfo
    """弹幕模式信息"""
    activity_info: ActivityInfo
    """活动信息"""


# endregion
class DanmuMsgInfoSender(
    msgspec.Struct, array_like=True
):  # TODO: Complete fields and comments
    uid: int
    """发送者 uid"""
    uname: str
    """发送者用户名"""
    __2: int
    __3: int
    __4: int
    rank: int
    """是否是正式用户，< 1e4 时不是"""
    verify: Literal[0, 1]
    """是否绑定手机"""
    __7: str


class DanmuMsgInfoMedal(
    msgspec.Struct, array_like=True
):  # TODO: Complete fields and comments
    level: int = 0
    """勋章等级"""
    name: str = ""
    """勋章名称"""
    uname: str = ""
    """勋章拥有者用户名"""
    room_id: int = 0
    """勋章拥有者房间号"""
    color: int = 0
    """勋章颜色"""
    text: str = ""  # NOTE: Guess
    code: int = 0  # NOTE: Guess
    color_border: int = 0
    """勋章边框色"""
    color_start: int = 0
    """勋章渐变色起始色"""
    color_end: int = 0
    """勋章渐变色结束色"""
    guard_type: int = 0
    """1: 总督，2: 提督，3: 舰长"""
    is_lighted: Literal[0, 1] = 0
    """是否点亮勋章"""
    uid: int = 0
    """勋章拥有者 uid"""


class DanmuMsgInfoLevel(
    msgspec.Struct, array_like=True
):  # TODO: Complete fields and comments
    level: int
    """用户等级"""
    __1: int
    __2: int
    rank: str | int
    """用户等级排名，> 50000 时为字符串 '>50000'，其余时候为 int"""
    __4: int


class DanmuMsgInfoCheckInfo(msgspec.Struct):  # TODO: Complete comments
    ts: int
    ct: str


class DanmuMsgInfo(
    msgspec.Struct, array_like=True
):  # TODO: Complete fields and comments
    meta: DanmuMsgInfoMeta
    """弹幕元数据"""
    text: str
    """弹幕内容"""
    sender: DanmuMsgInfoSender
    """发送者信息"""
    medal: DanmuMsgInfoMedal
    """勋章信息"""
    level: DanmuMsgInfoLevel
    """等级信息"""
    __5: tuple[str, str]
    __6: int
    __7: int
    __8: None
    check_info: DanmuMsgInfoCheckInfo
    __10: int
    __11: int
    __12: None
    __13: None
    __14: int
    __15: int


# endregion
class DanmuMsg(Command):
    cmd: Literal["DANMU_MSG"]
    info: DanmuMsgInfo
    """弹幕信息"""
