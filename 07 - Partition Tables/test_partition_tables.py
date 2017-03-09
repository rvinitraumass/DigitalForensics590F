import unittest
from uuid import UUID

import partition_tables


class TestParseMBR(unittest.TestCase):
    def testSimpleMBR(self):
        with open('usb-mbr.dd', 'rb') as f:
            data = f.read(512)
        self.assertEqual([{'type': '0x6', 'end': 3913727, 'start': 32, 'number': 0}],
                         partition_tables.parse_mbr(data))


class TestParseGPT(unittest.TestCase):
    def testSimpleGPT(self):
        with open('disk-image.dd', 'rb') as f:
            self.assertEqual([{'start': 40, 'end': 409639, 'number': 0, 'name': 'EFI system partition',
                               'type': UUID('c12a7328-f81f-11d2-ba4b-00a0c93ec93b')},
                              {'start': 409640, 'end': 585210495, 'number': 1, 'name': 'Iron',
                               'type': UUID('53746f72-6167-11aa-aa11-00306543ecac')},
                              {'start': 585210496, 'end': 586480031, 'number': 2, 'name': 'Recovery HD',
                               'type': UUID('426f6f74-0000-11aa-aa11-00306543ecac')},
                              {'start': 586481664, 'end': 976842879, 'number': 3, 'name': 'Apple_HFS_Untitled_2',
                               'type': UUID('48465300-0000-11aa-aa11-00306543ecac')}],
                             partition_tables.parse_gpt(f, 512))


if __name__ == '__main__':
    unittest.main()
