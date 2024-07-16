import os
from hardware.ssd_reader_interface import ISSDReader

class SSDReader(ISSDReader):

    def read(
            self,
            read_file_name,
            logical_bytes_address: int
    ) -> str:
        return self.read_from_line(read_file_name, logical_bytes_address)

    def read_from_line(self, read_file_name, logical_bytes_address) -> str:

        try:
            with open(read_file_name, 'r', encoding='utf-8') as file_handler:
                line_content = None
                for current_line_number, line in enumerate(file_handler, start=0):
                    if current_line_number == logical_bytes_address:
                        line_content = line.strip()
                        break;

                file_handler.close()
                return line_content

        except FileExistsError:
            print(f'{read_file_name} 파일이 존재하지 않습니다.')
