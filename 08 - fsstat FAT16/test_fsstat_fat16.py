import unittest

import fsstat_fat16
import subprocess
import tsk_helper


class TestFSStatFat16(unittest.TestCase):
    def testAdams(self):
        with open('adams.dd.fsstat.out') as f:
            expected = tsk_helper.strip_all(tsk_helper.get_fsstat_output(f))
        with open('adams.dd', 'rb') as f:
            actual = tsk_helper.strip_all(fsstat_fat16.fsstat_fat16(f))
        self.assertEqual(expected, actual)

    def testFragmented(self):
        expected = subprocess.check_output(["fsstat", "fragmented.dd"])
        with open('fragmented.dd.expected', 'w') as f:
            f.write(expected.decode())
        with open('fragmented.dd', 'rb') as f:
            actual = tsk_helper.strip_all(fsstat_fat16.fsstat_fat16(f,1024))
        with open('fragmented.dd.output', 'w') as f:
            f.write("\n".join(actual))
        self.failureException(expected,actual)

    def testSpiff(self):
        expected = subprocess.check_output(["fsstat","-o", "2", "spiff.dd"])
        with open('spiff.dd.expected', 'w') as f:
            f.write(expected.decode())
        with open('spiff.dd', 'rb') as f:
            actual = tsk_helper.strip_all(fsstat_fat16.fsstat_fat16(f,offset=2))
        with open('spiff.dd.output', 'w') as f:
            f.write("\n".join(actual))
        self.failureException(expected,actual)


if __name__ == '__main__':
    unittest.main()
