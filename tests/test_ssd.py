import os
from unittest import TestCase

from hardware.ssd import SSD

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_FILE_PATH = os.path.join(CURRENT_FILE_PATH, 'test_nand.txt')
TEST_RESULT_FILE_PATH = os.path.join(CURRENT_FILE_PATH, 'test_result.txt')
TEST_BUFFER_FILE_PATH = os.path.join(CURRENT_FILE_PATH, 'test_buffer.txt')

INITIAL_DATA_VALUE = '0x00000000'


class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD(TEST_DATA_FILE_PATH, TEST_RESULT_FILE_PATH, TEST_BUFFER_FILE_PATH)

    def tearDown(self):
        os.remove(TEST_DATA_FILE_PATH)
        os.remove(TEST_RESULT_FILE_PATH)
        os.remove(TEST_BUFFER_FILE_PATH)

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
        with self.subTest("INVALID VALUE"):
            self.assert_ssd_run_raises(['ssd', 'E', '1', '-1'])

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
        self.ssd.run(['ssd', 'F'])

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
        self.ssd.run(['ssd', 'F'])

        lines = self.get_lines(TEST_DATA_FILE_PATH)
        with self.subTest("LBA=0"):
            self.assertEqual('0x000000AA', lines[0])
        with self.subTest("LBA=1"):
            self.assertEqual('0x00000000', lines[1])
        with self.subTest("LBA=2"):
            self.assertEqual('0x00000000', lines[2])
        with self.subTest("LBA=3"):
            self.assertEqual('0x000000DD', lines[3])

    def test_optimize_duplicated_write(self):
        self.ssd.run(['ssd', 'W', '20', '0xABCDABCD'])
        self.ssd.run(['ssd', 'W', '21', '0x12341234'])
        self.ssd.run(['ssd', 'W', '20', '0xEEEEFFFF'])
        del self.ssd
        lines = self.get_lines(TEST_BUFFER_FILE_PATH)
        lines = [e for e in lines if e != 'None']
        with self.subTest("BUFFER_LEN=2"):
            self.assertEqual(2, len(lines))
        with self.subTest("ADDR=21"):
            self.assertEqual('W 21 0x12341234', lines[0])
        with self.subTest("ADDR=20"):
            self.assertEqual('W 20 0xEEEEFFFF', lines[1])

    def test_optimize_post_erase(self):
        self.ssd.run(['ssd', 'W', '20', '0xABCDABCD'])
        self.ssd.run(['ssd', 'W', '21', '0x12341234'])
        self.ssd.run(['ssd', 'E', '18', '5'])
        del self.ssd
        lines = self.get_lines(TEST_BUFFER_FILE_PATH)
        lines = [e for e in lines if e != 'None']
        with self.subTest("BUFFER_LEN=1"):
            self.assertEqual(1, len(lines))
        with self.subTest("ADDR=18"):
            self.assertEqual('E 18 5', lines[0])

    def test_optimize_merge_erase(self):
        self.ssd.run(['ssd', 'W', '20', '0xABCDABCD'])
        self.ssd.run(['ssd', 'E', '10', '2'])
        self.ssd.run(['ssd', 'E', '12', '3'])
        del self.ssd
        lines = self.get_lines(TEST_BUFFER_FILE_PATH)
        lines = [e for e in lines if e != 'None']
        with self.subTest("BUFFER_LEN=2"):
            self.assertEqual(2, len(lines))
        with self.subTest("ADDR=20"):
            self.assertEqual('W 20 0xABCDABCD', lines[0])
        with self.subTest("ADDR=10"):
            self.assertEqual('E 10 5', lines[1])

    def test_optimize_narrow_range_of_erase(self):
        self.ssd.run(['ssd', 'E', '10', '4'])
        self.ssd.run(['ssd', 'E', '40', '5'])
        self.ssd.run(['ssd', 'W', '12', '0xABCD1234'])
        self.ssd.run(['ssd', 'E', '50', '1'])
        self.ssd.run(['ssd', 'W', '13', '0x4BCD5351'])
        self.ssd.run(['ssd', 'W', '50', '0xABCD1234'])
        del self.ssd
        lines = self.get_lines(TEST_BUFFER_FILE_PATH)
        lines = [e for e in lines if e != 'None']
        with self.subTest("BUFFER_LEN=5"):
            self.assertEqual(5, len(lines))
        with self.subTest("LINE 1"):
            self.assertEqual('E 10 2', lines[0])
        with self.subTest("LINE 2"):
            self.assertEqual('E 40 5', lines[1])
        with self.subTest("LINE 3"):
            self.assertEqual('W 12 0xABCD1234', lines[2])
        with self.subTest("LINE 4"):
            self.assertEqual('W 13 0x4BCD5351', lines[3])
        with self.subTest("LINE 5"):
            self.assertEqual('W 50 0xABCD1234', lines[4])
