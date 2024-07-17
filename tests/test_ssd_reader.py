import os
from random import randint
from unittest import TestCase, skip

from hardware.ssd_reader import SSDReader

READ_FILE_DIR = './nand_test.txt'
VALUE_FIRST = '0xAAAABBBB'
VALUE_SECOND = '0x00001111'


class TestSSDReader(TestCase):
    def setUp(self):
        self.file_handler = open(READ_FILE_DIR, 'w')
        for _ in range(50):
            self.file_handler.write(VALUE_FIRST + '\n')
        for _ in range(50):
            self.file_handler.write(VALUE_SECOND + '\n')
        self.file_handler.close()

    def tearDown(self):
        os.remove(READ_FILE_DIR)

    def test_read(self):
        ssd_reader = SSDReader(READ_FILE_DIR)

        for target_address in range(100):
            answer = VALUE_FIRST if target_address < 50 else VALUE_SECOND
            ret = ssd_reader.read(target_address)
            self.assertEqual(answer, ret)
