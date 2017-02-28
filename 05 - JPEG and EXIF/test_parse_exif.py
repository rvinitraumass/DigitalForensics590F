import unittest


import jpeg_exif


class TestParseExif(unittest.TestCase):
    def test_fullsizerender(self):
        with open('FullSizeRender.jpg', 'rb') as f:
            self.assertEqual({'DateTime': '2015:01:10 16:18:44',
                              'ExifIFDPointer': 180,
                              'GPSInfoIFDPointer': 978,
                              'Make': 'Apple',
                              'Model': 'iPhone 5',
                              'ResolutionUnit': 2,
                              'Software': '8.1.2',
                              'XResolution': '72/1',
                              'YResolution': '72/1'},
                             jpeg_exif.parse_exif(f))

    def test_goresuperman(self):
        with open('gore-superman.jpg', 'rb') as f:
            self.assertEqual({'Compression': 6,
                              'DateTime': '2006:06:06 21:02:57',
                              'ExifIFDPointer': 164,
                              'JPEGInterchangeFormat': 302,
                              'JPEGInterchangeFormatLength': 4814,
                              'Orientation': 1,
                              'ResolutionUnit': 2,
                              'Software': 'Adobe Photoshop Elements 2.0',
                              'XResolution': '72/1',
                              'YResolution': '72/1'},
                             jpeg_exif.parse_exif(f))


if __name__ == '__main__':
    unittest.main()
