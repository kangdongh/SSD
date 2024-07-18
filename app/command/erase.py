from typing import List

from app.command.interface import ICommand
from app.input_checker import check_valid_address_int
from app.shell_api import ShellAPI


class EraseCommand(ICommand):
    _lba: int
    _size: int

    def __init__(self, cmd: List[str]):
        if len(cmd) != 2:
            raise ValueError()
        lba_str = cmd[0]
        if not lba_str.isdigit():
            raise ValueError()
        lba = int(cmd[0])
        check_valid_address_int(lba)
        self._lba = lba
        size_str = cmd[1]
        if not size_str.isdigit():
            raise ValueError()
        size = int(size_str)
        if size <= 0:
            raise ValueError()
        check_valid_address_int(lba + size)
        self._size = size

    def run(self, api: ShellAPI):
        api.erase(self._lba, self._size)
