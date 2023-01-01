from broadcastlv.header import Header, HeaderStruct


def test_header_struct():
    assert HeaderStruct.format == ">I2H2I"
    assert HeaderStruct.size == 16
    assert (
        HeaderStruct.pack(1, 2, 3, 4, 5)
        == b"\x00\x00\x00\x01\x00\x02\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05"
    )
    assert HeaderStruct.unpack(
        b"\x00\x00\x00\x01\x00\x02\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05"
    ) == (1, 2, 3, 4, 5)


def test_header_init():
    header = Header(1, 2, 3, 5, 6)

    assert header.size == 1
    assert header.header_size == 2
    assert header.protover == 3
    assert header.op == 5
    assert header.seq == 6


def test_header_from_bytes():
    assert Header.from_bytes(
        b"\x00\x00\x00\x01\x00\x02\x00\x03\x00\x00\x00\x05\x00\x00\x00\x06"
    ) == Header(1, 2, 3, 5, 6)


def test_header_bytes():
    assert (
        bytes(Header(1, 2, 3, 5, 6))
        == b"\x00\x00\x00\x01\x00\x02\x00\x03\x00\x00\x00\x05\x00\x00\x00\x06"
    )
