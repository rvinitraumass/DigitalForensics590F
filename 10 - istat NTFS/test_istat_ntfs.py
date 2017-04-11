import unittest

import istat_ntfs
import tsk_helper



class TestIstatNtfs(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.fractional_score = {}

    def testSimple(self):
        with open('simple.ntfs.64.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('simple.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 64))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)


    def testImage64(self):
        with open('image.ntfs.64.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 64))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)
    # 
    def testImage65(self):
        with open('image.ntfs.65.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 65))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)

    def testImage67(self):
        with open('image.ntfs.67.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 67))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)

    def testImage68(self):
        with open('image.ntfs.68.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 68))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)

    def testImage69(self):
        with open('image.ntfs.69.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 69))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)

    def testImage70(self):
        with open('image.ntfs.70.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('image.ntfs', 'rb') as f:
            actual = tsk_helper.strip_all(istat_ntfs.istat_ntfs(f, 70))
        if len(expected) != len(actual):
            self.fail()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
