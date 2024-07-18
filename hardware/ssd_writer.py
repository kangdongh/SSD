from hardware.ssd_writer_interface import ISSDWriter
from logger import CommandLogger


class SSDWriter(ISSDWriter):
    def __init__(self, write_file_path: str, max_lba: int = 100, logger: CommandLogger = CommandLogger()):
        self._logger = logger
        self._write_file_path = write_file_path
        self._max_lba = max_lba

    def write(self, logical_bytes_address: int, length_to_write: int, data_to_write: str):
        try:
            logger = self._logger.get_logger('write', self.__class__.__name__, 'write')
            logger.info(f'WRITE function received with param: {logical_bytes_address}, {length_to_write}, {data_to_write}')
            if not self._is_valid_address_and_data(logical_bytes_address, data_to_write):
                raise Exception('INVALID COMMAND')
            with open(self._write_file_path, 'r') as file:
                lines = file.readlines()
            if not self._is_valid_file(lines):
                raise Exception('INVALID COMMAND')

            for i in range(length_to_write):
                lines[logical_bytes_address + i] = data_to_write + '\n'

            with open(self._write_file_path, 'w') as file:
                file.writelines(lines)
        except Exception:
            raise Exception('INVALID COMMAND')

    def _is_valid_address_and_data(self, address, data):
        if address < 0 or address >= self._max_lba or len(data) != 10:
            return False

        if not data.startswith('0x'):
            return False

        hex_digits = set('0123456789abcdefABCDEF')
        for char in data[2:]:
            if char not in hex_digits:
                return False
        return True

    def _is_valid_file(self, file_line_lists):
        if len(file_line_lists) != self._max_lba:
            return False
        return True
