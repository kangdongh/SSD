import os
from unittest import TestCase, skip
from unittest.mock import patch

from hardware.ssd import SSD
from hardware.ssd_reader import SSDReader
from hardware.ssd_writer import SSDWriter

TEST_DATA_FILE_PATH = './test_nand.txt'
TEST_RESULT_FILE_PATH = './test_result.txt'
INITIAL_DATA_VALUE = '0x00000000'


class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD(SSDReader(), SSDWriter(), TEST_DATA_FILE_PATH, TEST_RESULT_FILE_PATH)

    def tearDown(self):
        os.remove(TEST_DATA_FILE_PATH)
        os.remove(TEST_RESULT_FILE_PATH)

    @skip
    def test_initialize(self):
        self.assertEqual(True, os.path.exists(TEST_DATA_FILE_PATH))
        self.assertEqual(True, os.path.exists(TEST_RESULT_FILE_PATH))

        with open(TEST_DATA_FILE_PATH, 'r') as data_file:
            for _ in range(100):
                self.assertEqual(INITIAL_DATA_VALUE, data_file.readline())

    @skip
    def test_run_invalid_input_LBA(self):
        with self.assertRaises(Exception):
            self.ssd.run(['SSD', 'W', '-5'])
        with self.assertRaises(Exception):
            self.ssd.run(['SSD', 'R', '100'])

    @skip
    def test_run_invalid_input_command(self):
        with self.assertRaises(Exception):
            self.ssd.run(['SSD', 'X', '2'])
        with self.assertRaises(Exception):
            self.ssd.run(['SAD', 'R', '2'])
        with self.assertRaises(Exception):
            self.ssd.run(['SSD', 'W', '2', '0xAABBCCGG'])

    @skip
    @patch.object(SSDReader, 'read')
    def test_run_read(self, read_fn):
        with open(TEST_DATA_FILE_PATH, 'w') as data_file:
            data_file.write('0x00000000\n0x00000000\n0x00000002')
        read_fn.result_value = '0x00000002'

        self.ssd.run(['SSD', 'R', 2])

        with open(TEST_RESULT_FILE_PATH, 'r') as result_file:
            self.assertEqual('0x00000002', result_file.readline())

    @skip
    @patch.object(SSDWriter, 'write')
    def test_run_write(self, write_fn):
        target_address = 2
        self.ssd.run(['SSD', 'W', str(target_address), '0x00000002'])

        with open(TEST_DATA_FILE_PATH, 'r') as data_file:
            for _ in range(target_address):
                data_file.readline()
            self.assertEqual('0x00000002', data_file.readline())
