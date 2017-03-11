import struct
import uuid


def parse_mbr(mbr_bytes):
    mbr_entries = []
    number = 0
    for offset in [0,16,32,48]:
        entry = {}
        partition = mbr_bytes[446+offset:462+offset]
        type = struct.unpack('<B', partition[4:5])[0]
        if type:
            entry['type'] = hex(type)
            entry['number'] = number
            number += 1
            lba_start = struct.unpack('<I',partition[8:12])[0]
            entry['start'] = lba_start
            sector_size = struct.unpack('<I',partition[12:16])[0]
            entry['end'] = lba_start + sector_size - 1
            mbr_entries.append(entry)
    return mbr_entries


def parse_gpt(gpt_file, sector_size=512):
    gpt_entries = []
    gpt_file.seek(sector_size)
    gpt_header = gpt_file.read(sector_size)
    table_start = struct.unpack('<Q', gpt_header[72:80])[0]
    number_of_entries = struct.unpack('<I', gpt_header[80:84])[0]
    entry_size = struct.unpack('<I', gpt_header[84:88])[0]
    gpt_file.seek(table_start*sector_size)
    partition_table = gpt_file.read(number_of_entries*entry_size)
    for number in range(0,number_of_entries):
        entry = {}
        entry_offset = number * entry_size
        type = uuid.UUID(bytes_le=partition_table[entry_offset:entry_offset+16])
        if type != uuid.UUID(int=0):
            entry['type'] = type
            entry['number'] = number
            number+=1
            entry['start'] = struct.unpack('<Q',partition_table[entry_offset+32:entry_offset+40])[0]
            entry['end'] = struct.unpack('<Q', partition_table[entry_offset+40:entry_offset+48])[0]
            entry['name'] = partition_table[entry_offset+56:entry_offset+128].decode('utf-16-le').split('\x00',1)[0]
            gpt_entries.append(entry)
    return gpt_entries