from unittest import TestCase
from unittest.mock import patch

from app.api import read_ssd, write_ssd, erase_ssd, flush_ssd
from app.system_call_handler import SystemCallHandler

VALUE = '0x00000001'


class TestAPI(TestCase):

    def setUp(self):
        self.run_mk = patch.object(SystemCallHandler, 'run').start()
        self.get_result_mk = patch.object(SystemCallHandler, 'get_result').start()

    def test_read_ssd(self):
        self.get_result_mk.return_value = VALUE

        self.assertEqual(read_ssd(1), VALUE)
        self.get_result_mk.assert_called_once()
        self.run_mk.assert_called_once()
        self.run_mk.assert_any_call(['R', '1'])

    def test_write_ssd(self):
        write_ssd(1, VALUE)
        self.run_mk.assert_called_once()
        self.run_mk.assert_any_call(['W', '1', VALUE])

    def test_erase_ssd(self):
        erase_ssd(1, 15)
        self.assertEqual(self.run_mk.call_count, 2)

    def test_flush_ssd(self):
        flush_ssd()
        self.run_mk.assert_called_once()
        self.run_mk.assert_any_call(['F'])
