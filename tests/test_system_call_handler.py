import os
from unittest import TestCase

from app.system_call_handler import SystemCallHandler, initialize_system_call_handler

INVALID_RESULT_PATH = os.path.abspath('./invalid.txt')

INVALID_SSD_PATH = os.path.abspath('./invalid_ssd_file_path.py')


class TestSystemCallHandler(TestCase):
    def test_singleton(self):
        initialize_system_call_handler(INVALID_SSD_PATH, INVALID_RESULT_PATH)
        sut = SystemCallHandler()
        self.assertEqual(INVALID_SSD_PATH, sut.get_ssd_path())
        self.assertEqual(INVALID_RESULT_PATH, sut.get_result_file_path())
