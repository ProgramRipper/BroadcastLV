from importlib import reload
from sys import modules

import pytest


def test_lazy_import():
    del modules["broadcastlv.event"]  # reload Command
    del modules["broadcastlv.command"]  # reload COMMAND_MAP
    del modules["broadcastlv.command.danmu_msg"]  # reload DanmuMsg

    import broadcastlv.command
    from broadcastlv.command import COMMAND_MAP

    # initial state
    assert COMMAND_MAP == {}

    from broadcastlv.command import DanmuMsg

    # DanmuMsg is imported
    assert COMMAND_MAP == {"DANMU_MSG": DanmuMsg}
    assert dir(broadcastlv.command) == ["COMMAND_MAP", "DanmuMsg"]

    # unknown symbol
    with pytest.raises(ImportError):
        from broadcastlv.command import UnknownCommand
