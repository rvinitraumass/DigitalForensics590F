import unittest

import fsstat_fat16
import tsk_helper


class TestFSStatFat16(unittest.TestCase):
    def testAdams(self):
        with open('adams.dd.fsstat.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('adams.dd', 'rb') as f:
            actual = tsk_helper.strip_all(fsstat_fat16.fsstat_fat16(f))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
