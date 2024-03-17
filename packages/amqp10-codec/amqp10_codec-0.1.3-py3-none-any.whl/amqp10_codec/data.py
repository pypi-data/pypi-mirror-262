from amqp10_codec import amqp_read_wire_formatting, amqp_write_wire_formatting
from amqp10_codec.described_format_code import DescribedFormatCode
from amqp10_codec.format_code_consts import FormatCode


class Data:
    def __init__(self, data):
        self.data = data

    @property
    def contents(self):
        return self.data

    @property
    def size(self):
        return (
            amqp_write_wire_formatting.get_sequence_size(self.data)
            + DescribedFormatCode.SIZE
        )

    def write(self):
        buffer, offset = DescribedFormatCode.write(DescribedFormatCode.ApplicationData)
        length = len(self.data)

        if length <= 255:
            buffer.append(FormatCode.Vbin8)
            buffer.append(length)
            offset += 1 + length
        else:
            buffer.append(FormatCode.Vbin32)
            buffer += bytearray([0] * 4)
            amqp_write_wire_formatting.write_uint32(buffer, length, offset + 1)
            offset += 4 + length

        buffer.extend(self.data)
        return buffer, offset

    @staticmethod
    def parse(buffer, offset):
        body, offset = amqp_read_wire_formatting.read_data(buffer, offset)

        return offset, body
