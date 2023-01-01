from broadcastlv.util import pascal_to_upper_snake


def test_pascal_to_upper_snake():
    mapping = [
        ("DanmuMsg", "DANMU_MSG"),
        ("SysMsg", "SYS_MSG"),
        ("SysGift", "SYS_GIFT"),
        ("GuardMsg", "GUARD_MSG"),
        ("SendGift", "SEND_GIFT"),
        ("Live", "LIVE"),
        ("Preparing", "PREPARING"),
        ("End", "END"),
        ("Close", "CLOSE"),
        ("Block", "BLOCK"),
        ("Round", "ROUND"),
        ("Welcome", "WELCOME"),
        ("Refresh", "REFRESH"),
        ("ActivityRedPacket", "ACTIVITY_RED_PACKET"),
        ("RoomLimit", "ROOM_LIMIT"),
        ("PkPre", "PK_PRE"),
        ("PkEnd", "PK_END"),
        ("PkSettle", "PK_SETTLE"),
        ("PkMicEnd", "PK_MIC_END"),
        ("HotRoomNotify", "HOT_ROOM_NOTIFY"),
        ("PlayTag", "PLAY_TAG"),
        ("PlayProgressBar", "PLAY_PROGRESS_BAR"),
        ("LivePlayerLogRecycle", "LIVE_PLAYER_LOG_RECYCLE"),
    ]

    for pascal, upper_snake in mapping:
        assert pascal_to_upper_snake(pascal) == upper_snake
