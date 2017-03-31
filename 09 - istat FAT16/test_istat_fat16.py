import unittest

import istat_fat16
import tsk_helper


class TestIstatFat16(unittest.TestCase):
    def testAdams5(self):
        with open('adams.dd.5.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('adams.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 5))

        self.assertEqual(expected, actual)

    def testAdams7(self):
        with open('adams.dd.7.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('adams.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 7))

        self.assertEqual(expected, actual)

    def testAdams549(self):
        # note: 590F-only
        with open('adams.dd.549.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('adams.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 549))

        self.assertEqual(expected, actual)

    def testFragmented5(self):
        with open('fragmented.dd.5.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('fragmented.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 5, 1024))

        self.assertEqual(expected, actual)

    def testFragmented7(self):
        with open('fragmented.dd.7.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('fragmented.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 7, 1024))

        self.assertEqual(expected, actual)

    def testSpiff5(self):
        with open('spiff.dd.5.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('spiff.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 5, offset=2))

        self.assertEqual(expected, actual)

    def testSpiff12(self):
        with open('spiff.dd.12.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('spiff.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 12, offset=2))

        self.assertEqual(expected, actual)

    def testSpiff14(self):
        with open('spiff.dd.14.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('spiff.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 14, offset=2))

        self.assertEqual(expected, actual)

    def testSpiff679(self):
        with open('spiff.dd.679.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('spiff.dd', 'rb') as f:
            actual = tsk_helper.strip_all(istat_fat16.istat_fat16(f, 679, offset=2))

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
