import io
import unittest


import jpeg_exif


class TestFindJFIF(unittest.TestCase):
    def setUp(self):
        data = bytearray(1024)
        soi_list = [158, 429, 620, 738]
        eoi_list = [8, 670, 848, 890]

        for offset in soi_list:
            data[offset] = 0xFF
            data[offset + 1] = 0xD8

        for offset in eoi_list:
            data[offset] = 0xFF
            data[offset + 1] = 0xD9

        self.f = io.BytesIO(data)

    def test_find_entire(self):
        data = bytearray(1024)
        data[0] = 0xFF
        data[1] = 0xD8
        data[-2] = 0xFF
        data[-1] = 0xD9
        f = io.BytesIO(data)

        self.assertEqual([(0, len(data) - 1)], jpeg_exif.find_jfif(f))

    def test_find_multiple(self):
        self.assertEqual([(158, 671), (158, 849), (158, 891),
                          (429, 671), (429, 849), (429, 891),
                          (620, 671), (620, 849), (620, 891),
                          (738, 849), (738, 891)],
                         sorted(jpeg_exif.find_jfif(self.f)))

    def test_find_multiple_max_include(self):
        self.assertEqual([(620, 671), (738, 849), (738, 891)],
                         sorted(jpeg_exif.find_jfif(self.f, max_length=154)))

    def test_find_multiple_max_exclude(self):
        self.assertEqual([(620, 671), (738, 849)],
                         sorted(jpeg_exif.find_jfif(self.f, max_length=153)))

    def test_find_multiple_designs_doc(self):
        with open('Designs.doc', 'rb') as f:
            self.assertEqual([(17210, 40511),
                              (17210, 63148),
                              (17210, 184712),
                              (17210, 263982),
                              (17210, 334302),
                              (17210, 408520),
                              (17210, 461199),
                              (17210, 542219),
                              (17210, 552600),
                              (17210, 673512),
                              (17210, 2542880),
                              (144732, 184712),
                              (144732, 263982),
                              (144732, 334302),
                              (144732, 408520),
                              (144732, 461199),
                              (144732, 542219),
                              (144732, 552600),
                              (144732, 673512),
                              (144732, 2542880),
                              (153983, 184712),
                              (153983, 263982),
                              (153983, 334302),
                              (153983, 408520),
                              (153983, 461199),
                              (153983, 542219),
                              (153983, 552600),
                              (153983, 673512),
                              (153983, 2542880),
                              (162806, 184712),
                              (162806, 263982),
                              (162806, 334302),
                              (162806, 408520),
                              (162806, 461199),
                              (162806, 542219),
                              (162806, 552600),
                              (162806, 673512),
                              (162806, 2542880),
                              (179338, 184712),
                              (179338, 263982),
                              (179338, 334302),
                              (179338, 408520),
                              (179338, 461199),
                              (179338, 542219),
                              (179338, 552600),
                              (179338, 673512),
                              (179338, 2542880),
                              (343742, 408520),
                              (343742, 461199),
                              (343742, 542219),
                              (343742, 552600),
                              (343742, 673512),
                              (343742, 2542880),
                              (377194, 408520),
                              (377194, 461199),
                              (377194, 542219),
                              (377194, 552600),
                              (377194, 673512),
                              (377194, 2542880),
                              (538358, 542219),
                              (538358, 552600),
                              (538358, 673512),
                              (538358, 2542880),
                              (646496, 673512),
                              (646496, 2542880),
                              (666773, 673512),
                              (666773, 2542880),
                              (668803, 673512),
                              (668803, 2542880)],
                             jpeg_exif.find_jfif(f))


if __name__ == '__main__':
    unittest.main()
