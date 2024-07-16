from unittest import TestCase
from unittest.mock import Mock

from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2

TEST_APP_2_NUM_LBA = 6


def app1_raise_if_write_out_of_range(val: str):
    if val != TestApp1.FULL_WRITE_VALUE:
        raise ValueError()
    return None


def app2_raise_if_write_out_of_range(addr: str, val: str):
    addr = int(addr)
    if addr > 5 or addr < 0:
        raise ValueError()
    if val not in [TestApp2.FIRST_WRITE_VALUE, TestApp2.OVERWRITE_VALUE]:
        raise ValueError()
    return None


def app2_raise_if_read_out_of_range(addr: int):
    addr = int(addr)
    if addr > 5 or addr < 0:
        raise ValueError()
    return TestApp2.OVERWRITE_VALUE


class TestTestApps(TestCase):
    def setUp(self):
        self.basic_logic = Mock()
        self.test_app_1 = TestApp1()
        self.test_app_2 = TestApp2()

    def test_app_1_call_basic_logic_functions_correctly(self):
        self.basic_logic.full_read.return_value = '\n'.join([TestApp1.FULL_WRITE_VALUE] * 100)
        self.basic_logic.full_write.side_effect = app1_raise_if_write_out_of_range

        self.test_app_1.run(self.basic_logic)

        self.basic_logic.full_write.assert_called_once()
        self.basic_logic.full_read.assert_called_once()

    def test_app_1_error_detected(self):
        self.basic_logic.full_read.return_value = ''

        with self.assertRaises(Exception):
            self.test_app_1.run(self.basic_logic)

    def test_app_2_call_basic_logic_functions_correctly(self):
        self.basic_logic.write.side_effect = app2_raise_if_write_out_of_range
        self.basic_logic.read.side_effect = app2_raise_if_read_out_of_range

        self.test_app_2.run(self.basic_logic)

        self.assertEqual(self.basic_logic.write.call_count,
                         TestApp2.DUPL_WRITE_COUNT * TEST_APP_2_NUM_LBA + TEST_APP_2_NUM_LBA)
        self.assertEqual(self.basic_logic.read.call_count, TEST_APP_2_NUM_LBA)

    def test_app_2_error_detected(self):
        self.basic_logic.read.return_value = TestApp2.FIRST_WRITE_VALUE

        with self.assertRaises(Exception):
            self.test_app_2.run(self.basic_logic)
