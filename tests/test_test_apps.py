from unittest import TestCase, skip
from unittest.mock import Mock

from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2

APP2_WRITE_VALUE_LOWERCASE = '0xaaaabbbb'

APP2_OVERWRITE_VALUE = '0x12345678'

TEST_APP_2_DUPL_WRITE_COUNT = 30

TEST_APP_2_NUM_LBA = 6


def raise_if_write_out_of_range(addr: int, val: str):
    if addr > 5 or addr < 0:
        raise ValueError()
    if val.lower() not in [APP2_WRITE_VALUE_LOWERCASE or APP2_OVERWRITE_VALUE]:
        raise ValueError()
    return None


def raise_if_read_out_of_range(addr: int):
    if addr > 5 or addr < 0:
        raise ValueError()
    return APP2_OVERWRITE_VALUE


class TestTestApps(TestCase):
    def setUp(self):
        self.basic_logic = Mock()
        self.basic_logic.full_read.return_value = '0x00000001\n' * 100
        self.test_app_1 = TestApp1()
        self.test_app_2 = TestApp2()

    @skip
    def test_app_1_call_basic_logic_functions_correctly(self):
        self.test_app_1.run(self.basic_logic)
        self.basic_logic.full_write.assert_called_once()
        self.basic_logic.full_read.assert_called_once()

    @skip
    def test_app_1_error_detected(self):
        self.basic_logic.full_read.return_value = ''

        with self.assertRaises(Exception):
            self.test_app_1.run(self.basic_logic)

    @skip
    def test_app_2_call_basic_logic_functions_correctly(self):
        self.basic_logic.write.side_effects = raise_if_write_out_of_range
        self.basic_logic.read.side_effects = raise_if_read_out_of_range

        self.test_app_2.run(self.basic_logic)

        self.assertEqual(self.basic_logic.write.call_count,
                         TEST_APP_2_DUPL_WRITE_COUNT * TEST_APP_2_NUM_LBA + TEST_APP_2_NUM_LBA)
        self.assertEqual(self.basic_logic.read.call_count, TEST_APP_2_NUM_LBA)

    @skip
    def test_app_2_error_detected(self):
        self.basic_logic.read.return_value = '0xAAAABBBB'

        with self.assertRaises(Exception):
            self.test_app_2.run(self.basic_logic)
