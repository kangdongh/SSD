import os
from unittest import TestCase

from hardware.ssd import SSD

TEST_DATA_FILE_PATH = './test_nand.txt'
TEST_RESULT_FILE_PATH = './test_result.txt'
INITIAL_DATA_VALUE = '0x00000000'


class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD(TEST_DATA_FILE_PATH, TEST_RESULT_FILE_PATH)

    def tearDown(self):
        os.remove(TEST_DATA_FILE_PATH)
        os.remove(TEST_RESULT_FILE_PATH)

    def get_lines(self, file_name):
        with open(file_name, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

    def test_initialize_if_file_not_exist_before(self):
        self.assertEqual(True, os.path.exists(TEST_DATA_FILE_PATH))
        self.assertEqual(True, os.path.exists(TEST_RESULT_FILE_PATH))

        lines = self.get_lines(TEST_DATA_FILE_PATH)
        for i in range(100):
            self.assertEqual(INITIAL_DATA_VALUE, lines[i])

    def test_initialize_if_file_exist_before(self):
        with open(TEST_DATA_FILE_PATH, 'w') as data_file:
            data_file.write('0xAAAAAAAA\n0xBBBBBBBB\n0xCCCCCCCC\n')
            for _ in range(97):
                data_file.write(INITIAL_DATA_VALUE + '\n')

        self.ssd.initialize()

        lines = self.get_lines(TEST_DATA_FILE_PATH)
        self.assertEqual('0xAAAAAAAA', lines[0])
        self.assertEqual('0xBBBBBBBB', lines[1])
        self.assertEqual('0xCCCCCCCC', lines[2])
        for i in range(3, 100):
            self.assertEqual(INITIAL_DATA_VALUE, lines[i])

    def assert_ssd_run_raises(self, args):
        with self.assertRaises(Exception):
            self.ssd.run(args)

    def test_run_invalid_input_LBA(self):
        with self.subTest("LBA=-5"):
            self.assert_ssd_run_raises(['ssd', 'R', '-5'])
        with self.subTest("LBA=100"):
            self.assert_ssd_run_raises(['ssd', 'W', '100'])
        with self.subTest("LBA=-3"):
            self.assert_ssd_run_raises(['ssd', 'E', '-1', '1'])

    def test_run_invalid_input_command(self):
        with self.subTest("INVALID TYPE"):
            self.assert_ssd_run_raises(['ssd', 'X', '2'])
        with self.subTest("INVALID VALUE"):
            self.assert_ssd_run_raises(['ssd', 'W', '2', '0xAABBCCGG'])
        with self.subTest("INVALID VALUE"):
            self.assert_ssd_run_raises(['ssd', 'E', '98', '3'])
        with self.subTest("INVALID VALUE"):
            self.assert_ssd_run_raises(['ssd', 'E', '1', '11'])
        with self.subTest("INVALID VALUE"):
            self.assert_ssd_run_raises(['ssd', 'E', '1', 'A'])

    def test_run_read(self):
        with open(TEST_DATA_FILE_PATH, 'w') as data_file:
            data_file.write('0x00000000\n0x00000000\n0x00000002\n')
            for _ in range(97):
                data_file.write(INITIAL_DATA_VALUE + '\n')

        self.ssd.run(['ssd', 'R', '2'])

        lines = self.get_lines(TEST_RESULT_FILE_PATH)
        self.assertEqual('0x00000002', lines[0])

    def test_run_write(self):
        target_address = 6
        self.ssd.run(['ssd', 'W', str(target_address), '0x00000002'])

        lines = self.get_lines(TEST_DATA_FILE_PATH)
        self.assertEqual('0x00000002', lines[target_address])

    def test_run_erase(self):
        with open(TEST_DATA_FILE_PATH, 'w') as data_file:
            data_file.write('0x000000AA\n0x000000BB\n0x000000CC\n0x000000DD\n')
            for _ in range(96):
                data_file.write(INITIAL_DATA_VALUE + '\n')
        target_address = 1
        target_size = 2
        self.ssd.run(['ssd', 'E', str(target_address), str(target_size)])

        lines = self.get_lines(TEST_DATA_FILE_PATH)
        with self.subTest("LBA=0"):
            self.assertEqual('0x000000AA', lines[0])
        with self.subTest("LBA=1"):
            self.assertEqual('0x00000000', lines[1])
        with self.subTest("LBA=2"):
            self.assertEqual('0x00000000', lines[2])
        with self.subTest("LBA=3"):
            self.assertEqual('0x000000DD', lines[3])
