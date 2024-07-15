from unittest import TestCase, skip
from unittest.mock import Mock
from hardware.ssd_writer import SSDWriter

class TestSSDWriter(TestCase):

    @skip
    def test_write01(self):
        write_file_name = 'nand.txt'
        logical_bytes_address = 1
        data_to_write = '0x9988FFFA'

        ssd_writer = SSDWriter()
        ssd_writer.write(write_file_name, logical_bytes_address, data_to_write)
        self.assertEqual(data_to_write, self.read_from_line(write_file_name, logical_bytes_address))

    @skip
    def test_write02(self):
        write_file_name = 'nand.txt'
        logical_bytes_address = 2
        data_to_write = '0x9988FFFB'

        ssd_writer = SSDWriter()
        ssd_writer.write(write_file_name, logical_bytes_address, data_to_write)
        self.assertEqual(data_to_write, self.read_from_line(write_file_name, logical_bytes_address))

    def read_from_line(self, write_file_name, logical_bytes_address):
        open_file = open(write_file_name, 'r')
        line_content = None

        for current_line_number, line in enumerate(open_file, start=0):
            if current_line_number == logical_bytes_address:
                line_content = line.strip()
                return line_content