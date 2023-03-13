__all__ = [
    "LocalProtocolError",
    "ProtocolError",
    "RemoteProtocolError",
    "UnknownCommandWarning",
]


class ProtocolError(Exception):
    ...


class LocalProtocolError(ProtocolError):
    ...


class RemoteProtocolError(ProtocolError):
    ...


class UnknownCommandWarning(RuntimeWarning):
    ...
