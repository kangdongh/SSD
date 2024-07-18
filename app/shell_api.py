from typing import List, Optional

from app.input_checker import check_valid_address_int, check_valid_value
from app.system_call_handler import SystemCallHandler


class ShellAPI:
    _system_call_handler: SystemCallHandler

    def __init__(self, system_call_handler: Optional[SystemCallHandler] = None):
        self._system_call_handler = \
            system_call_handler if system_call_handler is not None else SystemCallHandler()

    def read(self, lba: int):
        check_valid_address_int(lba)
        self._system_call(['R', str(lba)])
        return self._read_result()

    def write(self, lba: int, value: str):
        check_valid_address_int(lba)
        check_valid_value(value)
        self._system_call(['W', str(lba), value])

    def erase(self, start_lba: int, size: int):
        check_valid_address_int(start_lba)
        check_valid_address_int(start_lba + size)
        while size > 0:
            erase_size = min(size, 10)
            self._system_call(['E', str(start_lba), str(erase_size)])
            size -= erase_size
            start_lba += erase_size

    def flush(self):
        self._system_call(['F'])

    def get_system_env(self):
        ssd_path = self._system_call_handler.get_ssd_path()
        result_path = self._system_call_handler.get_result_file_path()
        return [ssd_path, result_path]

    def _system_call(self, system_call_arguments: List[str]):
        self._system_call_handler.run(system_call_arguments)

    def _read_result(self):
        return self._system_call_handler.get_result()
