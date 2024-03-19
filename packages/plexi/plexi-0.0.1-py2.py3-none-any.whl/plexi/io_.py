import io

import struct


def round_up(n):
    "Rounds an integer up to the nearest multiple of four"
    div, mod = divmod(n, 4)
    if mod:
        return (div+1) * 4
    else:
        return n
    
def load_from_stream(cls, stream : io.IOBase):
    values = struct.unpack(r"<2sI4xI", stream.read(14))
    keys = ["type_code", "file_size", "data_offset"]
    header = dict(zip(keys, values))

    values = struct.unpack(r"<IIIHHIIIIII", stream.read(40))
    keys = [
        "header_size",
        "width",
        "height",
        "planes",
        "bits_per_pixel",
        "compression",
        "image_size",
        "hrex",
        "vres",
        "colors_used",
        "important_colors",
    ]
    info_header = dict(zip(keys, values))

    height, width = info_header["height"], info_header["width"]
    bmp = cls(width, height)
    scan_line_width = round_up(width*3)

    for y in range(height):
        scan_line = stream.read(scan_line_width)
        for x in range(width):
            bgr = scan_line[x*3:x*3+3]
            b, g, r = struct.unpack("BBB", bgr)
            bmp[x, y] = (r, g, b)
    
    return bmp


def save_to_stream(bmp, stream : io.IOBase):
    scan_line_width = round_up(bmp.width*3)
    padding_size = scan_line_width - bmp.width*3
    header_size = 14
    info_header_size = 40
    image_size =  scan_line_width * bmp.height
    data_offset = header_size + info_header_size
    file_size = data_offset + image_size

    stream.write(struct.pack(r"<2sI4xI", b'BM', file_size, data_offset))

    stream.write(struct.pack(r"<IIIHHIIIIII", 40, bmp.width, bmp.height, 1, 24, 0, image_size, 3779, 3779, 0, 0))
    for y in range(bmp.height):
        for x in range(bmp.width):
            r, g, b = bmp[x, y]
            stream.write(struct.pack("BBB", b, g, r))
        stream.write(b'\00' * padding_size)
