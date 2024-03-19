class FormatCode:
    Described = 0x00
    Null = 0x40

    # Bool
    Bool = 0x56  # boolean with the octet 0x00 being false and octet 0x01 being true
    BoolTrue = 0x41
    BoolFalse = 0x42

    # Unsigned
    Ubyte = 0x50  # 8-bit unsigned integer (1)
    Ushort = 0x60  # 16-bit unsigned integer in network byte order (2)
    Uint = 0x70  # 32-bit unsigned integer in network byte order (4)
    SmallUint = 0x52  # unsigned integer value in the range 0 to 255 inclusive (1)
    Uint0 = 0x43  # the uint value 0 (0)
    Ulong = 0x80  # 64-bit unsigned integer in network byte order (8)
    SmallUlong = 0x53  # unsigned long value in the range 0 to 255 inclusive (1)
    Ulong0 = 0x44  # the ulong value 0 (0)

    # Signed
    Byte = 0x51  # 8-bit two's-complement integer (1)
    Short = 0x61  # 16-bit two's-complement integer in network byte order (2)
    Int = 0x71  # 32-bit two's-complement integer in network byte order (4)
    Smallint = 0x54  # 8-bit two's-complement integer (1)
    Long = 0x81  # 64-bit two's-complement integer in network byte order (8)
    Smalllong = 0x55  # 8-bit two's-complement integer

    # Decimal
    Float = 0x72  # IEEE 754-2008 binary32 (4)
    Double = 0x82  # IEEE 754-2008 binary64 (8)

    Decimal32 = (
        0x74  # IEEE 754-2008 decimal32 using the Binary Integer Decimal encoding (4)
    )
    Decimal64 = (
        0x84  # IEEE 754-2008 decimal64 using the Binary Integer Decimal encoding (8)
    )
    Decimal128 = (
        0x94  # IEEE 754-2008 decimal128 using the Binary Integer Decimal encoding (16)
    )

    Vbin8 = 0xA0  # up to 2^8 - 1 octets of binary data (1 + variable)
    Vbin32 = 0xB0  # up to 2^32 - 1 octets of binary data (4 + variable)

    Str8 = 0xA1  # up to 2^8 - 1 octets worth of UTF-8 Unicode (with no byte order mark) (1 + variable)
    Str32 = 0xB1  # up to 2^32 - 1 octets worth of UTF-8 Unicode (with no byte order mark) (4 +variable)

    Sym8 = 0xA3  # up to 2^8 - 1 seven bit ASCII characters representing a symbolic value (1 + variable)
    Sym32 = 0xB3  # up to 2^32 - 1 seven bit ASCII characters representing a symbolic value (4 + variable)

    # Compound
    List0 = 0x45  # the empty list (i.e. the list with no elements) (0)
    List8 = 0xC0  # up to 2^8 - 1 list elements with total size less than 2^8 octets (1 + compound)
    List32 = 0xD0  # up to 2^32 - 1 list elements with total size less than 2^32 octets (4 + compound)

    Map8 = 0xC1  # up to 2^8 - 1 octets of encoded map data (1 + compound)
    Map32 = 0xD1  # up to 2^32 - 1 octets of encoded map data (4 + compound)

    Array8 = 0xE0  # up to 2^8 - 1 array elements with total size less than 2^8 octets (1 + array)
    Array32 = 0xF0  # up to 2^32 - 1 array elements with total size less than 2^32 octets (4 + array)

    Char = 0x73  # a UTF-32BE encoded Unicode character (4)

    Timestamp = 0x83  # 64-bit two's-complement integer representing milliseconds since the unix epoch
    UUID = 0x98  # UUID as defined in section 4.1.2 of RFC-4122
