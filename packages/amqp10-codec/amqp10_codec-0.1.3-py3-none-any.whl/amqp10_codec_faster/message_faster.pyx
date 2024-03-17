from datetime import datetime as dt
from datetime import timezone

import cython

from libc.stdint cimport (int8_t, int16_t, int32_t, int64_t, uint8_t, uint16_t,
                          uint32_t, uint64_t)
from libc.stdlib cimport free, malloc
from libc.string cimport memcpy
from libc.time cimport gmtime_r, time, time_t, tm

DEF DESCRIBED_FORMAT_CODE_SIZE = 3


@cython.no_gc_clear
@cython.final
@cython.freelist(1000)
cdef class Message:
    cdef:
        public object body
        public object application_properties
        public object properties
        public object amqp_value
        public object header
        public object annotations

    def __init__(self):
        self.body = None
        self.header = None
        self.application_properties = None
        self.amqp_value = None
        self.properties = None
        self.annotations = None

    cpdef Message unmarshal_c(self, unsigned char[:] buffer):
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
        cdef Message msg = Message()
        cdef Py_ssize_t offset = 0
        cdef Py_ssize_t buffer_length = buffer.shape[0]
        cdef uint8_t described_format_code

        cdef unsigned char *buffer_p = &buffer[0]

        while offset != buffer_length:
            described_format_code = <uint8_t> buffer_p[offset + 2] # don't need 0 and 1

            if described_format_code == 0x75:
                offset += DESCRIBED_FORMAT_CODE_SIZE
                msg.body = read_application_data(buffer_p, &offset)
            elif described_format_code == 0x70:
                msg.header = Header().parse(buffer_p, &offset)
            elif described_format_code == 0x74:
                offset += DESCRIBED_FORMAT_CODE_SIZE
                msg.application_properties = read_map(buffer_p, &offset)
            elif described_format_code == 0x72:
                offset += DESCRIBED_FORMAT_CODE_SIZE
                msg.annotations = read_map(buffer_p, &offset)
            elif described_format_code == 0x73:
                msg.properties = Properties().parse(buffer_p, &offset)
            elif described_format_code == 0x77:
                offset += DESCRIBED_FORMAT_CODE_SIZE
                msg.amqp_value = read_any(buffer_p, &offset)
        return msg

    cpdef unsigned char[:] marshal_c(self):
        cdef unsigned char[:] body = bytearray(self.body)
        cdef unsigned char *mv_body = &body[0]
        #pass buffer from here
        return write_data(mv_body, body.shape[0])


@cython.no_gc_clear
@cython.final
@cython.freelist(1000)
cdef class Header:
    cdef:
        public bint durable
        public uint8_t priority
        public uint32_t ttl
        public bint first_acquirer
        public uint32_t delivery_count

    def __init__(
        self,
    ):
        self.durable = False
        self.priority = 0
        self.ttl = 0
        self.first_acquirer = False
        self.delivery_count = 0

    cdef Header parse(self, unsigned char *buffer, Py_ssize_t *offset):

        cdef uint32_t fields = read_composite_header(buffer, offset)
        cdef Header h = Header()
        cdef uint8_t index
        cdef unsigned char value

        for index in range(0, fields, 1):

            value = buffer[offset[0]]
            if value == 0x40:  # Null
                offset[0] += 1

            else:
                if index == 0:
                    h.durable = read_any(buffer, offset)
                elif index == 1:
                    h.priority = read_any(buffer, offset)
                elif index == 2:
                    h.ttl = read_any(buffer, offset)
                elif index == 3:
                    h.first_acquirer = read_any(buffer, offset)
                elif index == 4:
                    h.delivery_count = read_any(buffer, offset)
                else:
                    raise ValueError("Properties Parse invalid index {index}")
        return h



@cython.no_gc_clear
@cython.final
@cython.freelist(1000)
cdef class Properties:
    cdef:
        public object message_id
        public object user_id
        public object to
        public object subject
        public object reply_to
        public object correlation_id
        public object content_type
        public object content_encoding
        public object absolute_expiry_time
        public object creation_time
        public object group_id
        public object group_sequence
        public object reply_to_group_id

    def __init__(
        self,
    ):
        self.message_id = None
        self.user_id = None
        self.to = None
        self.subject = None
        self.reply_to = None
        self.correlation_id = None
        self.content_type = None
        self.content_encoding = None
        self.absolute_expiry_time = None
        self.creation_time = None
        self.group_id = None
        self.group_sequence = None
        self.reply_to_group_id = None

    
    cdef Properties parse(self, unsigned char *buffer, Py_ssize_t *offset):
        cdef uint32_t fields = read_composite_header(buffer, offset)
        cdef unsigned char value
        p = Properties()
        for index in range(0, fields, 1):
            value = buffer[offset[0]]

            if value == 0x40: # Null
                offset[0] += 1
            else:
                if index == 0:
                    p.message_id = read_any(buffer, offset)
                elif index == 1:
                    p.user_id = read_application_data(buffer, offset)
                elif index == 2:
                    p.to = read_any(buffer, offset)
                elif index == 3:
                    p.subject = read_any(buffer, offset)
                elif index == 4:
                    p.reply_to = read_any(buffer, offset)
                elif index == 5:
                    p.correlation_id = read_any(buffer, offset)
                elif index == 6:
                    p.content_type = read_any(buffer, offset)
                elif index == 7:
                    p.content_encoding = read_any(buffer, offset)
                elif index == 8:
                    p.absolute_expiry_time = read_any(buffer, offset)
                elif index == 9:
                    p.creation_time = read_any(buffer, offset)
                elif index == 10:
                    p.group_id = read_any(buffer, offset)
                elif index == 11:
                    p.group_sequence = read_any(buffer, offset)
                elif index == 12:
                    p.reply_to_group_id = read_any(buffer, offset)
                else:
                    raise ValueError("Properties Parse invalid index {index}")

        return p



cdef bytes read_application_data(unsigned char *buffer, Py_ssize_t *offset):

    cdef unsigned char data_type = buffer[offset[0]]
    cdef uint8_t length_8
    cdef uint32_t length_32
    cdef bytes body

    if data_type == 0xA0: # Vbin8
        offset[0] += sizeof(data_type)
        length_8 = read_uint8(buffer, offset)
        body = buffer[offset[0]: offset[0] + length_8]
        offset[0] += length_8

    elif data_type == 0xB0: # Vbin32
        offset[0] += sizeof(data_type)
        length_32 = read_uint32(buffer, offset)
        body = buffer[offset[0]: offset[0] + length_32]
        offset[0] += length_32
    else:
        raise ValueError("Error in read_data {} not found".format(hex(data_type)))
        
    return body


cdef dict read_map(unsigned char *buffer, Py_ssize_t *offset):
    cdef uint32_t items_count = read_map_header(&buffer[0], offset)

    cdef dict amqpMap = {}
    for _ in range(0, items_count, 1):
        key = read_any(&buffer[0], offset)
        value = read_any(&buffer[0], offset)
        amqpMap[key] = value

    return amqpMap

cdef uint32_t read_composite_header(unsigned char *buffer, Py_ssize_t *offset):
    cdef uint8_t data_type = buffer[offset[0]]
    cdef uint32_t fields

    if data_type != 0:
        raise ValueError(f"Invalid composite header {data_type}")
    offset[0] += sizeof(data_type)
    read_any(buffer, offset)
    fields = read_list_header(buffer, offset)
    return fields

cdef uint32_t read_list_header(unsigned char *buffer, Py_ssize_t *offset):
    cdef unsigned char data_type = buffer[offset[0]]
    cdef uint32_t length

    if data_type == 0x45: #List0
        length = 0
        offset[0] += 1
    elif data_type == 0xC0: #List8
        # move the offset by two to discard unused size value
        offset[0] += 2
        length = read_uint8(buffer, offset)
    elif data_type == 0xD0: # List32
        # move the offset by five to discard unused size value
        offset[0] += 5
        length = read_uint32(buffer, offset)
    else:
        raise ValueError("Invalid list header {}".format(hex(data_type)))
    
    return length


cdef uint32_t read_map_header(unsigned char *buffer, Py_ssize_t *offset):
    cdef unsigned char data_type = buffer[offset[0]]
    cdef uint8_t map_8
    cdef uint32_t map_32
    offset[0] += sizeof(data_type)

    if data_type == 0xC1: # Map8
        # Ignore this byte
        offset[0] += 1
        map_8 = read_uint8(buffer, offset)
        items_count = map_8
    elif data_type == 0xD1: # Map32
        # Ignore this 4 bytes
        offset[0] += 4
        map_32 = read_uint32(buffer, offset)
        items_count = map_32
    
    return items_count // 2

cdef read_any(unsigned char *buffer, Py_ssize_t *offset) except *:
    cdef unsigned char data_type = buffer[offset[0]]
    offset[0] += 1
    cdef uint32_t length

    if data_type == 0xA3: # Sym8
        length = read_uint8(&buffer[0], offset)
        return read_string(&buffer[0], offset, length)

    elif data_type == 0xA1: #Str8
        length = read_uint8(&buffer[0], offset)
        return read_string(&buffer[0], offset, length)

    elif data_type == 0xB3: # Sym32
        length = read_uint32(&buffer[0], offset)
        return read_string(&buffer[0], offset, length)

    elif data_type == 0xB1: # Str32
        length = read_uint32(&buffer[0], offset)
        return read_string(&buffer[0], offset, length)

    elif data_type in (0x44,0x43) : #Ulong0, Uint0
        return 0

    elif data_type in (0x53, 0x52, 0x50): #SmallUlong, SmallUint, Ubyte
        return read_uint8(&buffer[0], offset)

    elif data_type in (0x54, 0x55, 0x51): #Smallint Smalllong Byte
        return read_int8(&buffer[0], offset)

    elif data_type ==  0x81: # Long
        return read_int64(&buffer[0], offset)
    elif data_type == 0x80: # Ulong:
        return read_uint64(&buffer[0], offset)

    elif data_type == 0x71: # Int:
        return read_int32(&buffer[0], offset)
    elif data_type == 0x70:  # Uint
        return read_uint32(&buffer[0], offset)

    elif data_type == 0x61:  # Short:
        return read_short(&buffer[0], offset)
    elif data_type == 0x60: # Ushort
        return read_ushort(&buffer[0], offset)

    elif data_type == 0xA0: #Vbin8
        return read_vbin8(&buffer[0], offset)
    elif data_type == 0xB0: #Vbin32
        return read_vbin32(&buffer[0], offset)

    elif data_type == 0x56: # Bool:
        return read_bool(&buffer[0], offset)
    elif data_type == 0x41: # BoolTrue
        return True
    elif data_type == 0x42: # BoolFalse
        return False

    elif data_type == 0x83: # Timestamp:
        return read_timestamp(&buffer[0], offset)

    elif data_type == 0x72: #float
        return read_float(&buffer[0], offset)
    elif data_type == 0x82: #double
        return read_double(&buffer[0], offset)

    elif data_type == 0x40: # Null:
        return None


#-------------- decode
cdef bytes read_vbin8(unsigned char *buffer, Py_ssize_t *offset):
    cdef bytes binary_data
    cdef uint8_t length
    length = read_uint8(buffer, offset)
    binary_data = buffer[offset[0]: offset[0] + length]
    offset[0] += length

    return binary_data

cdef bytes read_vbin32(unsigned char *buffer, Py_ssize_t *offset):
    cdef bytes binary_data
    length = read_uint32(buffer, offset)
    binary_data = buffer[offset[0]: offset[0] + length]
    offset[0] += length

    return binary_data

cdef uint8_t read_uint8(unsigned char *buffer,  Py_ssize_t *offset) except? -1:
    cdef uint8_t result = buffer[offset[0]]
    offset[0] += sizeof(uint8_t)
    return result

cdef uint16_t read_ushort(unsigned char *buffer,  Py_ssize_t *offset):
    cdef uint16_t result = 0
    cdef uint8_t i
    for i in range(0, 2, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(uint16_t)
    return result

cdef uint32_t read_uint32(unsigned char *buffer,  Py_ssize_t *offset):
    cdef uint32_t result = 0
    cdef uint8_t i
    for i in range(0, 4, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(uint32_t)
    return result

cdef uint64_t read_uint64(unsigned char* buffer, Py_ssize_t *offset):
    cdef uint64_t result = 0
    cdef uint8_t i
    for i in range(0, 8, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(uint64_t)
    return result

cdef int8_t read_int8(unsigned char *buffer,  Py_ssize_t *offset):
    cdef int8_t result = buffer[offset[0]]
    offset[0] += sizeof(int8_t)
    return result

cdef int16_t read_short(unsigned char *buffer,  Py_ssize_t *offset):
    cdef int16_t result = 0
    cdef uint8_t i
    for i in range(0, 2, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(int16_t)
    return result

cdef int32_t read_int32(unsigned char *buffer,  Py_ssize_t *offset):
    cdef int32_t result = 0
    cdef uint8_t i
    for i in range(0, 4, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(int32_t)
    return result

cdef int64_t read_int64(unsigned char* buffer, Py_ssize_t *offset):
    cdef int64_t result = 0
    cdef uint8_t i
    for i in range(0, 8, 1):
        result = (result << 8) | buffer[offset[0] + i]
    offset[0] += sizeof(int64_t)
    return result

cdef float read_float(unsigned char *buffer, Py_ssize_t *offset) except *:
    cdef float result
    cdef uint8_t* p_result = <uint8_t*>&result
    for i in range(0, 4, 1):
        p_result[3 - i] = buffer[offset[0] + i]
    offset[0] += 4
    return result

cdef double read_double(unsigned char* buffer, Py_ssize_t *offset):
    cdef double result
    cdef uint8_t* p_result = <uint8_t*>&result
    for i in range(0, 8, 1):
        p_result[7 - i] = buffer[offset[0] + i]
    offset[0] += 8
    return result

cdef object read_string(unsigned char *buffer, Py_ssize_t *offset, uint32_t length):
    cdef object data_string

    data_string = bytes(buffer[offset[0]:offset[0]+length]).decode("utf-8")
    offset[0] += length
    return data_string

cdef bint read_bool(unsigned char *buffer, Py_ssize_t *offset):
    cdef bint result = <bint> buffer[offset[0]]
    offset[0] += 1
    return result

cdef read_timestamp(unsigned char* buffer, Py_ssize_t* offset):
    cdef int64_t value
    value = read_int64(buffer, offset)
    cdef tm t = datetime_from_unix_milliseconds(value)

    return dt(year=t.tm_year + 1900, month=t.tm_mon + 1, day=t.tm_mday, 
            hour=t.tm_hour, minute=t.tm_min, second=t.tm_sec, tzinfo=timezone.utc)


cdef tm datetime_from_unix_milliseconds(time_t ms):
    cdef time_t t = <time_t> (ms / 1000)
    cdef tm date
    gmtime_r(&t, &date)

    return date


cdef unsigned char[:] write_data(unsigned char *msg_body, Py_ssize_t message_body_length):
    cdef Py_ssize_t buffer_size = calc_buffer_size(message_body_length)
    cdef unsigned char* buffer = <unsigned char *> malloc(buffer_size)
    cdef Py_ssize_t offset = 0

    try:
       write_descriptor(buffer, &offset)

       if message_body_length <= 255:
           write_byte(buffer, &offset, 0xa0)
           write_byte(buffer, &offset, message_body_length)
       else:
           write_byte(buffer, &offset, 0xb0)
           write_uint32(buffer, &offset, message_body_length)

       write_body(buffer, &offset, msg_body, message_body_length)

       return <bytearray>buffer[:offset]

    finally:
       free(buffer)

cdef Py_ssize_t calc_buffer_size(Py_ssize_t message_body_length):
    cdef Py_ssize_t result = DESCRIBED_FORMAT_CODE_SIZE + sizeof(char)

    if message_body_length <= 255:
        result += sizeof(char)
    else:
        result += sizeof(uint32_t)

    result += message_body_length

    return result


cdef void write_descriptor(unsigned char* dest, Py_ssize_t* offset):
    dest[offset[0]] = 0x00
    dest[offset[0] + 1] = 0x53
    dest[offset[0] + 2] = 0x75
    offset[0] += DESCRIBED_FORMAT_CODE_SIZE


cdef void write_byte(unsigned char* dest, Py_ssize_t* offset, unsigned char value):
    dest[offset[0]] = value
    offset[0] += 1

cdef void write_body(unsigned char* dest, Py_ssize_t* offset, unsigned char* body, Py_ssize_t body_len):

    if dest == NULL:
        raise MemoryError("Memory allocation failed")

    memcpy(dest + offset[0], body, body_len)
    offset[0] += body_len

cdef void write_uint32(unsigned char* dest, Py_ssize_t* offset, Py_ssize_t body_len):
    dest[offset[0]] = (body_len >> 24) & 0xFF
    dest[offset[0] + 1] = (body_len >> 16) & 0xFF
    dest[offset[0] + 2] = (body_len >> 8) & 0xFF
    dest[offset[0] + 3] = body_len & 0xFF
    offset[0] += sizeof(uint32_t)
