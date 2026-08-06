import struct


def read_uint8(f, endianness):
    return struct.unpack(endianness + "B", f.read(1))[0]


def read_ushort(f, endianness):
    return struct.unpack(endianness + "H", f.read(2))[0]
    
    
def read_uint(f, endianness):
    return struct.unpack(endianness + "I", f.read(4))[0]
    

def read_uint64(f, endianness):
    return struct.unpack(endianness + "Q", f.read(8))[0]


def read_float(f, endianness):
    return struct.unpack(endianness + "f", f.read(4))[0]
    

def read_cstring(f, encoding="utf-8"):
    chars = bytearray()

    while True:
        b = f.read(1)
        if b == b"" or b == b"\x00":
            break
        chars.extend(b)

    return chars.decode(encoding)
    


def align(num, f, offset):
    alignment_bytes = (num - (offset % num)) % num
    f.seek(alignment_bytes, 1)


    

    