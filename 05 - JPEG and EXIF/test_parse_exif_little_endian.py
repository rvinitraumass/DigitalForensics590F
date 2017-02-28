import unittest


import jpeg_exif


class TestParseExifLittleEndian(unittest.TestCase):
    def test_leaves(self):
        with open('leaves.jpg', 'rb') as f:
            self.assertEqual({'Compression': 6,
                              'DateTime': '2015:11:09 11:59:11',
                              'ExifIFDPointer': 14248,
                              'JPEGInterchangeFormat': 35652,
                              'JPEGInterchangeFormatLength': 3459,
                              'Make': 'EASTMAN KODAK COMPANY',
                              'Model': 'KODAK EASYSHARE C195 Digital Camera',
                              'Orientation': 1,
                              'ResolutionUnit': 2,
                              'XResolution': '72/1',
                              'YCbCrPositioning': 1,
                              'YResolution': '72/1'},
                             jpeg_exif.parse_exif(f))


if __name__ == '__main__':
    unittest.main()
