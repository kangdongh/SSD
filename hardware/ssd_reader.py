import os
from hardware.ssd_reader_interface import ISSDReader

READ_RESULT_FILE = './result.txt'


class SSDReader(ISSDReader):

    def read(
            self,
            read_file_name,
            logical_bytes_address: int
    ) -> str:
        line_content = self.read_from_line(read_file_name, logical_bytes_address)
        self.write_read_result(READ_RESULT_FILE, line_content)
        return line_content

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

    def write_read_result(self, write_file_name, read_result):

        try:
            with open("write_file_name", "w") as file_handler:
                file_handler.write(read_result)
                file_handler.close()
        except IOError as e:
            print(f"IOError 발생: {e}")
        except OSError as e:
            print(f"OSError 발생: {e}")
        except Exception as e:
            print(f"예기치 않은 예외 발생: {e}")
