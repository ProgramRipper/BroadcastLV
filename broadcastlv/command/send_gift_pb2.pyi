from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlindGiftProtobuf(_message.Message):
    __slots__ = ["blind_gift_config_id", "from_", "gift_action", "original_gift_id", "original_gift_name"]
    BLIND_GIFT_CONFIG_ID_FIELD_NUMBER: ClassVar[int]
    FROM__FIELD_NUMBER: ClassVar[int]
    GIFT_ACTION_FIELD_NUMBER: ClassVar[int]
    ORIGINAL_GIFT_ID_FIELD_NUMBER: ClassVar[int]
    ORIGINAL_GIFT_NAME_FIELD_NUMBER: ClassVar[int]
    blind_gift_config_id: int
    from_: int
    gift_action: str
    original_gift_id: int
    original_gift_name: str
    def __init__(self, blind_gift_config_id: Optional[int] = ..., original_gift_id: Optional[int] = ..., original_gift_name: Optional[str] = ..., from_: Optional[int] = ..., gift_action: Optional[str] = ...) -> None: ...

class GiftItemProtobuf(_message.Message):
    __slots__ = ["action", "batch_combo_id", "coin_type", "combo_resources_id", "combo_stay_time", "combo_total_coin", "crit_prob", "demarcation", "discount_price", "effect_block", "face_effect_id", "face_effect_type", "float_sc_resouce_id", "gift_id", "gift_name", "is_join_receiver", "is_naming", "is_special_batch", "magnification", "num", "price", "rcost", "receive_user_info", "show_batch_combo_send", "super_batch_gift_num", "tag_name", "test", "tid", "timestamp", "total_coin"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    BATCH_COMBO_ID_FIELD_NUMBER: ClassVar[int]
    COIN_TYPE_FIELD_NUMBER: ClassVar[int]
    COMBO_RESOURCES_ID_FIELD_NUMBER: ClassVar[int]
    COMBO_STAY_TIME_FIELD_NUMBER: ClassVar[int]
    COMBO_TOTAL_COIN_FIELD_NUMBER: ClassVar[int]
    CRIT_PROB_FIELD_NUMBER: ClassVar[int]
    DEMARCATION_FIELD_NUMBER: ClassVar[int]
    DISCOUNT_PRICE_FIELD_NUMBER: ClassVar[int]
    EFFECT_BLOCK_FIELD_NUMBER: ClassVar[int]
    FACE_EFFECT_ID_FIELD_NUMBER: ClassVar[int]
    FACE_EFFECT_TYPE_FIELD_NUMBER: ClassVar[int]
    FLOAT_SC_RESOUCE_ID_FIELD_NUMBER: ClassVar[int]
    GIFT_ID_FIELD_NUMBER: ClassVar[int]
    GIFT_NAME_FIELD_NUMBER: ClassVar[int]
    IS_JOIN_RECEIVER_FIELD_NUMBER: ClassVar[int]
    IS_NAMING_FIELD_NUMBER: ClassVar[int]
    IS_SPECIAL_BATCH_FIELD_NUMBER: ClassVar[int]
    MAGNIFICATION_FIELD_NUMBER: ClassVar[int]
    NUM_FIELD_NUMBER: ClassVar[int]
    PRICE_FIELD_NUMBER: ClassVar[int]
    RCOST_FIELD_NUMBER: ClassVar[int]
    RECEIVE_USER_INFO_FIELD_NUMBER: ClassVar[int]
    SHOW_BATCH_COMBO_SEND_FIELD_NUMBER: ClassVar[int]
    SUPER_BATCH_GIFT_NUM_FIELD_NUMBER: ClassVar[int]
    TAG_NAME_FIELD_NUMBER: ClassVar[int]
    TEST_FIELD_NUMBER: ClassVar[int]
    TID_FIELD_NUMBER: ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: ClassVar[int]
    TOTAL_COIN_FIELD_NUMBER: ClassVar[int]
    action: str
    batch_combo_id: str
    coin_type: str
    combo_resources_id: int
    combo_stay_time: int
    combo_total_coin: int
    crit_prob: int
    demarcation: int
    discount_price: int
    effect_block: int
    face_effect_id: int
    face_effect_type: int
    float_sc_resouce_id: int
    gift_id: int
    gift_name: str
    is_join_receiver: bool
    is_naming: bool
    is_special_batch: int
    magnification: float
    num: int
    price: int
    rcost: int
    receive_user_info: ReceiveUserInfoProtobuf
    show_batch_combo_send: bool
    super_batch_gift_num: int
    tag_name: str
    test: int
    tid: str
    timestamp: int
    total_coin: int
    def __init__(self, gift_id: Optional[int] = ..., gift_name: Optional[str] = ..., num: Optional[int] = ..., demarcation: Optional[int] = ..., price: Optional[int] = ..., discount_price: Optional[int] = ..., total_coin: Optional[int] = ..., coin_type: Optional[str] = ..., tid: Optional[str] = ..., timestamp: Optional[int] = ..., super_batch_gift_num: Optional[int] = ..., batch_combo_id: Optional[str] = ..., combo_resources_id: Optional[int] = ..., combo_total_coin: Optional[int] = ..., combo_stay_time: Optional[int] = ..., magnification: Optional[float] = ..., show_batch_combo_send: bool = ..., action: Optional[str] = ..., effect_block: Optional[int] = ..., is_special_batch: Optional[int] = ..., float_sc_resouce_id: Optional[int] = ..., tag_name: Optional[str] = ..., crit_prob: Optional[int] = ..., rcost: Optional[int] = ..., test: Optional[int] = ..., face_effect_type: Optional[int] = ..., face_effect_id: Optional[int] = ..., is_naming: bool = ..., receive_user_info: Optional[Union[ReceiveUserInfoProtobuf, Mapping]] = ..., is_join_receiver: bool = ...) -> None: ...

class MedalInfoProtobuf(_message.Message):
    __slots__ = ["anchor_roomid", "anchor_uname", "guard_level", "is_lighted", "medal_color", "medal_color_border", "medal_color_end", "medal_color_start", "medal_level", "medal_name", "special", "target_id"]
    ANCHOR_ROOMID_FIELD_NUMBER: ClassVar[int]
    ANCHOR_UNAME_FIELD_NUMBER: ClassVar[int]
    GUARD_LEVEL_FIELD_NUMBER: ClassVar[int]
    IS_LIGHTED_FIELD_NUMBER: ClassVar[int]
    MEDAL_COLOR_BORDER_FIELD_NUMBER: ClassVar[int]
    MEDAL_COLOR_END_FIELD_NUMBER: ClassVar[int]
    MEDAL_COLOR_FIELD_NUMBER: ClassVar[int]
    MEDAL_COLOR_START_FIELD_NUMBER: ClassVar[int]
    MEDAL_LEVEL_FIELD_NUMBER: ClassVar[int]
    MEDAL_NAME_FIELD_NUMBER: ClassVar[int]
    SPECIAL_FIELD_NUMBER: ClassVar[int]
    TARGET_ID_FIELD_NUMBER: ClassVar[int]
    anchor_roomid: int
    anchor_uname: str
    guard_level: int
    is_lighted: int
    medal_color: int
    medal_color_border: int
    medal_color_end: int
    medal_color_start: int
    medal_level: int
    medal_name: str
    special: str
    target_id: int
    def __init__(self, target_id: Optional[int] = ..., special: Optional[str] = ..., anchor_uname: Optional[str] = ..., anchor_roomid: Optional[int] = ..., medal_level: Optional[int] = ..., medal_name: Optional[str] = ..., medal_color: Optional[int] = ..., medal_color_start: Optional[int] = ..., medal_color_end: Optional[int] = ..., medal_color_border: Optional[int] = ..., is_lighted: Optional[int] = ..., guard_level: Optional[int] = ...) -> None: ...

class ReceiveUserInfoProtobuf(_message.Message):
    __slots__ = ["uid", "uname"]
    UID_FIELD_NUMBER: ClassVar[int]
    UNAME_FIELD_NUMBER: ClassVar[int]
    uid: int
    uname: str
    def __init__(self, uname: Optional[str] = ..., uid: Optional[int] = ...) -> None: ...

class SendGiftBroadcastProtobuf(_message.Message):
    __slots__ = ["blind_gift", "face", "gift_list", "guard_level", "medal_info", "name_color", "send_master", "svga_block", "switch", "uid", "uname"]
    BLIND_GIFT_FIELD_NUMBER: ClassVar[int]
    FACE_FIELD_NUMBER: ClassVar[int]
    GIFT_LIST_FIELD_NUMBER: ClassVar[int]
    GUARD_LEVEL_FIELD_NUMBER: ClassVar[int]
    MEDAL_INFO_FIELD_NUMBER: ClassVar[int]
    NAME_COLOR_FIELD_NUMBER: ClassVar[int]
    SEND_MASTER_FIELD_NUMBER: ClassVar[int]
    SVGA_BLOCK_FIELD_NUMBER: ClassVar[int]
    SWITCH_FIELD_NUMBER: ClassVar[int]
    UID_FIELD_NUMBER: ClassVar[int]
    UNAME_FIELD_NUMBER: ClassVar[int]
    blind_gift: BlindGiftProtobuf
    face: str
    gift_list: _containers.RepeatedCompositeFieldContainer[GiftItemProtobuf]
    guard_level: int
    medal_info: MedalInfoProtobuf
    name_color: str
    send_master: SendMasterProtobuf
    svga_block: int
    switch: bool
    uid: int
    uname: str
    def __init__(self, uid: Optional[int] = ..., uname: Optional[str] = ..., face: Optional[str] = ..., name_color: Optional[str] = ..., guard_level: Optional[int] = ..., svga_block: Optional[int] = ..., send_master: Optional[Union[SendMasterProtobuf, Mapping]] = ..., medal_info: Optional[Union[MedalInfoProtobuf, Mapping]] = ..., blind_gift: Optional[Union[BlindGiftProtobuf, Mapping]] = ..., gift_list: Optional[Iterable[Union[GiftItemProtobuf, Mapping]]] = ..., switch: bool = ...) -> None: ...

class SendMasterProtobuf(_message.Message):
    __slots__ = ["uid", "uname"]
    UID_FIELD_NUMBER: ClassVar[int]
    UNAME_FIELD_NUMBER: ClassVar[int]
    uid: int
    uname: str
    def __init__(self, uid: Optional[int] = ..., uname: Optional[str] = ...) -> None: ...
