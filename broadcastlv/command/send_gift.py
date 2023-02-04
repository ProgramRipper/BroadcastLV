import sys
from collections.abc import MutableSequence
from typing import TYPE_CHECKING, Literal

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

import msgspec

from ..event import Command
from .send_gift_pb2 import BlindGiftProtobuf as BlindGiftProtobuf
from .send_gift_pb2 import GiftItemProtobuf as GiftItemProtobuf
from .send_gift_pb2 import MedalInfoProtobuf as MedalInfoProtobuf
from .send_gift_pb2 import ReceiveUserInfoProtobuf as ReceiveUserInfoProtobuf
from .send_gift_pb2 import SendGiftBroadcastProtobuf as SendGiftBroadcastProtobuf
from .send_gift_pb2 import SendMasterProtobuf as SendMasterProtobuf


class BlindGift(msgspec.Struct, rename={"from_": "from"}, kw_only=True, gc=False):
    blind_gift_config_id: int
    original_gift_id: int
    """盲盒礼物 ID"""
    original_gift_name: str
    """盲盒礼物名称"""
    from_: int
    gift_action: str = "爆出"
    """礼物动作，如 '爆出'"""


class SendMaster(msgspec.Struct, kw_only=True, gc=False):
    uid: int
    uname: str


class BatchComboSend(msgspec.Struct, kw_only=True, gc=False):
    action: str
    """同 SendGift.data.action"""
    batch_combo_id: str
    """同 SendGift.data.batch_combo_id"""
    batch_combo_num: int
    blind_gift: BlindGift | None
    """同 SendGift.data.blind_gift"""
    gift_id: int
    """同 SendGift.data.gift_id"""
    gift_name: str
    """同 SendGift.data.gift_name"""
    gift_num: int
    send_master: SendMaster | None
    """同 SendGift.data.send_master"""
    uid: int
    """同 SendGift.data.uid"""
    uname: str
    """同 SendGift.data.uname"""


class ComboSend(msgspec.Struct, kw_only=True, gc=False):
    action: str
    """同 SendGift.data.action"""
    combo_id: str
    """盲盒时为 uuid，其他时候为 'gift:combo_id:{uid}:{target_id}:{gift_id}:{gift_num}{timestamp:.4f}'"""
    combo_num: int
    gift_id: int
    """同 SendGift.data.gift_id"""
    gift_name: str
    """同 SendGift.data.gift_name"""
    gift_num: int
    send_master: SendMaster | None
    """同 SendGift.data.send_master"""
    uid: int
    """同 SendGift.data.uid"""
    uname: str
    """同 SendGift.data.uname"""


class MedalInfo(msgspec.Struct, kw_only=True, gc=False):
    target_id: int = 0
    """勋章拥有者 uid"""
    special: str
    anchor_uname: str = "--"
    anchor_roomid: int = 0
    medal_level: int = 1
    """勋章等级"""
    medal_name: str = "--"
    """勋章名称"""
    medal_color: int
    """勋章颜色"""
    medal_color_start: int = 0
    """勋章渐变色起始色"""
    medal_color_end: int = 0
    """勋章渐变色结束色"""
    medal_color_border: int = 0
    """勋章边框色"""
    is_lighted: Literal[0, 1] = 0
    """是否点亮勋章"""
    guard_level: Literal[0, 1, 2, 3] = 0
    """同 SendGift.data.guard_level"""
    icon_id: int


class ReceiveUserInfo(msgspec.Struct, kw_only=True, gc=False):
    uid: int
    """接收者 uid"""
    uname: str
    """接收者用户名"""


class SendGiftBroadcastStruct(
    msgspec.Struct,
    rename={
        "beat_id": "beatId",
        "gift_id": "giftId",
        "gift_name": "giftName",
        "gift_type": "giftType",
    },
    kw_only=True,
    gc=False,
):
    # SendGiftBroadcast attributes
    uid: int = 0
    """发送者 uid"""
    uname: str = ""
    """发送者用户名"""
    face: str
    """发送者头像 url"""
    name_color: str = ""
    """发送者用户名颜色，可以为任意 css 颜色值"""
    guard_level: int
    """大航海等级，0: 非舰长，1: 总督，2: 提督，3: 舰长"""
    svga_block: int
    send_master: SendMaster | None = None
    medal_info: MedalInfo
    """勋章信息"""
    blind_gift: BlindGift | None
    """盲盒礼物"""

    @property
    def gift_list(self) -> MutableSequence[Self]:
        return [self]

    switch: bool  # L90026

    # GiftItem attributes
    gift_id: int
    """礼物 ID"""
    gift_name: str
    """礼物名称"""
    num: int = 1
    """礼物数量"""
    demarcation: int
    price: int = 0
    """礼物瓜子数"""
    discount_price: int
    """礼物折扣瓜子数"""
    total_coin: int
    """总瓜子数"""
    coin_type: Literal["gold", "silver"]
    """瓜子类型，gold: 金瓜子，silver: 银瓜子"""
    tid: str  # Guess 与 rnd 一致
    timestamp: int = 0
    """时间戳，单位：秒"""
    super_batch_gift_num: int
    batch_combo_id: str
    """盲盒时为 uuid，其他时候为 'batch:{combo_id}'"""
    combo_resources_id: Literal[0, 1, 2, 3, 5]
    """连击条资源 ID，控制连击条的样式"""
    combo_total_coin: int
    """连击总瓜子数"""
    combo_stay_time: int
    """连击条保留时间"""
    magnification: float

    @property
    def show_batch_combo_send(self) -> bool:
        return self.batch_combo_send is not None

    action: str = "--"
    """礼物动作，如 '投喂'"""
    effect_block: int = 0
    is_special_batch: int
    float_sc_resource_id: int
    tag_image: str
    crit_prob: int
    rcost: int
    face_effect_type: int
    face_effect_id: int
    is_naming: bool
    """是否由 TA 冠名"""
    is_join_receiver: bool
    receive_user_info: ReceiveUserInfo

    # Extra JSON fields
    batch_combo_send: BatchComboSend | None
    beat_id: str
    biz_source: Literal["live", "Live", "xlottery-anchor"]
    """礼物来源，live/Live: 普通礼物，xlottery-anchor: 天选时刻"""
    broadcast_id: int
    combo_send: ComboSend | None
    """连击信息"""
    dmscore: int
    draw: int
    effect: int
    gift_type: int
    gold: int
    is_first: bool
    original_gift_name: str
    remain: int
    rnd: str
    silver: int
    super: int
    super_gift_num: int
    top_list: None


_send_gift_broadcast_struct_decode = msgspec.json.Decoder(
    SendGiftBroadcastStruct
).decode


class Data(msgspec.Struct, kw_only=True, gc=False):
    pb: bytes = b""


_data_decode = msgspec.json.Decoder(Data).decode


class SendGift(Command, kw_only=True, gc=False):
    cmd: Literal["SEND_GIFT"] = "SEND_GIFT"
    data: SendGiftBroadcastStruct | SendGiftBroadcastProtobuf if TYPE_CHECKING else msgspec.Raw

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Self:
        self = super().from_bytes(buffer)
        data: msgspec.Raw = self.data  # type: ignore
        if pb := _data_decode(data).pb:
            self.data = SendGiftBroadcastProtobuf()
            self.data.ParseFromString(pb)
        else:
            self.data = _send_gift_broadcast_struct_decode(data)
        return self

    def into_buffer(self, buffer: bytearray, offset: int = 0) -> None:
        if isinstance(self.data, SendGiftBroadcastProtobuf):
            super(
                SendGift,
                SendGift(
                    data=Data(pb=self.data.SerializeToString()),  # type:ignore
                ),
            ).into_buffer(buffer, offset)
        else:
            super().into_buffer(buffer, offset)

    def __bytes__(self) -> bytes:
        if isinstance(self.data, SendGiftBroadcastProtobuf):
            return super(
                SendGift,
                SendGift(
                    data=Data(pb=self.data.SerializeToString()),  # type: ignore
                ),
            ).__bytes__()
        return super().__bytes__()
