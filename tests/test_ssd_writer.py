import os
from unittest import TestCase
from hardware.ssd_writer import SSDWriter

WRITE_FILE_NAME = './nand_test.txt'
INIT_VALUE = '0x00000000\n'


class TestSSDWriter(TestCase):

    def setUp(self):
        super().setUp()
        self.ssd_writer = SSDWriter(WRITE_FILE_NAME)
        self.file_handler = open(WRITE_FILE_NAME, 'w')
        for _ in range(100):
            self.file_handler.write(INIT_VALUE)
        self.file_handler.close()

    def tearDown(self):
        os.remove(WRITE_FILE_NAME)

    def test_success_write_to_line01(self):
        logical_bytes_address = 3
        data_to_write = '0x9988FFFA'

        self.ssd_writer.write(logical_bytes_address, 1, data_to_write)
        self.assertEqual(data_to_write, self.read_from_line(WRITE_FILE_NAME, logical_bytes_address))

    def test_success_write_to_line02(self):
        logical_bytes_address = 99
        data_to_write = '0x9988FFFB'

        self.ssd_writer.write(logical_bytes_address, 1, data_to_write)
        self.assertEqual(data_to_write, self.read_from_line(WRITE_FILE_NAME, logical_bytes_address))

    def read_from_line(self, read_file_name, logical_bytes_address) -> str:
        file_handler = open(read_file_name, 'r')

        line_content = None
        for current_line_number, line in enumerate(file_handler, start=0):
            if current_line_number == logical_bytes_address:
                line_content = line.strip()
                break
        file_handler.close()
        return line_content
