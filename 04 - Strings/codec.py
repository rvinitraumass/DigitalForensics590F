def encode(codepoint):
    encoded_array = []
    if codepoint <= 0x007f:
        encoded_array.append(codepoint)
    elif codepoint <= 0x07ff:
        encoded_array.append(((codepoint >> 6) & 0b00011111) | 0b11000000)
        encoded_array.append((codepoint & 0b00111111) | 0b10000000)
    elif codepoint <= 0xffff:
        encoded_array.append(((codepoint >> 12) & 0b00001111) | 0b11100000)
        encoded_array.append(((codepoint >> 6) & 0b00111111) | 0b10000000)
        encoded_array.append((codepoint & 0b00111111) | 0b10000000)
    elif codepoint <= 0x10ffff:
        encoded_array.append(((codepoint >> 18) & 0b00000111) | 0b11110000)
        encoded_array.append(((codepoint >> 12) & 0b00111111) | 0b10000000)
        encoded_array.append(((codepoint >> 6) & 0b00111111) | 0b10000000)
        encoded_array.append((codepoint & 0b00111111) | 0b10000000)
    return bytes(encoded_array)


def decode(bytes_object):
    decoded_number = 0
    if len(bytes_object) == 1:
        decoded_number = bytes_object[0]
    elif len(bytes_object) == 2:
        decoded_number = ((bytes_object[0] & 0b00011111) << 6) | (bytes_object[1] & 0b00111111)
    elif len(bytes_object) == 3:
        decoded_number = ((bytes_object[0] & 0b00001111) << 12) | ((bytes_object[1] & 0b00111111) << 6) | (bytes_object[2] & 0b00111111)
    elif len(bytes_object) == 4:
        decoded_number = ((bytes_object[0] & 0b00000111) << 18) | ((bytes_object[1] & 0b00111111) << 12) | ((bytes_object[2] & 0b00111111) << 6) | (
        bytes_object[3] & 0b00111111)
    return decoded_number


def main():
    pass

if __name__ == '__main__':
    main()