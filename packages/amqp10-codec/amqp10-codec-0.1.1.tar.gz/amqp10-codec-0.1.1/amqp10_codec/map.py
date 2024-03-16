from amqp10_codec import amqp_read_wire_formatting


class Map:
    @staticmethod
    def parse(buffer, offset):
        items_count, offset = amqp_read_wire_formatting.read_map_header(buffer, offset)

        props = {}
        for _ in range(items_count):
            key, offset = amqp_read_wire_formatting.read_any(buffer, offset)
            value, offset = amqp_read_wire_formatting.read_any(buffer, offset)
            props[key] = value

        return offset, props
