import io
import unittest


import jpeg_exif


class TestCarve(unittest.TestCase):
    def setUp(self):
        # first create some synthetic test data
        self.data = bytes([b for b in range(256)] * 16)

        # then create a file-like object on that data
        # (behaves the same as something you open())
        self.f = io.BytesIO(self.data)

    def test_carve_all(self):
        data = jpeg_exif.carve(self.f, 0, len(self.data) - 1)
        self.assertEqual(len(self.data), len(data))
        self.assertEqual(self.data, data)

    def test_carve_from_front(self):
        data = jpeg_exif.carve(self.f, 0, 63)
        self.assertEqual(64, len(data))
        self.assertEqual(self.data[:64], data)

    def test_carve_from_rear(self):
        data = jpeg_exif.carve(self.f, len(self.data) - 1 - 63, len(self.data) - 1)
        self.assertEqual(64, len(data))
        self.assertEqual(self.data[-64:], data)

    def test_carve_from_middle(self):
        data = jpeg_exif.carve(self.f, 64, len(self.data) - 1 - 64)
        self.assertEqual(len(self.data) - 128, len(data))
        self.assertEqual(self.data[64:-64], data)


if __name__ == '__main__':
    unittest.main()
