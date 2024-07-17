from hardware.ssd_writer_interface import ISSDWriter
from logger import CommandLogger


class SSDWriter(ISSDWriter):
    def __init__(self, logger: CommandLogger = CommandLogger()):
        self._logger = logger

    def write(self, write_file_path: str, logical_bytes_address: int, data_to_write: str, max_lba: int = 100):
        logger = self._logger.get_logger('write', self.__class__.__name__, 'write')
        logger.info(f'WRITE function received with param: {write_file_path}, {logical_bytes_address}, {data_to_write}')
        try:
            if not self._is_valid_address_and_data(logical_bytes_address, data_to_write, max_lba):
                raise Exception('INVALID COMMAND')
            with open(write_file_path, 'r') as file:
                lines = file.readlines()
            if not self._is_valid_file(lines, max_lba):
                raise Exception('INVALID COMMAND')

            lines[logical_bytes_address] = data_to_write + '\n'

            with open(write_file_path, 'w') as file:
                file.writelines(lines)
        except Exception:
            raise Exception('INVALID COMMAND')

    def _is_valid_address_and_data(self, address, data, max_lba):
        if address < 0 or address >= max_lba or len(data) != 10:
            return False

        if not data.startswith('0x'):
            return False

        hex_digits = set('0123456789abcdefABCDEF')
        for char in data[2:]:
            if char not in hex_digits:
                return False
        return True

    def _is_valid_file(self, file_line_lists, max_lba):
        if len(file_line_lists) != max_lba:
            return False
        return True
