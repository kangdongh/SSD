from typing import List, Optional

from app.system_call_handler import SystemCallHandler


class ShellAPI:
    _system_call_handler: SystemCallHandler

    def __init__(self, system_call_handler: Optional[SystemCallHandler] = None):
        self._system_call_handler = \
            system_call_handler if system_call_handler is not None else SystemCallHandler()

    def _check_valid_lba(self, lba: int):
        if 0 <= lba < 100:
            return
        raise ValueError(f"Invalid lba Error: {lba}")

    def _check_valid_value(self, value: str):
        pass

    def read(self, lba: int):
        self._check_valid_lba(lba)
        s = SystemCallHandler()
        s.run(['R', str(lba)])
        return s.get_result()

    def write(self, lba: int, value: str):
        self._check_valid_lba(lba)
        self._check_valid_value(value)
        self._system_call(['W', str(lba), value])

    def erase(self, start_lba: int, size: int):
        self._check_valid_lba(start_lba)
        self._check_valid_lba(start_lba + size)
        while size > 0:
            erase_size = min(size, 10)
            self._system_call(['E', str(start_lba), str(erase_size)])
            size -= erase_size
            start_lba += erase_size

    def flush(self):
        self._system_call(['F'])

    def _system_call(self, system_call_arguments: List[str]):
        self._system_call_handler.run(system_call_arguments)

    def _read_result(self):
        return self._system_call_handler.get_result()
