import argparse


def print_strings(file_obj, encoding, min_len, print_all):
    count = 0
    printable = []

    if encoding == 'l':
        byte = file_obj.read(2)
        while byte:
            if (0x20 <= byte[0] <= 0x7e) and byte[1] == 0x00:
                count += 1
                printable.append(byte.decode(encoding='utf-16-le'))
            elif print_all and (0xa1 <= byte[0] <= 0xfe) and (0x00 <= byte[1] <= 0xd7):
                count += 1
                printable.append(byte.decode(encoding='utf-16-le'))
            else:
                if count >= min_len:
                    print(''.join(printable))
                count = 0
                printable = []
            byte = file_obj.read(2)
        if count >= min_len:
            print(''.join(printable))
    elif encoding == 'b':
        byte = file_obj.read(2)
        while byte:
            if (0x20 <= byte[1] <= 0x7e) and byte[0] == 0x00:
                count += 1
                printable.append(byte.decode(encoding='utf-16-be'))
            elif print_all and (0xa1 <= byte[1] <= 0xfe) and (0x00 <= byte[0] <= 0xd7):
                count += 1
                printable.append(byte.decode(encoding='utf-16-be'))
            else:
                if count >= min_len:
                    print(''.join(printable))
                count = 0
                printable = []
            byte = file_obj.read(2)
        if count >= min_len:
            print(''.join(printable))
    else:
        byte = file_obj.read(1)
        while byte:
            flag = False
            if (0x20 <= byte[0] <= 0x7e):
                count += 1
                printable.append(byte.decode(encoding='utf-8'))
                flag = True
            if print_all and not flag and (0xc2 <= byte[0] <= 0xdf):
                byte+=file_obj.read(1)
                if (0xa1 <= byte[1] <= 0xbf):
                    count += 1
                    printable.append(byte.decode(encoding='utf-8'))
                    flag = True
            if print_all and not flag and (0xe0 <= byte[0] <= 0xed):
                if len(byte) != 2:
                    byte += file_obj.read(1)
                byte += file_obj.read(1)
                if (0x80 <= byte[2] <= 0xbf):
                    count += 1
                    printable.append(byte.decode(encoding='utf-8'))
                    flag = True
            if not flag:
                if count >= min_len:
                    print(''.join(printable))
                count = 0
                printable = []
            byte = file_obj.read(1)
        if count >= min_len:
            print(''.join(printable))


def main():
    parser = argparse.ArgumentParser(description='Print the printable strings from a file.')
    parser.add_argument('filename')
    parser.add_argument('-n', metavar='min-len', type=int, default=4,
                        help='Print sequences of characters that are at least min-len characters long')
    parser.add_argument('-e', metavar='encoding', choices=('s', 'l', 'b'), default='s',
                        help='Select the character encoding of the strings that are to be found. ' +
                             'Possible values for encoding are: s = UTF-8, b = big-endian UTF-16, ' +
                             'l = little endian UTF-16.')
    parser.add_argument('-x', action='store_true')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        print_strings(f, args.e, args.n, args.x)

if __name__ == '__main__':
    main()