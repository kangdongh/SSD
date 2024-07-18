from typing import List

from app.command.interface import ICommand
from app.input_checker import check_valid_address_int
from app.shell_api import ShellAPI


class EraseRangeCommand(ICommand):
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
        lba_end = cmd[1]
        if not lba_end.isdigit():
            raise ValueError()
        lba_end = int(lba_end)
        size = lba_end - lba
        if size <= 0:
            raise ValueError()
        check_valid_address_int(lba + size - 1)
        self._size = size

    def run(self, api: ShellAPI):
        api.erase(self._lba, self._size)

    @classmethod
    def description(cls):
        return "Erase value from startLBA to endLBA on SSD / usage : erase_range <Start LBA>  <End LBA>"
