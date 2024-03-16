from datetime import datetime

from amqp10_codec import amqp_read_wire_formatting


class Properties:
    def __init__(
        self,
    ):
        self.message_id: object = None
        self.user_id: bytes = None
        self.to: str = None
        self.subject: str = None
        self.reply_to: str = None
        self.correlation_id: object = None
        self.content_type: str = None
        self.content_encoding: str = None
        self.absolute_expiry_time: datetime = None
        self.creation_time: datetime = None
        self.group_id: str = None
        self.group_sequence: int = 0
        self.reply_to_group_id: str = None

    @staticmethod
    def parse(buffer, offset):
        offset, fields = amqp_read_wire_formatting.read_composite_header(buffer, offset)
        p = Properties()
        for index in range(fields):
            byte_read, value = amqp_read_wire_formatting.try_read_null(buffer[offset])
            offset += byte_read
            if not value:
                if index == 0:
                    p.message_id, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 1:
                    p.user_id, offset = amqp_read_wire_formatting.read_data(
                        buffer, offset
                    )
                    continue
                elif index == 2:
                    p.to, offset = amqp_read_wire_formatting.read_any(buffer, offset)
                    continue
                elif index == 3:
                    p.subject, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 4:
                    p.reply_to, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 5:
                    p.correlation_id, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 6:
                    p.content_type, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 7:
                    p.content_encoding, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 8:
                    (
                        p.absolute_expiry_time,
                        offset,
                    ) = amqp_read_wire_formatting.read_timestamp(buffer, offset)
                    continue
                elif index == 9:
                    p.creation_time, offset = amqp_read_wire_formatting.read_timestamp(
                        buffer, offset
                    )
                    continue
                elif index == 10:
                    p.group_id, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 11:
                    p.group_sequence, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 12:
                    p.reply_to_group_id, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                else:
                    raise ValueError("Properties Parse invalid index {index}")

        return offset, p
