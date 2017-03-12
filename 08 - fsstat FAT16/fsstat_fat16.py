import struct

def as_le_unsigned(b):
    table = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    return struct.unpack('<' + table[len(b)], b)[0]

def fsstat_fat16(fat16_file, sector_size=512, offset=0):
    result = ['FILE SYSTEM INFORMATION',
              '--------------------------------------------',
              'File System Type: FAT16',
              '']
    boot_sector = fat16_file.read(sector_size)
    result.append('OEM Name: '+ boot_sector[3:11].decode('ascii').strip())
    result.append('Volume ID: ' + hex(as_le_unsigned(boot_sector[39:43])))
    result.append('Volume Label (Boot Sector): ' + boot_sector[43:54].decode('ascii').strip())
    result.append('File System Type Label: ' + boot_sector[54:62].decode('ascii').strip())
    result.append('')
    sectors_before_start = as_le_unsigned(boot_sector[28:32])
    result.append('Sectors before file system: '+ str(sectors_before_start))
    result.append('')
    result.append('File System Layout( in sectors)')
    sector_count = max(as_le_unsigned(boot_sector[19:21]), as_le_unsigned(boot_sector[32:36]))-1
    result.append('Total Range: '+ str(sectors_before_start)+ ' - ' + str(sector_count))
    reserved_area_size = as_le_unsigned(boot_sector[14:16])
    result.append('* Reserved: ' + str(sectors_before_start) + ' - ' + str(sectors_before_start + reserved_area_size-1))
    result.append('** Boot Sector: ' + str(sectors_before_start))
    fat_size = as_le_unsigned(boot_sector[22:24])
    fat_start = sectors_before_start + 1
    number_of_fats = as_le_unsigned(boot_sector[16:17])
    for f in range(number_of_fats):
        result.append('* FAT '+str(f)+': ' + str(fat_start) +' - '+ str(fat_start+fat_size-1))
        fat_start = (f+1)*fat_size+1
    data_area_start = number_of_fats * fat_size + 1
    result.append('* Data Area: ' + str(data_area_start) +' - '+ str(sector_count))
    root_area_end = data_area_start + as_le_unsigned(boot_sector[17:19])*32//sector_size-1
    result.append('** Root Directory: ' + str(data_area_start) + ' - ' + str(root_area_end))
    cluster_size = as_le_unsigned(boot_sector[13:14])
    num_clusters = (sector_count - root_area_end) // cluster_size
    cluster_area_end = root_area_end + cluster_size * num_clusters
    result.append('** Cluster Area: '+ str(root_area_end+1) + ' - ' + str(cluster_area_end))
    if sector_count - cluster_area_end != 0:
        result.append('** Non-clustered: ' + str(cluster_area_end + 1) + ' - ' + str(sector_count))
    result.append('')
    result.append('CONTENT INFORMATION')
    result.append('--------------------------------------------')
    result.append('Sector Size: ' + str(sector_size))
    result.append('Cluster Size: ' + str(cluster_size * sector_size))
    result.append('Total Cluster Range: 2 - ' + str(num_clusters+1))
    result.append('')
    result.append('FAT CONTENTS (in sectors)')
    result.append('--------------------------------------------')


    # then do a few things, .append()ing to result as needed

    return result

# if __name__ == '__main__':
#     with open('adams.dd', 'rb') as f:
#         print("\n".join(fsstat_fat16(f)))