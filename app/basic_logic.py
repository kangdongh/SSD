import subprocess
from typing import List


class BasicLogic:
    _ssd_path: str

    def __init__(self, ssd_path):
        self._ssd_path = ssd_path

    def read(self, lba: str) -> str:
        pass

    def write(self, lba: str, value: str) -> None:
        pass

    def full_read(self) -> str:
        pass

    def full_write(self, value: str) -> None:
        pass

    def help(self) -> str:
        help_str = ""
        with open('./help_description.txt', 'r') as file:
            help_str = file.read()

        return help_str

    def _system_call(self, args: List[str]):
        subprocess.run(['python', self._ssd_path] + args)

    def _read_result(self):
        # read result.txt and return the read value
        pass

    def _write_result(self):
        pass

    def _full_read_result(self):
        # read result.txt and return the read value
        pass

    def _help_result(self):
        pass
