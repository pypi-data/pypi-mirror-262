from amqp10_codec import amqp_read_wire_formatting
from amqp10_codec.amqp_write_wire_formatting import encode_body_value
from amqp10_codec.annotations import Annotations
from amqp10_codec.application_properties import ApplicationProperties
from amqp10_codec.data import Data
from amqp10_codec.described_format_code import DescribedFormatCode
from amqp10_codec.header import Header
from amqp10_codec.properties import Properties


class Message:
    def __init__(self):
        self.body = None
        self.header = None
        self.application_properties = None
        self.amqp_value = None
        self.properties = None
        self.annotations = None

    @staticmethod
    def unmarshal(buffer):
        #                                                            Bare Message
        #                                                               |
        #                                         .---------------------+--------------------.
        #                                         |                                           |
        #    +--------+-------------+-------------+------------+--------------+--------------+--------
        #    | header | delivery-   | message-    | properties | application- | application- | footer |
        #    |        | annotations | annotations |             | properties  | data         |        |
        #    +--------+-------------+-------------+------------+--------------+--------------+--------+
        #    Altogether a message consists of the following sections:
        #    • Zero or one header.
        #    • Zero or one delivery-annotations.
        #    • Zero or one message-annotations.
        #    • Zero or one properties.
        #    • Zero or one application-properties.
        #    • The body consists of either: one or more data sections, one or more amqp-sequence sections,
        #    or a single amqp-value section.
        #    • Zero or one footer.

        msg = Message()
        offset = 0
        buffer_length = len(buffer)
        while offset != buffer_length:
            data_code = DescribedFormatCode.read(buffer, offset)

            if data_code is DescribedFormatCode.ApplicationData:
                offset += DescribedFormatCode.SIZE
                offset, msg.body = Data.parse(buffer, offset)
            elif data_code is DescribedFormatCode.MessageHeader:
                offset, msg.header = Header.parse(buffer, offset)
            elif data_code is DescribedFormatCode.ApplicationProperties:
                offset += DescribedFormatCode.SIZE
                (
                    offset,
                    msg.application_properties,
                ) = ApplicationProperties.parse(buffer, offset)
            elif data_code is DescribedFormatCode.MessageAnnotations:
                offset += DescribedFormatCode.SIZE
                offset, msg.annotations = Annotations.parse(buffer, offset)
            elif data_code is DescribedFormatCode.MessageProperties:
                offset, msg.properties = Properties.parse(buffer, offset)
            elif data_code is DescribedFormatCode.AmqpValue:
                offset += DescribedFormatCode.SIZE
                value, offset = amqp_read_wire_formatting.read_any(buffer, offset)
                msg.amqp_value = value
        return msg

    @staticmethod
    def marshal(value: str):
        msg = Message()
        encoded_msg = encode_body_value(value)
        msg.body, offset = Data(encoded_msg).write()

        return msg
