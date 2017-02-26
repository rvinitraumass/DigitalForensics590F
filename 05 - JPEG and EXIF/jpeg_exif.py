import tags

class ExifParseError(Exception):
    def init(__self__):
        pass


def carve(f, start, end):
    # return the bytes

    f.seek(start)
    return f.read(end-start+1)


def find_jfif(f, max_length=None):
    seq_list = []
    soi_tags = []
    eoi_tags = []
    byte = f.read(1)
    offset = 0
    while byte:
        if byte == b'\xff':
            byte = f.read(1)
            offset += 1
            if byte == b'\xd8':
                soi_tags.append(offset-1)
            elif byte == b'\xd9':
                eoi_tags.append(offset)
            elif byte == b'\xff':
                continue
        byte = f.read(1)
        offset += 1
    for soi in soi_tags:
        for eoi in eoi_tags:
            if (soi+1 < eoi-1):
                if max_length and eoi - soi + 1 <= max_length:
                    seq_list.append((soi,eoi))
                elif not max_length:
                    seq_list.append((soi, eoi))
    return seq_list


def parse_exif(f):


    return {'Make':'Apple'}