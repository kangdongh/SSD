from typing import List

from app.command.interface import ICommand
from app.input_checker import check_valid_value
from app.shell_api import ShellAPI


class FullWriteCommand(ICommand):
    _value: str

    def __init__(self, cmd: List[str]):
        if len(cmd) != 1:
            raise ValueError()
        value = cmd[0]
        check_valid_value(value)
        self._value = value

    def run(self, api: ShellAPI):
        for lba in range(100):
            api.write(lba, self._value)

    @classmethod
    def description(cls):
        return "Write value at all LBAs / usage: fullwrite <VALUE>"
