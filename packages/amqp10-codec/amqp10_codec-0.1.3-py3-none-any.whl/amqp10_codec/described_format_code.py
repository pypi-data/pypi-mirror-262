from amqp10_codec.format_code_consts import FormatCode


class DescribedFormatCode:
    SIZE = 3

    # AMQP 1.0 Described Format Codes

    ApplicationData = 0x75
    MessageAnnotations = 0x72
    MessageProperties = 0x73
    ApplicationProperties = 0x74
    MessageHeader = 0x70
    AmqpValue = 0x77

    @staticmethod
    def read(buffer: bytes, offset: int) -> int:
        return buffer[offset + 2]

    @staticmethod
    def write(data: int):
        buffer = bytearray()
        buffer.append(FormatCode.Described)
        buffer.append(FormatCode.SmallUlong)
        buffer.append(data)
        offset = 3

        return buffer, offset
