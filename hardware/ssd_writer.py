from hardware.ssd_writer_interface import ISSDWriter


class SSDWriter(ISSDWriter):
    def write(self, write_file_path: str, logical_bytes_address: int, data_to_write: str):
        try:
            if not self._is_valid_data(data_to_write):
                raise Exception('INVALID COMMAND')
            with open(write_file_path, 'r') as file:
                lines = file.readlines()
            if not self._is_valid_file(lines):
                raise Exception('INVALID COMMAND')

            lines[logical_bytes_address] = data_to_write + '\n'

            with open(write_file_path, 'w') as file:
                file.writelines(lines)
        except Exception:
            raise Exception('INVALID COMMAND')

    def _is_valid_data(self, data):
        if len(data) != 10:
            return False

        if not data.startswith('0x'):
            return False

        hex_digits = set('0123456789abcdefABCDEF')
        for char in data[2:]:
            if char not in hex_digits:
                return False
        return True

    def _is_valid_file(self, file_line_lists):
        if len(file_line_lists) != 100:
            return False
        return True
