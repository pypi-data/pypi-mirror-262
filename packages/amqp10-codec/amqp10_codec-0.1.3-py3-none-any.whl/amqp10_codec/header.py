from amqp10_codec import amqp_read_wire_formatting


class Header:
    def __init__(
        self,
    ):
        self.durable = False
        self.priority = 0
        self.ttl = 0
        self.first_acquirer = False
        self.delivery_count = 0

    @staticmethod
    def parse(buffer, offset):
        offset, fields = amqp_read_wire_formatting.read_composite_header(buffer, offset)
        h = Header()
        for index in range(fields):
            byte_read, value = amqp_read_wire_formatting.try_read_null(buffer[offset])
            offset += byte_read
            if not value:
                if index == 0:
                    h.durable, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 1:
                    h.priority, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 2:
                    h.ttl, offset = amqp_read_wire_formatting.read_any(buffer, offset)
                    continue
                elif index == 3:
                    h.first_acquirer, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                elif index == 4:
                    h.delivery_count, offset = amqp_read_wire_formatting.read_any(
                        buffer, offset
                    )
                    continue
                else:
                    raise ValueError("Properties Parse invalid index {index}")

        return offset, h
