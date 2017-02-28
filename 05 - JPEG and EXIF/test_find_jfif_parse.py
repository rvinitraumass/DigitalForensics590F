import io
import unittest


import jpeg_exif


class TestFindJFIFParse(unittest.TestCase):
    def setUp(self):
        with open('minimal.jpg', 'rb') as f:
            self.minimal_bytes = f.read()
        self.f_minimal = io.BytesIO(self.minimal_bytes)

        # create an in-memory carveable file-like object with the following layout:
        # 100 bytes
        # valid jpeg
        # 100 bytes
        # invalid: first segment marker not there!
        # 100 bytes
        # invalid marker: FF00
        # 100 bytes
        # invalid: FFFF
        # 100 bytes
        # invalid: FFD8
        # 100 bytes
        # invalid: FFD9
        # 100 bytes
        # truncated

        embedded_data = bytearray(7 * 100 + 8 * len(self.minimal_bytes) + 16)

        offset = 100
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes
        embedded_data[offset + 2] = 0x00

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes
        embedded_data[offset + 21] = 0x00

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes
        embedded_data[offset + 21] = 0xFF

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes
        embedded_data[offset + 21] = 0xD8

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + len(self.minimal_bytes)] = self.minimal_bytes
        embedded_data[offset + 21] = 0xD9

        offset += 100 + len(self.minimal_bytes)
        embedded_data[offset:offset + 16] = bytes.fromhex('ff d8 ff e0 00 10 4a 46  49 46 00 01 01 01 ff d9')

        self.f_embedded = io.BytesIO(embedded_data)

    def test_find_entire_invalid(self):
        data = bytearray(1024)
        data[0] = 0xFF
        data[1] = 0xD8
        data[-2] = 0xFF
        data[-1] = 0xD9
        f = io.BytesIO(data)

        self.assertEqual([], jpeg_exif.find_jfif(f, parse=True))

    def test_find_multiple_invalid(self):
        obviously_invalid_data = bytearray(1024)
        soi_list = [158, 429, 620, 738]
        eoi_list = [8, 670, 848, 890]

        for offset in soi_list:
            obviously_invalid_data[offset] = 0xFF
            obviously_invalid_data[offset + 1] = 0xD8

        for offset in eoi_list:
            obviously_invalid_data[offset] = 0xFF
            obviously_invalid_data[offset + 1] = 0xD9

        f_only_soi_eoi = io.BytesIO(obviously_invalid_data)
        self.assertEqual([], jpeg_exif.find_jfif(f_only_soi_eoi, parse=True))

    def test_find_minimal(self):
        self.assertEqual([(0, len(self.minimal_bytes) - 1)],
                         jpeg_exif.find_jfif(self.f_minimal, parse=True))

    def test_find_minimal_embedded(self):
        data = bytearray(1024)
        data[100:100 + len(self.minimal_bytes)] = self.minimal_bytes
        f = io.BytesIO(data)
        self.assertEqual([(100, 100 + len(self.minimal_bytes) - 1)],
                         jpeg_exif.find_jfif(f, parse=True))

    def test_find_embedded_noparse(self):
        self.assertEqual(
            [(100, 403), (100, 807), (100, 1211), (100, 1615), (100, 2019), (100, 2141), (100, 2423), (100, 2539),
             (504, 807), (504, 1211), (504, 1615), (504, 2019), (504, 2141), (504, 2423), (504, 2539), (908, 1211),
             (908, 1615), (908, 2019), (908, 2141), (908, 2423), (908, 2539), (1312, 1615), (1312, 2019), (1312, 2141),
             (1312, 2423), (1312, 2539), (1716, 2019), (1716, 2141), (1716, 2423), (1716, 2539), (1736, 2019),
             (1736, 2141), (1736, 2423), (1736, 2539), (2120, 2141), (2120, 2423), (2120, 2539), (2524, 2539)],
            sorted(jpeg_exif.find_jfif(self.f_embedded)))

    def test_find_embedded(self):
        self.assertEqual(
            [(100, 403), (100, 807), (100, 1211), (100, 1615), (100, 2019), (100, 2141), (100, 2423), (100, 2539)],
            sorted(jpeg_exif.find_jfif(self.f_embedded, parse=True)))

    def test_find_designs_doc_parse(self):
        with open('Designs.doc', 'rb') as f:
            self.assertEqual(
                [(666773, 2542880), (668803, 673512), (668803, 2542880)],
                sorted(jpeg_exif.find_jfif(f, parse=True)))


if __name__ == '__main__':
    unittest.main()
