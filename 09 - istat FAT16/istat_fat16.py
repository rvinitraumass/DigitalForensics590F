import struct


def as_unsigned(bs, endian='<'):
    unsigned_format = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    if len(bs) <= 0 or len(ytes) > 8:
        raise ValueError()
    fill = '\x00'
    while len(bs) not in unsigned_format:
        bs = bs + fill
    result = struct.unpack(endian + unsigned_format[len(bs)], bs)[0]
    return result


def decode_fat_time(time_bytes, tenths=0, tz='EDT'):
    v = as_unsigned(time_bytes)
    second = int(int(0x1F & v) * 2 + 10 * tenths)
    minute = (0x7E0 & v) >> 5
    hour = (0xF800 & v) >> 11
    return '{:02}:{:02}:{:02} ({})'.format(hour, minute, second, tz)


def decode_fat_day(date_bytes):
    v = as_unsigned(date_bytes)
    day = 0x1F & v
    month = (0x1E0 & v) >> 5
    year = ((0xFE00 & v) >> 9) + 1980
    return '{}-{:02}-{:02}'.format(year, month, day)


def istat_fat16(f, address, sector_size=512, offset=0):
    pass


if __name__ == '__main__':
    # values below are from the directory entry in adams.dd that corresponds to the
    # creation date/time of the `IMAGES` directory in the root directory, at
    # metadata address 5; it starts at offset 0x5240 from the start of the image
    print(decode_fat_day(bytes.fromhex('E138')), decode_fat_time(bytes.fromhex('C479'), 0))