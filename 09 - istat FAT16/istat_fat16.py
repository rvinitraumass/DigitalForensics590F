import struct


def as_unsigned(bs, endian='<'):
    unsigned_format = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    if len(bs) <= 0 or len(bs) > 8:
        raise ValueError()
    fill = '\x00'
    while len(bs) not in unsigned_format:
        bs = bs + fill
    result = struct.unpack(endian + unsigned_format[len(bs)], bs)[0]
    return result

def get_cluster_to_sector(cluster, cluster_size):
    return ((cluster - 2) * cluster_size)

def decode_fat_time(time_bytes, tenths=0, tz='EDT'):
    v = as_unsigned(time_bytes)
    second = int(int(0x1F & v) * 2)
    if tenths > 100:
        second += 1
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
    result = []
    f.seek(offset * sector_size)
    boot_sector = f.read(sector_size)
    fat_size = as_unsigned(boot_sector[22:24])
    sectors_before_start = as_unsigned(boot_sector[28:32])
    fat_start = sectors_before_start + 1
    number_of_fats = as_unsigned(boot_sector[16:17])
    reserved_area_size = as_unsigned(boot_sector[14:16])
    root_area_start = sectors_before_start - offset + reserved_area_size + number_of_fats * fat_size
    bytes_per_sector = as_unsigned(boot_sector[11:13])
    root_area_end = root_area_start + (as_unsigned(boot_sector[17:19]) * 32 // bytes_per_sector) - 1
    cluster_start = root_area_end + 1
    cluster_size = as_unsigned(boot_sector[13:14])
    f.seek(offset * sector_size + ((root_area_start*sector_size)+(address-3)*32))
    direc_entry = f.read(32)

    result.append('Directory Entry: '+str(address))

    if direc_entry[0] == 0xe5 or direc_entry[0] == 0x00:
        result.append('Not Allocated')
    else:
        result.append('Allocated')

    attr = direc_entry[11]
    file_attr = "File Attributes: "
    if attr & 0x0f == 0x0f:
        file_attr += 'Long File Name'
    else:
        if attr & 0x10:
            file_attr += "Directory"
        elif attr & 0x08:
            file_attr += "Volume Label"
        else:
            file_attr += "File"
        if attr & 0x01:
            file_attr += ", Read Only"
        if attr & 0x02:
            file_attr +=", Hidden"
        if attr & 0x04:
            file_attr += ", System"
        if attr & 0x20:
            file_attr += ", Archive"
    result.append(file_attr)

    file_size = as_unsigned(direc_entry[28:32])
    f.seek(fat_start * sector_size)
    fat = f.read(fat_size * sector_size)
    fat = fat[4:]
    count = 0
    sec_count = file_size // sector_size
    cluster_number = get_cluster_to_sector(as_unsigned(direc_entry[26:28]), cluster_size)
    cluster_offset = as_unsigned(fat[cluster_number:cluster_number + 2])
    cluster_line = []
    cluster_result = []
    flag = False
    while cluster_number < len(fat) and sec_count > 0:
        flag = True
        if len(cluster_line) == 8:
            cluster_result.append(" ".join(cluster_line))
            cluster_line = []
        for c in range(cluster_size):
            cluster_line.append(str(cluster_start + cluster_number + c))
        if cluster_offset < 0xffff and cluster_offset > 0:
            cluster_number = get_cluster_to_sector(cluster_offset, cluster_size)
        elif cluster_offset == 0xffff:
            flag = True
            break
        else:
            cluster_number += 2
        cluster_offset = as_unsigned(fat[cluster_number:cluster_number + 2])
        sec_count -= 2
        count += 2
    if len(cluster_line) == 8:
        cluster_result.append(" ".join(cluster_line))
        cluster_line = []

    if file_size == 0:
        for c in range(cluster_size):
            cluster_line.append(str(cluster_start + cluster_number + c))
            count+=1
    elif not flag or direc_entry[0] == 0xe5:
        rem_size = file_size % (sector_size * cluster_size)
        num_zeroes = rem_size // sector_size + 1
        for c in range(cluster_size - num_zeroes):
            cluster_line.append(str(cluster_start + cluster_number + c))
            count+=1
        for c in range(num_zeroes):
            cluster_line.append("0")
            count+=1
    if file_size == 0:
        result.append('Size: ' + str(count*sector_size))
    else:
        result.append('Size: ' + str(file_size))

    file_ext = "".join(i for i in direc_entry[8:12].decode('ascii') if 48 < ord(i) < 127)
    lowercase_byte = direc_entry[12]
    if direc_entry[0] == 0xe5:
        filename = '_'
    else:
        filename = direc_entry[0:1].decode('ascii').strip()
    filename += direc_entry[1:8].decode('ascii').strip()
    if lowercase_byte & 0x08:
        filename = filename.lower()
    if file_ext:
        if lowercase_byte & 0x10:
            filename += "." + file_ext.lower()
        else:
            filename += "." + file_ext
    result.append('Name: '+filename)

    result.append('')
    result.append('Directory Entry Times:')
    result.append('Written:\t'+ decode_fat_day(direc_entry[24:26]) + " " + decode_fat_time(direc_entry[22:24]))
    result.append('Accessed:\t' + decode_fat_day(direc_entry[18:20]) + " " + decode_fat_time(bytes.fromhex('0000')))
    result.append('Created:\t' + decode_fat_day(direc_entry[16:18]) + " " + decode_fat_time(direc_entry[14:16], direc_entry[13]))
    result.append('')

    result.append('Sectors:')
    for c in cluster_result:
        result.append(c)
    if len(cluster_line) > 0:
        result.append(" ".join(cluster_line))
    return result


if __name__ == '__main__':
    # values below are from the directory entry in adams.dd that corresponds to the
    # creation date/time of the `IMAGES` directory in the root directory, at
    # metadata address 5; it starts at offset 0x5240 from the start of the image
    print(decode_fat_day(bytes.fromhex('E138')), decode_fat_time(bytes.fromhex('0000'), 0))