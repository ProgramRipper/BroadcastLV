__all__ = [
    "LocalProtocolError",
    "ProtocolError",
    "RemoteProtocolError",
]


class ProtocolError(Exception):
    ...


class LocalProtocolError(ProtocolError):
    ...


class RemoteProtocolError(ProtocolError):
    ...
