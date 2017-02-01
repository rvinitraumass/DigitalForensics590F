import sys


def convert_to_hex(byte_seq):
    result = []
    count = 0
    for b in byte_seq:  # we can iterate over the bytes, since they're a sequence
        if count == 8:
            result.append(' {0:0{1}x}'.format(b, 2))
        else:
            result.append('{0:0{1}x}'.format(b, 2))
        count+=1
    return result


def convert_to_ascii(byte_seq):
    result = []
    for b in byte_seq:
        if b >= 0x20 and b <= 0x7e:
            result.append(chr(b))
        else:
            result.append('.')
    return result


def dump_file_hex(filename):
    with open(filename, 'rb') as f:  # when opened in binary mode, you can read() the entire file, or
                                     # read(16) some number of bytes at a time as an immutable sequence of bytes
        chunk = f.read(16)
        line_number = 0
        chunk_size = 0
        while chunk:  # empty sequences (that is, of length 0) evaluate to false
            print('{:08x}'.format(line_number*16), end='  ')  # print the line number, in hex, zero-padded to four places

            hex_list = convert_to_hex(chunk)
            line = ' '.join(hex_list)  # join() joins the list of strings, using the string it's called on
                                       # as the separator character
            if len(hex_list) < 8:
                print(line + ((16 - len(hex_list)) * 3) * ' ', end='   ')
            elif len(hex_list) < 16:
                print(line + ((16 - len(hex_list)) * 3) * ' ', end='  ')
            else:
                print(line , end='  ')

            ascii_list = convert_to_ascii(chunk)
            print('|'+''.join(ascii_list)+'|')

            chunk_size = len(chunk)
            chunk = f.read(16)
            line_number += 1
        if line_number != 0:
            print('{:08x}'.format((line_number-1) * 16 + chunk_size))  # print the line number, in hex, zero-padded to four places


def main():
    dump_file_hex(sys.argv[1])

if __name__ == '__main__':
    main()