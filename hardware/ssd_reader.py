from hardware.ssd_reader_interface import ISSDReader


class SSDReader(ISSDReader):
    def __init__(self, read_file_name):
        self._read_file_name = read_file_name

    def read(
            self,
            logical_bytes_address: int
    ) -> str:
        return self.read_from_line(self._read_file_name, logical_bytes_address)

    def read_from_line(self, read_file_name, logical_bytes_address) -> str:
        try:
            with open(read_file_name, 'r', encoding='utf-8') as file_handler:
                lines = file_handler.readlines()
                if logical_bytes_address < len(lines):
                    line_content = lines[logical_bytes_address].strip()
                    return line_content
                else:
                    print(f'주소 {logical_bytes_address}가 설정된 용량을 초과 합니다.')
                    return None

        except FileExistsError:
            print(f'{read_file_name} 파일이 존재하지 않습니다.')
