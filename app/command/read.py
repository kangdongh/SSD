from typing import List

from app.command.interface import ICommand
from app.input_checker import check_valid_address_int
from app.shell_api import ShellAPI


class ReadCommand(ICommand):
    _lba: int

    def __init__(self, cmd: List[str]):
        if len(cmd) != 1:
            raise ValueError()
        lba_str = cmd[0]
        if not lba_str.isdigit():
            raise ValueError()
        lba = int(lba_str)
        check_valid_address_int(lba)
        self._lba = lba

    def run(self, api: ShellAPI):
        print(api.read(self._lba))

    @classmethod
    def description(cls):
        return "Read value from SSD / usage: read <LBA>"
