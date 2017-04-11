import datetime
import struct


def as_signed_le(bs):
    signed_format = {1: 'b', 2: 'h', 4: 'l', 8: 'q'}
    if len(bs) <= 0 or len(bs) > 8:
        raise ValueError()

    fill = b'\x00'
    if ((bs[-1] & 0x80) >> 7) == 1:
        fill = b'\xFF'

    while len(bs) not in signed_format:
        bs = bs + fill
    result = struct.unpack('<' + signed_format[len(bs)], bs)[0]
    return result


def get_flags(flags):
    flag_num = 0
    flags_string = "Flags: "
    if flags & 0x0001:
        flag = "Read Only"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0002:
        flag = "Hidden"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0004:
        flag = "System"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0020:
        flag = "Archive"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0040:
        flag = "Device"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0080:
        flag = "Normal"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0100:
        flag = "Temporary"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0200:
        flag = "Sparse"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0400:
        flag = "Reparse Point"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x0800:
        flag = "Compressed"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x1000:
        flag = "Offline"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x2000:
        flag = "Not Content Indexed"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    if flags & 0x4000:
        flag = "Encrypted"
        if flag_num != 0:
            flag = ", " + flag
        flags_string += flag
    return flags_string


def istat_ntfs(f, address, sector_size=512, offset=0):
    results = []
    f.seek(offset*sector_size)
    boot_sector = f.read(sector_size)
    sectors_per_cluster = as_signed_le(boot_sector[13:14])
    sector_size = as_signed_le(boot_sector[11:13])
    cluster_size = sectors_per_cluster * sector_size
    mft_start_cluster = as_signed_le(boot_sector[48:56])
    mft_size_value = as_signed_le(boot_sector[64:65])
    if mft_size_value < 0:
        mft_size = pow(2,abs(mft_size_value))
    else:
        mft_size = mft_size_value * cluster_size
    f.seek(mft_start_cluster*cluster_size+address*mft_size)

    mft = f.read(mft_size)
    sequence = as_signed_le(mft[16:18])
    log_file_sequence_num = as_signed_le(mft[8:16])
    allocated_status = as_signed_le(mft[22:24])
    allocated = "Allocated File"
    if not allocated_status & 0x01:
        allocated = "Not " + allocated
    links = as_signed_le(mft[18:20])
    results.append('MFT Entry Header Values:')
    results.append('Entry: ' + str(address) +'        Sequence: '+str(sequence))
    results.append('$LogFile Sequence Number: ' + str(log_file_sequence_num))
    results.append(allocated)
    results.append('Links: '+ str(links))
    results.append('')
    attr_offset = as_signed_le(mft[20:22])
    attr_list = ['Attributes:']

    while as_signed_le(mft[attr_offset:attr_offset+8]) != 0xffffffff:
        attr_length = as_signed_le(mft[attr_offset+4:attr_offset+8])
        attr_type = as_signed_le(mft[attr_offset:attr_offset+4])
        attr_id = as_signed_le(mft[attr_offset+14:attr_offset+16])
        attr_non_resident = as_signed_le(mft[attr_offset+8:attr_offset+9])
        attr_resident = 'Resident'
        if attr_non_resident == 1:
            attr_resident = 'Non-'+attr_resident
        attr_name_length = as_signed_le(mft[attr_offset+9:attr_offset+10])
        attr_name_offset = None
        attr_name = 'N/A'
        if attr_name_length != 0:
            attr_name_offset = as_signed_le(mft[attr_offset+10:attr_offset+12])

        if attr_type == 16:
            content_size = as_signed_le(mft[attr_offset + 16: attr_offset + 20])
            content_offset = as_signed_le(mft[attr_offset+20: attr_offset+22])
            stand_info = mft[attr_offset+content_offset:attr_offset+content_offset+content_size]
            results.append('$STANDARD_INFORMATION Attribute Values:')
            flags = as_signed_le(stand_info[32:36])
            results.append(get_flags(flags))
            if content_size <= 48:
                owner_id = '0'
            else:
                owner_id = str(as_signed_le(stand_info[48:52]))
            results.append('Owner ID: ' + owner_id)
            results.append('Created:\t' + into_localtime_string(as_signed_le(stand_info[0:8])))
            results.append('File Modified:\t' + into_localtime_string(as_signed_le(stand_info[8:16])))
            results.append('MFT Modified:\t' + into_localtime_string(as_signed_le(stand_info[16:24])))
            results.append('Accessed:\t' + into_localtime_string(as_signed_le(stand_info[24:32])))
            results.append('')
            if attr_name_offset:
                attr_name = mft[attr_name_offset:attr_name_offset+attr_name_length].decode('utf-16')
            attr_list.append('Type: $STANDARD_INFORMATION (16-' + str(
                attr_id) + ')   Name: ' + attr_name + '   ' + attr_resident + '   size: ' + str(content_size))
        elif attr_type == 48:
            content_size = as_signed_le(mft[attr_offset + 16: attr_offset + 20])
            content_offset = as_signed_le(mft[attr_offset + 20: attr_offset + 22])
            filename_info = mft[attr_offset + content_offset:attr_offset + content_offset + content_size]
            results.append('$FILE_NAME Attribute Values:')
            flags = as_signed_le(filename_info[56:60])
            results.append(get_flags(flags))
            length_of_name = as_signed_le(filename_info[64:65]) * 2
            name = filename_info[66:66+length_of_name].decode('utf-16')
            results.append('Name: '+name)
            file_ref = filename_info[0:8]
            seq_num = as_signed_le(file_ref[-2:])
            parent_mft = as_signed_le(file_ref[:6])
            results.append('Parent MFT Entry: '+ str(parent_mft) + ' \tSequence: '+str(seq_num))
            allocated_size = as_signed_le(filename_info[40:48])
            actual_size = as_signed_le(filename_info[48:56])
            results.append('Allocated Size: ' + str(allocated_size) + '   \tActual Size: ' + str(actual_size))
            results.append('Created:\t' + into_localtime_string(as_signed_le(filename_info[8:16])))
            results.append('File Modified:\t' + into_localtime_string(as_signed_le(filename_info[16:24])))
            results.append('MFT Modified:\t' + into_localtime_string(as_signed_le(filename_info[24:32])))
            results.append('Accessed:\t' + into_localtime_string(as_signed_le(filename_info[32:40])))
            results.append('')
            if attr_name_offset:
                attr_name = mft[attr_name_offset:attr_name_offset+attr_name_length].decode('utf-16')
            attr_list.append('Type: $FILE_NAME (48-' + str(
                attr_id) + ')   Name: ' + attr_name + '   ' + attr_resident + '   size: ' + str(content_size))
        elif attr_type == 128:
            if attr_name_offset:
                attr_name = mft[attr_name_offset:attr_name_offset+attr_name_length].decode('utf-16')
            data_string = 'Type: $DATA (128-' + str(attr_id) + ')   Name: ' + attr_name + '   ' + attr_resident
            if not attr_non_resident:
                data_string += '   size: ' + str(as_signed_le(mft[attr_offset + 16: attr_offset + 20]))
            else:
                data_string += '   size: ' + str(as_signed_le(mft[attr_offset + 48: attr_offset + 56]))
                data_string += '  init_size: ' + str(as_signed_le(mft[attr_offset + 56: attr_offset + 64]))
            attr_list.append(data_string)
            if attr_non_resident:
                runlist_offset = as_signed_le(mft[attr_offset+32:attr_offset+34])
                num_vcn = as_signed_le(mft[attr_offset+24:attr_offset+32]) - as_signed_le(mft[attr_offset+16:attr_offset+24]) + 1
                prev_offset = attr_offset + runlist_offset
                count = 0
                line = []
                run_list = []
                run_offset = 0
                while count < num_vcn:
                    runlist_first_byte = mft[prev_offset]
                    run_length_in_bytes = runlist_first_byte & 0b00001111
                    run_offset_in_bytes = (runlist_first_byte & 0b11110000) >> 4
                    run_length = as_signed_le(mft[prev_offset+1:prev_offset+1+run_length_in_bytes])
                    run_offset += as_signed_le(mft[prev_offset+1+run_length_in_bytes:prev_offset+1+run_length_in_bytes+run_offset_in_bytes])
                    off = 0
                    while off < run_length:
                        if len(line) == 8:
                            run_list.append(" ".join(line))
                            line = [str(run_offset+off)]
                        else:
                            line.append(str(run_offset+off))
                        off+=1
                        count+=1
                    prev_offset = prev_offset+1+run_length_in_bytes+run_offset_in_bytes
                if len(line) != 0:
                    run_list.append(" ".join(line))
                attr_list += run_list
        attr_offset = attr_offset + attr_length
    results += attr_list
    return results


def into_localtime_string(windows_timestamp):
    """
    Convert a windows timestamp into istat-compatible output.

    Assumes your local host is in the EDT timezone.

    :param windows_timestamp: the struct.decoded 8-byte windows timestamp 
    :return: an istat-compatible string representation of this time in EDT
    """
    dt = datetime.datetime.fromtimestamp((windows_timestamp - 116444736000000000) / 10000000)
    hms = dt.strftime('%Y-%m-%d %H:%M:%S')
    fraction = windows_timestamp % 10000000
    return hms + '.' + str(fraction) + '00 (EDT)'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Display details of a meta-data structure (i.e. inode).')
    parser.add_argument('-o', type=int, default=0, metavar='imgoffset',
                        help='The offset of the file system in the image (in sectors)')
    parser.add_argument('-b', type=int, default=512, metavar='dev_sector_size',
                        help='The size (in bytes) of the device sectors')
    parser.add_argument('image', help='Path to an NTFS raw (dd) image')
    parser.add_argument('address', type=int, help='Meta-data number to display stats on')
    args = parser.parse_args()
    with open(args.image, 'rb') as f:
        result = istat_ntfs(f, args.address, args.b, args.o)
        for line in result:
            print(line.strip())