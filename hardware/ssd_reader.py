from hardware.ssd_reader_interface import ISSDReader
from logger import CommandLogger


class SSDReader(ISSDReader):
    def __init__(self, logger: CommandLogger = CommandLogger()):
        self._logger = logger

    def read(
            self,
            read_file_name,
            logical_bytes_address: int
    ) -> str:
        logger = self._logger.get_logger('read', self.__class__.__name__, 'read')
        logger.info(f'READ function received with param: {read_file_name}, {logical_bytes_address}')
        return self.read_from_line(read_file_name, logical_bytes_address)

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
