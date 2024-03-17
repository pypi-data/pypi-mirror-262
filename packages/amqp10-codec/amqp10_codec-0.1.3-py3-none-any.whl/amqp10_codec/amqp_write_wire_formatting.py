import struct


def get_sequence_size(data):
    if len(data) <= 255:
        return len(data) + 1
    else:
        return len(data) + 4


def encode_body_value(value: str) -> bytes:
    value_bytes = value.encode()
    length_encode = len(value)
    format_string = f">{length_encode}s"
    return struct.pack(format_string, value_bytes)


def decode_body_value(encoded_value: bytes, length_decode: int) -> str:
    format_string = f">{length_decode}s"
    return struct.unpack(format_string, encoded_value)[0]


def write_uint32(buffer, value, offset):
    struct.pack_into(">I", buffer, offset, value)
    return offset + 4
