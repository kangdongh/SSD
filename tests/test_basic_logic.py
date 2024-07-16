import warnings
warnings.filterwarnings('ignore')

import unittest
from unittest.mock import patch

from app.basic_logic import BasicLogic

TEMP_SSD_PATH = "basic_logic/test"
FULL_COUNT = 100
LBA = 3
VALUE = 0x00000000


class TestBasicLogic(unittest.TestCase):
    @unittest.skip
    @patch.object(BasicLogic, '_system_call')
    def test_read_result(self, mk):
        pass

    @patch.object(BasicLogic, '_read_result')
    def test_read_result(self, read_mk):
        read_mk.return_value = "0x0000000F"

        basic_logic = BasicLogic(TEMP_SSD_PATH)
        self.assertEqual(basic_logic._read_result(), "0x0000000F")
        self.assertEqual(read_mk.call_count, 1)

    @patch.object(BasicLogic, '_write_result')
    @patch.object(BasicLogic, '_read_result')
    def test_write_result(self, read_mk, write_mk):
        read_mk.return_value = "0x0000000F"

        basic_logic = BasicLogic(TEMP_SSD_PATH)
        basic_logic._write_result()

        self.assertEqual(basic_logic._read_result(), "0x0000000F")
        self.assertEqual(write_mk.call_count, 1)

    @patch.object(BasicLogic, '_help_result')
    def test_help_result(self, mk):
        mk.return_value = "This is the help desc"

        basic_logic = BasicLogic(TEMP_SSD_PATH)
        basic_logic._help_result()

        self.assertEqual(mk.call_count, 1)


if __name__ == "__main__":
    unittest.main()
