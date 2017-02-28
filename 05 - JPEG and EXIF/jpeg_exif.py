import tags
from struct import *

class ExifParseError(Exception):
    def init(__self__):
        pass


def carve(f, start, end):
    # return the bytes

    f.seek(start)
    return f.read(end-start+1)


def find_jfif(f, max_length=None, parse=False):
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

    if not parse:
        return seq_list
    final_seq_list = []
    for (soi,eoi) in seq_list:
        f.seek(soi+2)
        flag = False
        while True:
            byte = f.read(2)
            if byte[0] == 0xff:
                if byte[1] in [0xc0, 0xc2, 0xc4, 0xdb, 0xdd, 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef, 0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xfe]:
                    byte = f.read(2)
                    data_offset = unpack('>H', byte)[0] - 2
                    f.seek(data_offset, 1)
                elif byte[1] == 0xda and f.tell()+1 < eoi - 1:
                    flag = True
                    break
                else:
                    flag = False
                    break
            else:
                flag = False
                break
        if flag:
            final_seq_list.append((soi,eoi))
    return final_seq_list


def parse_exif(f):
    seq_list = find_jfif(f,parse=True)
    dictionary = {}
    for (soi,eoi) in seq_list:
        f.seek(soi + 2)
        entries = f.read(eoi-soi-1)
        segment_marker = entries[0:2]
        entries = entries[2:]
        while segment_marker:
            data_offset = unpack('>H', entries[0:2])[0]
            if segment_marker == b'\xff\xe1':
                if entries[2:6] == b'Exif':
                    exif_entries = entries[8:]
                    endian = exif_entries[0:2]
                    endianness = '>'
                    if endian == b'\x49\x49':
                        endianness = '<'
                    ifd_offset = unpack(endianness + 'L', exif_entries[4:8])[0]
                    while ifd_offset:
                        ifd_entry = exif_entries[ifd_offset:]
                        num_entries = unpack(endianness+'H', ifd_entry[0:2])[0]
                        tag_offset = 2
                        while num_entries != 0:
                            tag = unpack(endianness+'H', ifd_entry[tag_offset:tag_offset+2])[0]
                            key = tags.TAGS.get(tag)
                            if key:
                                fmt = unpack(endianness+'H', ifd_entry[tag_offset+2:tag_offset+4])[0]
                                num_components = unpack(endianness+'L', ifd_entry[tag_offset+4:tag_offset+8])[0]
                                if fmt == 1:
                                    length = num_components * 1
                                elif fmt == 2:
                                    length = num_components * 1
                                elif fmt == 3:
                                    length = num_components * 2
                                elif fmt == 4:
                                    length = num_components * 4
                                elif fmt == 5:
                                    length = num_components * 8
                                elif fmt == 7:
                                    length = num_components * 1
                                if length > 4:
                                    value_offset = unpack(endianness+'L', ifd_entry[tag_offset+8:tag_offset+12])[0]
                                    data = exif_entries[value_offset:]
                                else:
                                    data = ifd_entry[tag_offset+8:tag_offset+12]
                                if fmt == 1:
                                    dictionary[key] = unpack(endianness+'B', data[0:1])[0]
                                elif fmt == 2:
                                    dictionary[key] = bytes.decode(data[0:length-1])
                                elif fmt == 3:
                                    res_list = list(unpack(endianness+'%dH' % num_components, data[0:length]))
                                    if len(res_list) == 1:
                                        dictionary[key] = res_list[0]
                                    else:
                                        dictionary[key] = res_list
                                elif fmt == 4:
                                    dictionary[key] = unpack(endianness+'L', data[0:4])[0]
                                elif fmt == 5:
                                    (numerator, denominator) = unpack(endianness+'LL', data[0:8])
                                    dictionary[key] = "%s/%s" % (numerator, denominator)
                                elif fmt == 7:
                                    value = unpack(endianness+'% dB' % length, data[0:length])
                                    dictionary[key] = "".join("%.2x" % x for x in value)
                            tag_offset = tag_offset + 12
                            num_entries -= 1
                        ifd_offset = unpack(endianness + 'L', ifd_entry[tag_offset:tag_offset+4])[0]
            elif segment_marker == b'\xff\xda':
                break
            entries=entries[data_offset:]
            segment_marker = entries[0:2]
            entries = entries[2:]

    return dictionary