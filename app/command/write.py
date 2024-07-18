from typing import List

from app.command.interface import ICommand
from app.input_checker import check_valid_address_int, check_valid_value
from app.shell_api import ShellAPI


class WriteCommand(ICommand):
    _lba: int
    _value: str

    def __init__(self, cmd: List[str]):
        if len(cmd) != 2:
            raise ValueError()
        lba_str = cmd[0]
        if not lba_str.isdigit():
            raise ValueError()
        lba = int(cmd[0])
        check_valid_address_int(lba)
        self._lba = lba
        value = cmd[1]
        check_valid_value(value)
        self._value = value

    def run(self, api: ShellAPI):
        api.write(self._lba, self._value)
