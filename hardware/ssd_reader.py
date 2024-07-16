import os
from hardware.ssd_reader_interface import ISSDReader

READ_RESULT_FILE = './result_test.txt'

class SSDReader(ISSDReader):
    def tearDown(self):
        os.remove(READ_RESULT_FILE)

    def read(
            self,
            read_file_name,
            logical_bytes_address: int
    ) -> str:
        line_content = self.read_from_line(read_file_name, logical_bytes_address)
        self.write_read_resut(READ_RESULT_FILE, line_content)
        return line_content

    def read_from_line(self, read_file_name, logical_bytes_address):

        try:
            file_handler = open(read_file_name, 'r')
        except FileExistsError:
            print(f'{read_file_name} 파일이 존재하지 않습니다.')

        line_content = None

        for current_line_number, line in enumerate(file_handler, start=0):
            if current_line_number == logical_bytes_address:
                line_content = line.strip()
                file_handler.close()
                return line_content

    def write_read_resut(self, write_file_name, read_result):
        file_handler = open(write_file_name, 'w')
        file_handler.write(read_result)
        file_handler.close()
        return
