from unittest import skip, TestCase
from unittest.mock import Mock

from app.basic_logic import BasicLogic

NUM_LBA = 100
TEMP_SSD_PATH = "basic_logic/test"
FULL_COUNT = 100
LBA = '3'
VALUE = '0x00000001'


class TestBasicLogic(TestCase):
    def setUp(self):
        self.system_call_handler = Mock()
        self.system_call_handler.get_result.return_value = VALUE
        self.sut = BasicLogic(self.system_call_handler)

    @skip
    def test_read_result(self):
        ret = self.sut.read(LBA)

        self.assertEqual(ret, VALUE)
        self.system_call_handler.run.assert_called_once()
        self.system_call_handler.run.assert_any_call(['R', LBA])
        self.system_call_handler.get_result.assert_call_once()

    def test_write_result(self):
        self.sut.write(LBA, VALUE)

        self.system_call_handler.run.assert_called_once()
        self.system_call_handler.run.assert_any_call(['W', LBA, VALUE])

    @skip
    def test_full_read(self):
        expected_result = '\n'.join([VALUE] * NUM_LBA)

        ret = self.sut.full_read()

        self.assertEqual(ret, expected_result)
        self.assertEqual(self.system_call_handler.run.call_count, NUM_LBA)
        self.assertEqual(self.system_call_handler.get_result.call_count, NUM_LBA)

    def test_full_write(self):
        self.sut.full_write(VALUE)

        self.assertEqual(self.system_call_handler.run.call_count, NUM_LBA)
