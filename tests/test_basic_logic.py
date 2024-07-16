import warnings
warnings.filterwarnings('ignore')

import sys
import io

import unittest
from unittest.mock import Mock

from app.basic_logic import BasicLogic

FULL_COUNT = 100
LBA = 3
VALUE = 0x00000000


class TestBasicLogic(unittest.TestCase):
    def setUp(self):
        self.sut = Mock(spec=BasicLogic("basic_logic/test"))
        self.output = io.StringIO()

    @unittest.skip
    def test_read_pass(self):
        sys.stdout = self.output
        self.sut.read(LBA)

        self.assertEqual(self.output.getvalue(), "PASS to read from " + str(LBA))

    @unittest.skip
    def test_read_wrong_address(self):
        wrong_lba = -1

        with self.assertRaises(Exception):
            self.sut.read(wrong_lba)

    @unittest.skip
    def test_write_pass(self):
        self.sut.write(LBA, VALUE)
        # self.sut.read.return_value = VALUE

        self.assertEqual(self.sut.read(LBA), VALUE)

    @unittest.skip
    def test_write_wrong_address(self):
        wrong_lba = -1

        with self.assertRaises(Exception):
            self.sut.write(wrong_lba, VALUE)

    @unittest.skip
    def test_write_wrong_value(self):
        wrong_value = -1

        with self.assertRaises(Exception):
            self.sut.write(LBA, wrong_value)

    @unittest.skip
    def test_full_read(self):
        self.sut.full_read()

        self.assertEqual(self.sut.read.call_count, FULL_COUNT)

    @unittest.skip
    def test_full_write(self):
        self.sut.full_write(VALUE)

        self.assertEqual(self.sut.write.call_count, FULL_COUNT)

    @unittest.skip
    def test_exit_called_once(self):
        self.sut.exit()

        self.sut.exit.assert_called_once()

    @unittest.skip
    def test_help_called_once(self):
        self.sut.help()

        self.sut.help.assert_called_once()


if __name__ == "__main__":
    unittest.main()
