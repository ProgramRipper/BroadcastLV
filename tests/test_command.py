from sys import modules

import pytest


def test_lazy_import():
    modules.pop("broadcastlv.event", None)  # reload Command
    modules.pop("broadcastlv.command", None)  # reload COMMAND_MAP
    modules.pop("broadcastlv.command.danmu_msg", None)  # reload DanmuMsg

    import broadcastlv.command
    from broadcastlv.command import COMMAND_MAP, __all__
    from broadcastlv.event import Command

    # initial state
    assert COMMAND_MAP == {cmd: Command for cmd in __all__[1:]}

    from broadcastlv.command import DanmuMsg

    # DanmuMsg is imported
    assert COMMAND_MAP == {cmd: Command for cmd in __all__[1:]} | {
        "DANMU_MSG": DanmuMsg
    }
    assert dir(broadcastlv.command) == broadcastlv.command.__all__

    # unknown symbol
    with pytest.raises(ImportError):
        from broadcastlv.command import UnknownCommand
