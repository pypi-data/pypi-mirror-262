from libc.stdint cimport uint8_t, uint32_t


cdef read_any(unsigned char *buffer, Py_ssize_t *offset) except *
cdef uint32_t read_map_header(unsigned char *buffer, Py_ssize_t *offset)
cdef bytes read_application_data(unsigned char *buffer, Py_ssize_t *offset)
cdef uint32_t read_composite_header(unsigned char *buffer, Py_ssize_t *offset)
cdef uint32_t read_list_header(unsigned char *buffer, Py_ssize_t *offset)
cdef void write_descriptor(unsigned char* buffer, Py_ssize_t* offset)
cdef void write_byte(unsigned char* dest, Py_ssize_t* offset, unsigned char value)
cdef void write_body(unsigned char* dest, Py_ssize_t* offset, unsigned char* values, Py_ssize_t body_len)
cdef void write_uint32(unsigned char* dest, Py_ssize_t* offset, Py_ssize_t body_len)
